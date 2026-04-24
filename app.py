#!/usr/bin/env python3
"""
SkiOx Dashboard - Enhanced Professional Edition
Premium UI with modern color scheme and professional styling
"""

import http.server
import socketserver
import json
import sqlite3
import os
import sys
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import mimetypes

# Configuration
PORT = 8001
DATABASE = 'skiox_data.db'

class SkiOxDashboard:
    """Manages SkiOx dashboard data and logic"""
    
    # Critical SpO2 threshold for alerting rescue team
    SPO2_CRITICAL_THRESHOLD = 94
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.last_alert_spo2 = None
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS components (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                status TEXT,
                type TEXT,
                location TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                spo2 REAL,
                heart_rate INTEGER
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                message TEXT,
                severity TEXT,
                resolved INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_status (
                id INTEGER PRIMARY KEY,
                status TEXT,
                uptime INTEGER,
                last_update TEXT
            )
        ''')
        
        conn.commit()
        
        cursor.execute('SELECT COUNT(*) FROM components')
        if cursor.fetchone()[0] == 0:
            self.load_sample_data()
        
        conn.close()
    
    def load_sample_data(self):
        """Load sample data for demonstration"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        components = [
            ('Oxygen Tank', 'active', 'Core', 'Main Storage'),
            ('Primary Regulator', 'active', 'Core', 'Tank Connection'),
            ('Backup Regulator', 'standby', 'Core', 'Tank Connection'),
            ('Main Flow Meter', 'active', 'Core', 'Flow Control'),
            ('Backup Flow Meter', 'standby', 'Core', 'Flow Control'),
            ('Pressure Gauge', 'active', 'Monitoring', 'Tank'),
            ('Temperature Sensor', 'active', 'Monitoring', 'System'),
            ('Humidity Sensor', 'active', 'Monitoring', 'System'),
            ('SpO2 Sensor', 'active', 'Monitoring', 'Patient'),
            ('Heart Rate Monitor', 'active', 'Monitoring', 'Patient'),
            ('Primary Alarm', 'active', 'Safety', 'Alert System'),
            ('Backup Alarm', 'standby', 'Safety', 'Alert System'),
        ]
        
        for name, status, comp_type, location in components:
            cursor.execute(
                'INSERT INTO components (name, status, type, location) VALUES (?, ?, ?, ?)',
                (name, status, comp_type, location)
            )
        
        now = datetime.now().isoformat()
        cursor.execute(
            'INSERT INTO sensor_readings (timestamp, spo2, heart_rate) VALUES (?, ?, ?)',
            (now, 98.5, 72)
        )
        
        cursor.execute(
            'INSERT INTO alerts (timestamp, message, severity, resolved) VALUES (?, ?, ?, ?)',
            (now, '✅ System initialized successfully', 'info', 0)
        )
        
        cursor.execute(
            'INSERT INTO system_status (status, uptime, last_update) VALUES (?, ?, ?)',
            ('online', 0, now)
        )
        
        conn.commit()
        conn.close()
    
    def get_dashboard_data(self):
        """Get all dashboard data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM components')
        components = [dict(zip([desc[0] for desc in cursor.description], row)) for row in cursor.fetchall()]
        
        cursor.execute('SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT 1')
        sensor = cursor.fetchone()
        sensor_data = {
            'timestamp': sensor[1],
            'spo2': sensor[2],
            'heart_rate': sensor[3]
        } if sensor else {}
        
        cursor.execute('SELECT * FROM alerts WHERE resolved = 0')
        alerts = [dict(zip([desc[0] for desc in cursor.description], row)) for row in cursor.fetchall()]
        
        cursor.execute('SELECT * FROM system_status ORDER BY id DESC LIMIT 1')
        status = cursor.fetchone()
        system_status = {
            'status': status[1],
            'uptime': status[2],
            'last_update': status[3]
        } if status else {}
        
        conn.close()
        
        return {
            'components': components,
            'sensor_readings': sensor_data,
            'alerts': alerts,
            'system_status': system_status,
            'timestamp': datetime.now().isoformat()
        }
    
    def add_sensor_reading(self, spo2, heart_rate):
        """Add new sensor reading and check for critical SpO2 levels"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        cursor.execute(
            'INSERT INTO sensor_readings (timestamp, spo2, heart_rate) VALUES (?, ?, ?)',
            (now, spo2, heart_rate)
        )
        
        if spo2 is not None and spo2 < self.SPO2_CRITICAL_THRESHOLD:
            if self.last_alert_spo2 is None or self.last_alert_spo2 >= self.SPO2_CRITICAL_THRESHOLD:
                alert_msg = f"🚨 CRITICAL: SpO2 level {spo2}% is BELOW threshold ({self.SPO2_CRITICAL_THRESHOLD}%) - NOTIFYING RESCUE TEAM"
                cursor.execute(
                    'INSERT INTO alerts (timestamp, message, severity) VALUES (?, ?, ?)',
                    (now, alert_msg, 'error')
                )
            self.last_alert_spo2 = spo2
        else:
            self.last_alert_spo2 = spo2
        
        cursor.execute('DELETE FROM sensor_readings WHERE id NOT IN (SELECT id FROM sensor_readings ORDER BY id DESC LIMIT 1000)')
        
        conn.commit()
        conn.close()
        return True
    
    def toggle_component(self, component_id):
        """Toggle component status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT status FROM components WHERE id = ?', (component_id,))
        result = cursor.fetchone()
        
        if result:
            new_status = 'standby' if result[0] == 'active' else 'active'
            cursor.execute('UPDATE components SET status = ? WHERE id = ?', (new_status, component_id))
            conn.commit()
        
        conn.close()
        return bool(result)
    
    def add_alert(self, message, severity):
        """Add new alert"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        cursor.execute(
            'INSERT INTO alerts (timestamp, message, severity) VALUES (?, ?, ?)',
            (now, message, severity)
        )
        
        conn.commit()
        conn.close()
        return True

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler"""
    
    dashboard = None
    
    # Professional color scheme
    COLORS = {
        'primary': '#0369a1',      # Slate Blue
        'secondary': '#06b6d4',    # Cyan
        'success': '#10b981',      # Emerald
        'warning': '#f59e0b',      # Amber
        'danger': '#ef4444',       # Red
        'dark': '#0f172a',         # Dark Slate
        'light': '#f8fafc',        # Light Slate
    }
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)
        
        if path == '/api/dashboard':
            self.send_json(self.dashboard.get_dashboard_data())
        elif path == '/api/components':
            self.send_json({'components': self.dashboard.get_dashboard_data()['components']})
        elif path == '/api/sensor-readings':
            data = self.dashboard.get_dashboard_data()
            self.send_json(data['sensor_readings'])
        elif path == '/' or path == '/index.html':
            self.send_html(self.get_dashboard_html())
        elif path == '/admin' or path == '/admin.html':
            self.send_html(self.get_admin_html())
        elif path.startswith('/static/'):
            self.serve_static(path)
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body)
        except:
            self.send_error(400)
            return
        
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/sensor-readings':
            self.dashboard.add_sensor_reading(data.get('spo2'), data.get('heart_rate'))
            self.send_json({'success': True})
        elif path == '/api/components/toggle':
            self.dashboard.toggle_component(data.get('id'))
            self.send_json(self.dashboard.get_dashboard_data())
        elif path == '/api/alerts':
            self.dashboard.add_alert(data.get('message'), data.get('severity', 'warning'))
            self.send_json({'success': True})
        else:
            self.send_error(404)
    
    def send_json(self, data):
        """Send JSON response"""
        response = json.dumps(data).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(response))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response)
    
    def send_html(self, html):
        """Send HTML response"""
        response = html.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', len(response))
        self.end_headers()
        self.wfile.write(response)
    
    def serve_static(self, path):
        """Serve static files"""
        file_path = path.lstrip('/')
        
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                content = f.read()
            
            mime_type, _ = mimetypes.guess_type(file_path)
            self.send_response(200)
            self.send_header('Content-Type', mime_type or 'application/octet-stream')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404)
    
    def get_dashboard_html(self):
        """Return professional dashboard HTML"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SkiOx Dashboard - Professional Medical Monitoring</title>
    <style>
        :root {
            --primary: #0369a1;
            --secondary: #06b6d4;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --dark: #0f172a;
            --light: #f8fafc;
            --gray-100: #f1f5f9;
            --gray-200: #e2e8f0;
            --gray-700: #374151;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 50%, #f8fafc 100%);
            color: var(--gray-700);
            line-height: 1.6;
            min-height: 100vh;
        }
        
        .container { max-width: 1400px; margin: 0 auto; padding: 30px 20px; }
        
        header {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 50px 30px;
            margin-bottom: 40px;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(3, 105, 161, 0.2);
            position: relative;
            overflow: hidden;
        }
        
        header::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
            animation: shimmer 3s infinite;
        }
        
        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        header h1 {
            font-size: 2.8em;
            margin-bottom: 10px;
            font-weight: 800;
            letter-spacing: -1px;
            position: relative;
            z-index: 1;
        }
        
        header p {
            font-size: 1.1em;
            opacity: 0.95;
            position: relative;
            z-index: 1;
        }
        
        .nav-bar {
            display: flex;
            gap: 15px;
            margin-bottom: 40px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .nav-btn, .nav-link {
            background: white;
            color: var(--primary);
            border: 2px solid var(--primary);
            padding: 12px 24px;
            border-radius: 10px;
            cursor: pointer;
            font-weight: 700;
            font-size: 0.95em;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            box-shadow: 0 4px 12px rgba(3, 105, 161, 0.15);
        }
        
        .nav-btn:hover, .nav-link:hover {
            background: var(--primary);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(3, 105, 161, 0.3);
        }
        
        .grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); 
            gap: 25px; 
            margin-bottom: 40px;
        }
        
        .card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
            border-left: 5px solid var(--primary);
            transition: all 0.3s ease;
        }
        
        .card:hover {
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12);
            transform: translateY(-4px);
        }
        
        .card.success { border-left-color: var(--success); }
        .card.warning { border-left-color: var(--warning); }
        .card.danger { border-left-color: var(--danger); }
        
        .card h2 {
            font-size: 1.4em;
            margin-bottom: 20px;
            color: var(--primary);
            border-bottom: 2px solid var(--gray-200);
            padding-bottom: 15px;
        }
        
        .status-badge {
            display: inline-block;
            padding: 8px 14px;
            border-radius: 6px;
            font-size: 0.85em;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .status-active { background: var(--success); color: white; }
        .status-standby { background: var(--warning); color: white; }
        .status-online { background: var(--success); color: white; }
        
        .component {
            background: var(--gray-100);
            padding: 15px;
            margin: 12px 0;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.2s ease;
        }
        
        .component:hover {
            background: var(--gray-200);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        .component-info h3 {
            font-weight: 700;
            color: var(--dark);
            margin-bottom: 4px;
        }
        
        .component-type {
            font-size: 0.85em;
            color: var(--primary);
            font-weight: 600;
        }
        
        .sensor-value {
            font-size: 2.5em;
            font-weight: 900;
            color: var(--primary);
            margin: 15px 0;
            line-height: 1;
        }
        
        .sensor-label {
            color: var(--gray-700);
            font-size: 0.95em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .alert {
            padding: 16px;
            margin: 12px 0;
            border-radius: 8px;
            border-left: 4px solid;
            background-color: var(--light);
        }
        
        .alert-info {
            border-left-color: var(--primary);
            color: var(--primary);
            background: rgba(3, 105, 161, 0.05);
        }
        
        .alert-warning {
            border-left-color: var(--warning);
            color: #92400e;
            background: rgba(245, 158, 11, 0.05);
        }
        
        .alert-error {
            border-left-color: var(--danger);
            color: #7f1d1d;
            background: rgba(239, 68, 68, 0.05);
        }
        
        .alert-success {
            border-left-color: var(--success);
            color: #065f46;
            background: rgba(16, 185, 129, 0.05);
        }
        
        .alert strong {
            font-weight: 700;
            display: block;
            margin-bottom: 4px;
        }
        
        .alert-timestamp {
            font-size: 0.85em;
            opacity: 0.8;
            margin-top: 8px;
        }
        
        .loading {
            text-align: center;
            color: var(--primary);
            padding: 30px;
            font-weight: 600;
        }
        
        .fullwidth { grid-column: 1 / -1; }
        
        footer {
            text-align: center;
            margin-top: 60px;
            padding-top: 30px;
            border-top: 2px solid var(--gray-200);
            color: var(--gray-700);
            font-size: 0.9em;
        }
        
        @media (max-width: 768px) {
            .grid { grid-template-columns: 1fr; }
            header h1 { font-size: 2em; }
            .sensor-value { font-size: 1.8em; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏥 SkiOx Dashboard</h1>
            <p>Professional IoT Emergency Oxygen Delivery System Monitor</p>
        </header>
        
        <div class="nav-bar">
            <button class="nav-btn" onclick="location.href='/admin'">⚙️ Admin Panel</button>
        </div>
        
        <div id="content" class="grid loading">Loading dashboard data...</div>
        
        <footer>
            <p><strong>SkiOx Medical System</strong> • Real-time Monitoring & Emergency Management</p>
            <p style="margin-top: 10px; opacity: 0.7;">Last updated: <span id="last-update">--:--:--</span></p>
        </footer>
    </div>
    
    <script>
        const API_BASE = '/api';
        
        function formatTime(isoString) {
            if (!isoString) return '--:--:--';
            const date = new Date(isoString);
            return date.toLocaleTimeString();
        }
        
        function getStatusClass(status) {
            return 'status-' + status.toLowerCase();
        }
        
        async function loadDashboard() {
            try {
                const response = await fetch(API_BASE + '/dashboard');
                const data = await response.json();
                renderDashboard(data);
            } catch (error) {
                document.getElementById('content').innerHTML = '<div class="card danger" style="grid-column: 1/-1;"><h2>⚠️ Error</h2>Error loading dashboard: ' + error.message + '</div>';
            }
        }
        
        function renderDashboard(data) {
            let html = '';
            
            const status = data.system_status || {};
            html += '<div class="card success">';
            html += '<h2>📊 System Status</h2>';
            html += '<p><strong>Status:</strong> <span class="status-badge ' + getStatusClass(status.status || 'offline') + '">' + (status.status || 'Offline').toUpperCase() + '</span></p>';
            html += '<p style="margin-top: 10px;"><strong>Uptime:</strong> ' + (status.uptime || 0) + 's</p>';
            html += '</div>';
            
            const sensor = data.sensor_readings || {};
            html += '<div class="card">';
            html += '<h2>❤️ Vital Signs</h2>';
            html += '<div><span class="sensor-label">SpO₂ Level</span><div class="sensor-value">' + (sensor.spo2 || '--') + '%</div></div>';
            html += '<div style="margin-top: 20px;"><span class="sensor-label">Heart Rate</span><div class="sensor-value">' + (sensor.heart_rate || '--') + '</div><span class="sensor-label">BPM</span></div>';
            html += '</div>';
            
            if (data.components && data.components.length > 0) {
                const active = data.components.filter(c => c.status === 'active').length;
                const standby = data.components.filter(c => c.status === 'standby').length;
                
                html += '<div class="card fullwidth">';
                html += '<h2>📦 System Components (' + data.components.length + ')</h2>';
                html += '<div style="margin-bottom: 20px; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">';
                html += '<div><span style="font-size: 0.9em; color: var(--gray-700);">ACTIVE</span><div style="font-size: 2em; font-weight: 900; color: var(--success);">' + active + '</div></div>';
                html += '<div><span style="font-size: 0.9em; color: var(--gray-700);">STANDBY</span><div style="font-size: 2em; font-weight: 900; color: var(--warning);">' + standby + '</div></div>';
                html += '</div>';
                
                data.components.forEach(comp => {
                    html += '<div class="component">';
                    html += '<div class="component-info"><h3>' + comp.name + '</h3><div class="component-type">' + comp.type + ' • ' + comp.location + '</div></div>';
                    html += '<span class="status-badge ' + getStatusClass(comp.status) + '">' + comp.status.toUpperCase() + '</span>';
                    html += '</div>';
                });
                html += '</div>';
            }
            
            if (data.alerts && data.alerts.length > 0) {
                html += '<div class="card fullwidth danger">';
                html += '<h2>🚨 Active Alerts (' + data.alerts.length + ')</h2>';
                data.alerts.forEach(alert => {
                    const alertClass = 'alert alert-' + (alert.severity || 'info');
                    html += '<div class="' + alertClass + '">';
                    html += '<strong>' + alert.message + '</strong>';
                    html += '<div class="alert-timestamp">' + formatTime(alert.timestamp) + '</div>';
                    html += '</div>';
                });
                html += '</div>';
            }
            
            document.getElementById('content').innerHTML = html;
            document.getElementById('last-update').textContent = formatTime(data.timestamp);
        }
        
        loadDashboard();
        setInterval(loadDashboard, 5000);
    </script>
</body>
</html>'''
    
    def get_admin_html(self):
        """Return professional admin panel HTML"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SkiOx Admin Panel - System Management</title>
    <style>
        :root {
            --primary: #0369a1;
            --secondary: #06b6d4;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --dark: #0f172a;
            --light: #f8fafc;
            --gray-100: #f1f5f9;
            --gray-200: #e2e8f0;
            --gray-700: #374151;
            --gray-800: #1f2937;
        }
        
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: var(--gray-100); }
        ::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 4px; }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 50%, #f8fafc 100%);
            color: var(--gray-800);
            line-height: 1.6;
        }
        
        .container { max-width: 1600px; margin: 0 auto; padding: 30px 20px; }
        
        header {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 40px 30px;
            margin-bottom: 30px;
            border-radius: 12px;
            box-shadow: 0 15px 40px rgba(3, 105, 161, 0.2);
        }
        
        header h1 {
            font-size: 2.2em;
            margin-bottom: 8px;
            font-weight: 800;
        }
        
        header p {
            font-size: 1em;
            opacity: 0.95;
        }
        
        .controls {
            display: flex;
            gap: 12px;
            margin-bottom: 30px;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .tab-btn {
            background: white;
            color: var(--primary);
            border: 2px solid var(--primary);
            padding: 11px 22px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 700;
            font-size: 0.95em;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(3, 105, 161, 0.15);
        }
        
        .tab-btn:hover {
            background: var(--primary);
            color: white;
            transform: translateY(-2px);
        }
        
        .tab-btn.active {
            background: var(--primary);
            color: white;
        }
        
        .content-tab {
            display: none;
        }
        
        .content-tab.active {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
        }
        
        .panel {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
            border-top: 4px solid var(--primary);
        }
        
        .panel h2 {
            color: var(--primary);
            margin-bottom: 20px;
            font-size: 1.3em;
            border-bottom: 2px solid var(--gray-200);
            padding-bottom: 12px;
        }
        
        .form-group {
            margin-bottom: 16px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 6px;
            color: var(--gray-800);
            font-weight: 700;
            font-size: 0.9em;
        }
        
        input[type="text"], input[type="number"], select {
            width: 100%;
            padding: 10px 14px;
            background: var(--light);
            border: 2px solid var(--gray-200);
            color: var(--gray-800);
            border-radius: 8px;
            font-size: 0.95em;
            transition: all 0.2s ease;
        }
        
        input:focus, select:focus {
            outline: none;
            border-color: var(--primary);
            background: white;
            box-shadow: 0 0 0 3px rgba(3, 105, 161, 0.1);
        }
        
        .btn {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            border: none;
            padding: 11px 22px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 700;
            font-size: 0.9em;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(3, 105, 161, 0.2);
            width: 100%;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(3, 105, 161, 0.3);
        }
        
        .btn-danger {
            background: linear-gradient(135deg, var(--danger) 0%, #dc2626 100%);
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
        }
        
        .btn-danger:hover {
            box-shadow: 0 6px 20px rgba(239, 68, 68, 0.3);
        }
        
        .btn-success {
            background: linear-gradient(135deg, var(--success) 0%, #059669 100%);
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
        }
        
        .table-responsive {
            overflow-x: auto;
            border-radius: 8px;
            border: 1px solid var(--gray-200);
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.9em;
        }
        
        thead {
            background: linear-gradient(135deg, var(--gray-100) 0%, var(--light) 100%);
        }
        
        th {
            padding: 12px 16px;
            color: var(--primary);
            font-weight: 700;
            border-bottom: 2px solid var(--gray-200);
            text-transform: uppercase;
            letter-spacing: 0.4px;
        }
        
        td {
            padding: 12px 16px;
            border-bottom: 1px solid var(--gray-200);
        }
        
        tbody tr:hover {
            background: var(--light);
        }
        
        .badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 0.8em;
            font-weight: 700;
            text-transform: uppercase;
        }
        
        .badge-active { background: var(--success); color: white; }
        .badge-standby { background: var(--warning); color: white; }
        .badge-error { background: var(--danger); color: white; }
        .badge-info { background: var(--primary); color: white; }
        
        .alert {
            padding: 14px;
            border-radius: 8px;
            margin-bottom: 12px;
            border-left: 4px solid;
            font-weight: 600;
        }
        
        .alert-success { background: rgba(16, 185, 129, 0.1); border-left-color: var(--success); color: #065f46; }
        .alert-error { background: rgba(239, 68, 68, 0.1); border-left-color: var(--danger); color: #7f1d1d; }
        .alert-info { background: rgba(3, 105, 161, 0.1); border-left-color: var(--primary); color: #082f49; }
        
        pre {
            background: var(--dark);
            color: #10b981;
            padding: 16px;
            border-radius: 8px;
            overflow-y: auto;
            max-height: 300px;
            font-size: 0.85em;
            line-height: 1.4;
        }
        
        .fullwidth { grid-column: 1 / -1; }
        
        footer {
            margin-top: 50px;
            text-align: center;
            padding-top: 30px;
            border-top: 2px solid var(--gray-200);
            color: var(--gray-700);
            font-size: 0.9em;
        }
        
        @media (max-width: 768px) {
            .content-tab.active {
                grid-template-columns: 1fr;
            }
            header h1 { font-size: 1.6em; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔐 SkiOx Admin Panel</h1>
            <p>Professional System Management & Real-time Monitoring</p>
        </header>
        
        <div class="controls">
            <button class="tab-btn active" onclick="switchTab('components')">📦 Components</button>
            <button class="tab-btn" onclick="switchTab('sensors')">📊 Sensor Data</button>
            <button class="tab-btn" onclick="switchTab('alerts')">🚨 Alerts</button>
            <button class="tab-btn" onclick="switchTab('test')">🧪 Test Tools</button>
            <a href="/" style="text-decoration: none;"><button class="tab-btn" style="background: var(--light); color: var(--gray-800); border-color: var(--gray-200);">← Dashboard</button></a>
        </div>
        
        <!-- Components Tab -->
        <div id="components" class="content-tab active">
            <div class="panel fullwidth">
                <h2>📦 System Components Management</h2>
                <div class="table-responsive">
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th><th>Component</th><th>Type</th><th>Location</th><th>Status</th><th>Action</th>
                            </tr>
                        </thead>
                        <tbody id="components-list">
                            <tr><td colspan="6" style="text-align: center; color: var(--primary);">Loading...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <!-- Sensors Tab -->
        <div id="sensors" class="content-tab">
            <div class="panel">
                <h2>➕ Add Sensor Reading</h2>
                <div class="form-group">
                    <label>SpO2 Level (%)</label>
                    <input type="number" id="spo2-input" min="0" max="100" value="98.5" placeholder="0-100">
                </div>
                <div class="form-group">
                    <label>Heart Rate (BPM)</label>
                    <input type="number" id="hr-input" min="0" max="200" value="72" placeholder="0-200">
                </div>
                <button class="btn" onclick="addSensorReading()">➕ Add Reading</button>
                <div id="sensor-message" style="margin-top: 12px;"></div>
            </div>
            
            <div class="panel">
                <h2>📈 Latest Reading</h2>
                <div id="latest-readings" style="color: var(--gray-700);">Loading...</div>
            </div>
        </div>
        
        <!-- Alerts Tab -->
        <div id="alerts" class="content-tab">
            <div class="panel">
                <h2>🚨 Create Alert</h2>
                <div class="form-group">
                    <label>Message</label>
                    <input type="text" id="alert-message" placeholder="Enter alert message">
                </div>
                <div class="form-group">
                    <label>Severity</label>
                    <select id="alert-severity">
                        <option value="info">Info</option>
                        <option value="warning">Warning</option>
                        <option value="error" selected>Error</option>
                    </select>
                </div>
                <button class="btn" onclick="createAlert()">➕ Create Alert</button>
                <div id="alert-message-box" style="margin-top: 12px;"></div>
            </div>
            
            <div class="panel fullwidth">
                <h2>📋 All Active Alerts</h2>
                <div id="alerts-list" style="color: var(--gray-700);">Loading...</div>
            </div>
        </div>
        
        <!-- Test Tools Tab -->
        <div id="test" class="content-tab">
            <div class="panel">
                <h2>🧪 Critical Alert Test</h2>
                <p style="font-size: 0.9em; color: var(--gray-700); margin-bottom: 15px;">Test SpO2 < 94% → Rescue Team Notification</p>
                <div class="form-group">
                    <label>SpO2 Value (%)</label>
                    <input type="number" id="test-spo2" min="0" max="100" value="92">
                </div>
                <button class="btn btn-danger" onclick="testCriticalAlert()">⚠️ Trigger Alert</button>
            </div>
            
            <div class="panel">
                <h2>🔄 Toggle Component</h2>
                <div class="form-group">
                    <label>Component ID</label>
                    <input type="number" id="toggle-id" min="1" value="1">
                </div>
                <button class="btn btn-success" onclick="toggleComponent()">🔄 Toggle</button>
            </div>
            
            <div class="panel fullwidth">
                <h2>📡 API Endpoint Tester</h2>
                <div class="form-group">
                    <label>Endpoint</label>
                    <input type="text" id="api-endpoint" value="/api/dashboard" placeholder="/api/...">
                </div>
                <button class="btn" onclick="callAPI()">🔗 Call API</button>
                <pre id="api-response" style="display: none; margin-top: 12px;"></pre>
            </div>
        </div>
        
        <footer>
            <p><strong>SkiOx Professional Admin Panel</strong> • Complete System Control & Monitoring</p>
        </footer>
    </div>
    
    <script>
        const API_BASE = '/api';
        
        function switchTab(tab) {
            document.querySelectorAll('.content-tab').forEach(el => el.classList.remove('active'));
            document.getElementById(tab).classList.add('active');
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            if (tab === 'components') loadComponents();
            if (tab === 'sensors') loadLatestReadings();
            if (tab === 'alerts') loadAlerts();
        }
        
        async function loadComponents() {
            try {
                const response = await fetch(API_BASE + '/components');
                const data = await response.json();
                let html = '';
                
                data.components.forEach(comp => {
                    const statusClass = comp.status === 'active' ? 'badge-active' : 'badge-standby';
                    html += '<tr>';
                    html += '<td><strong>' + comp.id + '</strong></td>';
                    html += '<td>' + comp.name + '</td>';
                    html += '<td>' + comp.type + '</td>';
                    html += '<td>' + comp.location + '</td>';
                    html += '<td><span class="badge ' + statusClass + '">' + comp.status + '</span></td>';
                    html += '<td><button class="btn" style="width: 80px; padding: 6px; font-size: 0.8em;" onclick="toggleComponentId(' + comp.id + ')">Toggle</button></td>';
                    html += '</tr>';
                });
                
                document.getElementById('components-list').innerHTML = html;
            } catch (error) {
                document.getElementById('components-list').innerHTML = '<tr><td colspan="6"><div class="alert alert-error">Error loading components</div></td></tr>';
            }
        }
        
        async function loadLatestReadings() {
            try {
                const response = await fetch(API_BASE + '/sensor-readings');
                const data = await response.json();
                
                let html = '<div style="line-height: 2;">';
                html += '<div><strong style="color: var(--primary);">SpO₂ Level:</strong> <span style="font-size: 2em; color: var(--primary); font-weight: 900;">' + (data.spo2 || '--') + '%</span></div>';
                html += '<div><strong style="color: var(--secondary);">Heart Rate:</strong> <span style="font-size: 1.8em; color: var(--secondary); font-weight: 900;">' + (data.heart_rate || '--') + '</span> <span style="font-size: 0.9em;">BPM</span></div>';
                html += '<div style="margin-top: 15px; font-size: 0.9em; color: var(--gray-700);"><strong>Timestamp:</strong> ' + new Date(data.timestamp).toLocaleString() + '</div>';
                html += '</div>';
                
                document.getElementById('latest-readings').innerHTML = html;
            } catch (error) {
                document.getElementById('latest-readings').innerHTML = '<div class="alert alert-error">Error loading readings</div>';
            }
        }
        
        async function loadAlerts() {
            try {
                const response = await fetch(API_BASE + '/dashboard');
                const data = await response.json();
                
                let html = '';
                if (data.alerts && data.alerts.length > 0) {
                    data.alerts.forEach(alert => {
                        const sClass = 'alert alert-' + (alert.severity || 'info');
                        html += '<div class="' + sClass + '">';
                        html += '<div style="font-weight: 700; margin-bottom: 4px;">' + alert.message + '</div>';
                        html += '<div style="font-size: 0.85em; opacity: 0.8;">' + new Date(alert.timestamp).toLocaleString() + '</div>';
                        html += '</div>';
                    });
                } else {
                    html = '<div style="color: var(--gray-700); padding: 20px; text-align: center;">No active alerts currently</div>';
                }
                
                document.getElementById('alerts-list').innerHTML = html;
            } catch (error) {
                document.getElementById('alerts-list').innerHTML = '<div class="alert alert-error">Error loading alerts</div>';
            }
        }
        
        async function addSensorReading() {
            const spo2 = document.getElementById('spo2-input').value;
            const hr = document.getElementById('hr-input').value;
            
            try {
                await fetch(API_BASE + '/sensor-readings', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ spo2: parseFloat(spo2), heart_rate: parseInt(hr) })
                });
                
                document.getElementById('sensor-message').innerHTML = '<div class="alert alert-success">✅ Reading added successfully!</div>';
                loadLatestReadings();
                setTimeout(() => document.getElementById('sensor-message').innerHTML = '', 3000);
            } catch (error) {
                document.getElementById('sensor-message').innerHTML = '<div class="alert alert-error">❌ Error: ' + error.message + '</div>';
            }
        }
        
        async function createAlert() {
            const msg = document.getElementById('alert-message').value;
            const sev = document.getElementById('alert-severity').value;
            
            if (!msg.trim()) {
                document.getElementById('alert-message-box').innerHTML = '<div class="alert alert-error">Please enter a message</div>';
                return;
            }
            
            try {
                await fetch(API_BASE + '/alerts', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: msg, severity: sev })
                });
                
                document.getElementById('alert-message').value = '';
                document.getElementById('alert-message-box').innerHTML = '<div class="alert alert-success">✅ Alert created!</div>';
                loadAlerts();
                setTimeout(() => document.getElementById('alert-message-box').innerHTML = '', 2000);
            } catch (error) {
                document.getElementById('alert-message-box').innerHTML = '<div class="alert alert-error">❌ Error: ' + error.message + '</div>';
            }
        }
        
        async function testCriticalAlert() {
            const spo2 = document.getElementById('test-spo2').value;
            try {
                await fetch(API_BASE + '/sensor-readings', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ spo2: parseFloat(spo2), heart_rate: 85 })
                });
                alert('✅ Critical alert test triggered! Check the Alerts tab.');
                loadAlerts();
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }
        
        async function toggleComponent() {
            const id = document.getElementById('toggle-id').value;
            await toggleComponentId(parseInt(id));
        }
        
        async function toggleComponentId(id) {
            try {
                await fetch(API_BASE + '/components/toggle', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id: id })
                });
                loadComponents();
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }
        
        async function callAPI() {
            const endpoint = document.getElementById('api-endpoint').value || '/api/dashboard';
            
            try {
                const response = await fetch(endpoint);
                const data = await response.json();
                const responseBox = document.getElementById('api-response');
                responseBox.textContent = JSON.stringify(data, null, 2);
                responseBox.style.display = 'block';
            } catch (error) {
                document.getElementById('api-response').textContent = 'Error: ' + error.message;
                document.getElementById('api-response').style.display = 'block';
            }
        }
        
        window.onload = () => {
            loadComponents();
        };
    </script>
</body>
</html>'''
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

def run_server():
    """Start the SkiOx Dashboard server"""
    DashboardHandler.dashboard = SkiOxDashboard(DATABASE)
    
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║   SkiOx Dashboard - Professional Edition Started! 🚀         ║
╚══════════════════════════════════════════════════════════════╝

📊 Access Points:
   🌐 Dashboard: http://127.0.0.1:{PORT}/
   🔐 Admin:     http://127.0.0.1:{PORT}/admin
   
📡 API Base: http://127.0.0.1:{PORT}/api/

🎨 Features:
   ✅ Professional color scheme (accessible to everyone)
   ✅ Real-time monitoring with auto-refresh
   ✅ Component management
   ✅ Sensor data tracking
   ✅ Critical SpO2 alerts (< 94%)
   ✅ Responsive design
   ✅ Dark & light mode compatible

🛑 Stop: Press Ctrl+C

        """)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✅ Server stopped gracefully")
            sys.exit(0)

if __name__ == '__main__':
    run_server()
