#!/usr/bin/env python3
"""
SkiOx Dashboard - Standalone Server
Runs without external dependencies using Python standard library
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
        
        # Create tables
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
        
        # Load sample data if empty
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
        
        # Add sample sensor reading
        now = datetime.now().isoformat()
        cursor.execute(
            'INSERT INTO sensor_readings (timestamp, spo2, heart_rate) VALUES (?, ?, ?)',
            (now, 98.5, 72)
        )
        
        # Add sample alert
        cursor.execute(
            'INSERT INTO alerts (timestamp, message, severity, resolved) VALUES (?, ?, ?, ?)',
            (now, 'System initialized successfully', 'info', 0)
        )
        
        # Add system status
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
        
        # Check if SpO2 is below critical threshold and create alert
        if spo2 is not None and spo2 < self.SPO2_CRITICAL_THRESHOLD:
            # Only alert once per critical event (when transitioning below threshold)
            if self.last_alert_spo2 is None or self.last_alert_spo2 >= self.SPO2_CRITICAL_THRESHOLD:
                alert_msg = f"🚨 CRITICAL: SpO2 level {spo2}% is below safe threshold ({self.SPO2_CRITICAL_THRESHOLD}%) - NOTIFYING RESCUE TEAM"
                cursor.execute(
                    'INSERT INTO alerts (timestamp, message, severity) VALUES (?, ?, ?)',
                    (now, alert_msg, 'error')
                )
            self.last_alert_spo2 = spo2
        else:
            self.last_alert_spo2 = spo2
        
        # Keep only last 1000 readings
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
    """Custom HTTP request handler for SkiOx Dashboard"""
    
    dashboard = None
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)
        
        # API endpoints
        if path == '/api/dashboard':
            self.send_json(self.dashboard.get_dashboard_data())
        
        elif path == '/api/components':
            self.send_json({'components': self.dashboard.get_dashboard_data()['components']})
        
        elif path == '/api/sensor-readings':
            data = self.dashboard.get_dashboard_data()
            self.send_json(data['sensor_readings'])
        
        # Main dashboard HTML
        elif path == '/' or path == '/index.html':
            self.send_html(self.get_dashboard_html())
        
        # Admin page
        elif path == '/admin' or path == '/admin.html':
            self.send_html(self.get_admin_html())
        
        # Static files
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
        """Return dashboard HTML"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SkiOx Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
            color: #e2e8f0;
            min-height: 100vh;
        }
        
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        
        header {
            background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 50%, #0ea5e9 100%);
            color: white;
            padding: 40px 0;
            margin-bottom: 40px;
            text-align: center;
            border-radius: 12px;
            box-shadow: 0 20px 50px rgba(14, 165, 233, 0.3);
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
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
            animation: shine 3s infinite;
        }
        
        @keyframes shine {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            font-weight: 800;
            letter-spacing: -1px;
            position: relative;
            z-index: 1;
        }
        
        header p {
            font-size: 1.2em;
            opacity: 0.95;
            position: relative;
            z-index: 1;
            font-weight: 300;
        }
        
        .nav { 
            display: flex; 
            gap: 15px; 
            margin-bottom: 40px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .nav-btn {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            border: 2px solid transparent;
            padding: 12px 28px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 700;
            font-size: 1em;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
            text-decoration: none;
            display: inline-block;
        }
        
        .nav-btn:hover {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
        }
        
        .nav-btn.admin {
            background: linear-gradient(135deg, #f93a5a 0%, #f5576c 100%);
            box-shadow: 0 4px 15px rgba(249, 58, 90, 0.3);
        }
        
        .nav-btn.admin:hover {
            background: linear-gradient(135deg, #f5576c 0%, #e63050 100%);
            box-shadow: 0 6px 20px rgba(249, 58, 90, 0.4);
        }
        
        .grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); 
            gap: 25px; 
            margin-bottom: 30px; 
        }
        
        .card {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 2px solid #334155;
            border-radius: 12px;
            padding: 28px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #0ea5e9, #06b6d4, #0ea5e9);
        }
        
        .card:hover {
            border-color: #0ea5e9;
            box-shadow: 0 15px 40px rgba(14, 165, 233, 0.2);
            transform: translateY(-5px);
        }
        
        .card h2 {
            font-size: 1.4em;
            margin-bottom: 20px;
            color: #0ea5e9;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .sensor-value {
            font-size: 2.8em;
            font-weight: 800;
            color: #0ea5e9;
            margin: 15px 0;
            letter-spacing: -1px;
        }
        
        .sensor-label {
            color: #94a3b8;
            font-size: 0.95em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .status-badge {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 0.9em;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .status-active {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        }
        
        .status-standby {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: white;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
        }
        
        .status-online {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
        }
        
        .component {
            background: rgba(100, 116, 139, 0.1);
            padding: 16px;
            margin: 12px 0;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border: 1px solid #334155;
            transition: all 0.3s ease;
        }
        
        .component:hover {
            background: rgba(14, 165, 233, 0.1);
            border-color: #0ea5e9;
        }
        
        .component-name {
            font-weight: 700;
            color: #f1f5f9;
            font-size: 1.05em;
        }
        
        .component-type {
            font-size: 0.85em;
            color: #94a3b8;
            margin-top: 4px;
        }
        
        .alert {
            padding: 16px;
            margin: 12px 0;
            border-radius: 8px;
            border-left: 5px solid;
            background-color: rgba(100, 116, 139, 0.1);
            transition: all 0.3s ease;
        }
        
        .alert-info {
            background-color: rgba(14, 165, 233, 0.1);
            border-left-color: #0ea5e9;
            color: #7dd3fc;
        }
        
        .alert-warning {
            background-color: rgba(245, 158, 11, 0.1);
            border-left-color: #f59e0b;
            color: #fcd34d;
        }
        
        .alert-error {
            background-color: rgba(239, 68, 68, 0.1);
            border-left-color: #ef4444;
            color: #fca5a5;
        }
        
        .alert-timestamp {
            font-size: 0.85em;
            opacity: 0.8;
            margin-top: 8px;
        }
        
        .loading {
            text-align: center;
            color: #94a3b8;
            padding: 40px 20px;
            font-size: 1.05em;
        }
        
        footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 30px;
            border-top: 1px solid #334155;
            color: #64748b;
            font-size: 0.95em;
        }
        
        .stat-box {
            background: rgba(14, 165, 233, 0.1);
            padding: 12px 20px;
            border-radius: 8px;
            display: inline-block;
            margin: 8px;
            border: 1px solid #0ea5e9;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏥 SkiOx Dashboard</h1>
            <p>IoT Emergency Oxygen Delivery System Monitor</p>
        </header>
        
        <div class="nav">
            <button class="nav-btn" onclick="window.location.href='/'">📊 Dashboard</button>
            <button class="nav-btn admin" onclick="window.location.href='/admin'">🔐 Admin Panel</button>
        </div>
        
        <div id="content" class="loading">Loading dashboard data...</div>
        <footer>
            <p>SkiOx Emergency Oxygen Delivery System • Last Updated: <span id="last-update">--:--:--</span></p>
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
                document.getElementById('content').innerHTML = '<div class="alert alert-error">✗ Error loading dashboard: ' + error.message + '</div>';
            }
        }
        
        function renderDashboard(data) {
            let html = '<div class="grid">';
            
            // System Status Card
            const status = data.system_status || {};
            html += '<div class="card">';
            html += '<h2>⚙️ System Status</h2>';
            html += '<p><strong>Status:</strong> <span class="status-badge ' + getStatusClass(status.status || 'offline') + '">' + (status.status || 'Offline').toUpperCase() + '</span></p>';
            html += '<p style="margin-top: 10px; color: #94a3b8;"><strong>Uptime:</strong> ' + (status.uptime || 0) + 's</p>';
            html += '<p style="color: #94a3b8;"><strong>Updated:</strong> ' + formatTime(status.last_update) + '</p>';
            html += '</div>';
            
            // Latest Sensor Readings
            const sensor = data.sensor_readings || {};
            html += '<div class="card">';
            html += '<h2>❤️ Vital Signs</h2>';
            html += '<div><span class="sensor-label">SpO₂ Level</span><div class="sensor-value">' + (sensor.spo2 || '--') + '%</div></div>';
            html += '<div style="margin-top: 15px;"><span class="sensor-label">Heart Rate</span><div class="sensor-value">' + (sensor.heart_rate || '--') + ' BPM</div></div>';
            html += '</div>';
            
            // Components Status
            if (data.components && data.components.length > 0) {
                html += '<div class="card" style="grid-column: 1/-1;">';
                html += '<h2>📦 System Components (' + data.components.length + ')</h2>';
                const active = data.components.filter(c => c.status === 'active').length;
                const standby = data.components.filter(c => c.status === 'standby').length;
                html += '<div>';
                html += '<span class="stat-box">✓ Active: ' + active + '</span>';
                html += '<span class="stat-box">◐ Standby: ' + standby + '</span>';
                html += '</div>';
                html += '<div style="margin-top: 20px;">';
                data.components.forEach(comp => {
                    html += '<div class="component">';
                    html += '<div><div class="component-name">' + comp.name + '</div><div class="component-type">' + comp.type + ' • ' + comp.location + '</div></div>';
                    html += '<span class="status-badge ' + getStatusClass(comp.status) + '">' + comp.status.toUpperCase() + '</span>';
                    html += '</div>';
                });
                html += '</div></div>';
            }
            
            // Active Alerts
            if (data.alerts && data.alerts.length > 0) {
                html += '<div class="card" style="grid-column: 1/-1;">';
                html += '<h2>🚨 System Alerts (' + data.alerts.length + ')</h2>';
                data.alerts.forEach(alert => {
                    const alertClass = 'alert alert-' + (alert.severity || 'info');
                    html += '<div class="' + alertClass + '">';
                    html += '<strong>' + alert.message + '</strong>';
                    html += '<div class="alert-timestamp">' + formatTime(alert.timestamp) + '</div>';
                    html += '</div>';
                });
                html += '</div>';
            }
            
            html += '</div>';
            document.getElementById('content').innerHTML = html;
            document.getElementById('last-update').textContent = formatTime(data.timestamp);
        }
        
        // Load dashboard on page load
        loadDashboard();
        
        // Refresh every 5 seconds
        setInterval(loadDashboard, 5000);
    </script>
</body>
</html>'''
    
    def get_admin_html(self):
        """Return admin panel HTML"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SkiOx Admin Panel</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif; background: #1a1a2e; color: #eee; }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        header { background: linear-gradient(135deg, #f93a5a 0%, #f5576c 100%); color: white; padding: 25px 0; margin-bottom: 30px; text-align: center; border-radius: 8px; }
        header h1 { font-size: 2.2em; margin-bottom: 5px; }
        
        .nav { display: flex; gap: 10px; margin-bottom: 20px; }
        .nav-btn { background: #f93a5a; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-weight: 600; }
        .nav-btn:hover { background: #f5576c; }
        .nav-btn.active { background: #f5576c; }
        
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; }
        .panel { background: #16213e; border: 1px solid #333; border-radius: 8px; padding: 20px; }
        .panel h2 { color: #f93a5a; margin-bottom: 15px; font-size: 1.3em; border-bottom: 2px solid #f93a5a; padding-bottom: 10px; }
        
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; color: #bbb; font-size: 0.9em; font-weight: 600; }
        .form-group input, .form-group select { width: 100%; padding: 8px; background: #0f3460; border: 1px solid #333; color: #eee; border-radius: 4px; }
        .form-group input:focus, .form-group select:focus { outline: none; border-color: #f93a5a; }
        
        .btn { background: #f93a5a; color: white; border: none; padding: 10px 16px; border-radius: 4px; cursor: pointer; font-weight: 600; }
        .btn:hover { background: #f5576c; }
        .btn-small { padding: 6px 12px; font-size: 0.85em; }
        .btn-danger { background: #e74c3c; }
        .btn-danger:hover { background: #c0392b; }
        .btn-success { background: #27ae60; }
        .btn-success:hover { background: #229954; }
        
        .table-responsive { overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9em; }
        thead { background: #0f3460; }
        th { padding: 10px; color: #f93a5a; font-weight: 600; border-bottom: 2px solid #f93a5a; }
        td { padding: 10px; border-bottom: 1px solid #333; }
        tr:hover { background: #1a3a5a; }
        
        .badge { display: inline-block; padding: 4px 8px; border-radius: 3px; font-size: 0.8em; font-weight: 600; }
        .badge-active { background: #27ae60; color: white; }
        .badge-standby { background: #f39c12; color: white; }
        .badge-error { background: #e74c3c; color: white; }
        .badge-info { background: #3498db; color: white; }
        
        .alert { padding: 12px; border-radius: 4px; margin-bottom: 10px; }
        .alert-success { background: #27ae60; color: white; }
        .alert-error { background: #e74c3c; color: white; }
        .alert-info { background: #3498db; color: white; }
        
        .loading { text-align: center; color: #888; padding: 20px; }
        .fullwidth { grid-column: 1/-1; }
        
        .footer { margin-top: 30px; text-align: center; color: #666; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔐 SkiOx Admin Panel</h1>
            <p>System Management & Monitoring</p>
        </header>
        
        <div class="nav">
            <button class="nav-btn active" onclick="showTab('components')">Components</button>
            <button class="nav-btn" onclick="showTab('sensors')">Sensor Data</button>
            <button class="nav-btn" onclick="showTab('alerts')">Alerts</button>
            <button class="nav-btn" onclick="showTab('test')">Test Tools</button>
            <button class="nav-btn" onclick="location.href='/'">← Back to Dashboard</button>
        </div>
        
        <div id="content">
            <!-- Components Tab -->
            <div id="tab-components" class="grid">
                <div class="panel fullwidth">
                    <h2>📦 System Components</h2>
                    <div id="components-table" class="table-responsive loading">Loading...</div>
                </div>
            </div>
            
            <!-- Sensors Tab -->
            <div id="tab-sensors" class="grid" style="display:none;">
                <div class="panel">
                    <h2>📊 Add Sensor Reading</h2>
                    <div class="form-group">
                        <label>SpO2 Level (%)</label>
                        <input type="number" id="spo2-input" min="0" max="100" value="98.5" placeholder="0-100">
                    </div>
                    <div class="form-group">
                        <label>Heart Rate (BPM)</label>
                        <input type="number" id="hr-input" min="0" max="200" value="72" placeholder="0-200">
                    </div>
                    <button class="btn" onclick="addSensorReading()">➕ Add Reading</button>
                    <div id="sensor-message"></div>
                </div>
                
                <div class="panel">
                    <h2>📈 Latest Readings</h2>
                    <div id="latest-readings" class="loading">Loading...</div>
                </div>
            </div>
            
            <!-- Alerts Tab -->
            <div id="tab-alerts" class="grid" style="display:none;">
                <div class="panel">
                    <h2>🚨 Create Alert</h2>
                    <div class="form-group">
                        <label>Alert Message</label>
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
                    <div id="alert-message-box"></div>
                </div>
                
                <div class="panel fullwidth">
                    <h2>📋 All Alerts</h2>
                    <div id="alerts-list" class="loading">Loading...</div>
                </div>
            </div>
            
            <!-- Test Tools Tab -->
            <div id="tab-test" class="grid" style="display:none;">
                <div class="panel">
                    <h2>🧪 Test Critical Alert</h2>
                    <p style="color: #888; font-size: 0.9em; margin-bottom: 15px;">SpO2 below 94% triggers rescue team alert</p>
                    <div class="form-group">
                        <label>SpO2 Value</label>
                        <input type="number" id="test-spo2" min="0" max="100" value="92" placeholder="Enter SpO2">
                    </div>
                    <button class="btn btn-danger" onclick="testCriticalAlert()">⚠️ Trigger Critical Alert</button>
                </div>
                
                <div class="panel">
                    <h2>🔄 Toggle Component</h2>
                    <div class="form-group">
                        <label>Component ID</label>
                        <input type="number" id="toggle-id" min="1" value="1" placeholder="Component ID">
                    </div>
                    <button class="btn" onclick="toggleComponent()">🔄 Toggle Status</button>
                </div>
                
                <div class="panel fullwidth">
                    <h2>📡 API Test Console</h2>
                    <div class="form-group">
                        <label>Endpoint</label>
                        <input type="text" id="api-endpoint" value="/api/dashboard" placeholder="/api/...">
                    </div>
                    <button class="btn" onclick="callAPI()">🔗 Call API</button>
                    <pre id="api-response" style="background: #0f3460; padding: 10px; border-radius: 4px; margin-top: 10px; max-height: 300px; overflow-y: auto; display: none;"></pre>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>SkiOx Admin Panel • Real-time System Management</p>
        </div>
    </div>
    
    <script>
        const API_BASE = '/api';
        
        function showTab(tab) {
            // Hide all tabs
            document.querySelectorAll('[id^="tab-"]').forEach(el => el.style.display = 'none');
            // Show selected tab
            document.getElementById('tab-' + tab).style.display = 'grid';
            
            // Update nav buttons
            document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            // Load data for selected tab
            if (tab === 'components') loadComponents();
            if (tab === 'sensors') loadLatestReadings();
            if (tab === 'alerts') loadAlerts();
        }
        
        async function loadComponents() {
            try {
                const response = await fetch(API_BASE + '/components');
                const data = await response.json();
                
                let html = '<table><thead><tr><th>ID</th><th>Component</th><th>Type</th><th>Location</th><th>Status</th><th>Action</th></tr></thead><tbody>';
                
                data.components.forEach(comp => {
                    const statusClass = comp.status === 'active' ? 'badge-active' : 'badge-standby';
                    html += '<tr>';
                    html += '<td>' + comp.id + '</td>';
                    html += '<td>' + comp.name + '</td>';
                    html += '<td>' + comp.type + '</td>';
                    html += '<td>' + comp.location + '</td>';
                    html += '<td><span class="badge ' + statusClass + '">' + comp.status.toUpperCase() + '</span></td>';
                    html += '<td><button class="btn btn-small" onclick="toggleComponentId(' + comp.id + ')">Toggle</button></td>';
                    html += '</tr>';
                });
                
                html += '</tbody></table>';
                document.getElementById('components-table').innerHTML = html;
            } catch (error) {
                document.getElementById('components-table').innerHTML = '<div class="alert alert-error">Error loading components: ' + error.message + '</div>';
            }
        }
        
        async function loadLatestReadings() {
            try {
                const response = await fetch(API_BASE + '/sensor-readings');
                const data = await response.json();
                
                let html = '<div style="color: #888;">';
                html += '<p><strong>SpO2:</strong> ' + (data.spo2 || '--') + '%</p>';
                html += '<p><strong>Heart Rate:</strong> ' + (data.heart_rate || '--') + ' BPM</p>';
                html += '<p><strong>Time:</strong> ' + new Date(data.timestamp).toLocaleString() + '</p>';
                html += '</div>';
                
                document.getElementById('latest-readings').innerHTML = html;
            } catch (error) {
                document.getElementById('latest-readings').innerHTML = 'Error loading readings';
            }
        }
        
        async function loadAlerts() {
            try {
                const response = await fetch(API_BASE + '/dashboard');
                const data = await response.json();
                
                let html = '<div>';
                if (data.alerts && data.alerts.length > 0) {
                    data.alerts.forEach(alert => {
                        const sClass = 'alert alert-' + (alert.severity || 'info');
                        html += '<div class="' + sClass + '" style="margin-bottom: 10px;">';
                        html += '<strong>' + alert.message + '</strong><br>';
                        html += '<small>' + new Date(alert.timestamp).toLocaleString() + '</small>';
                        html += '</div>';
                    });
                } else {
                    html += '<p style="color: #666;">No alerts currently</p>';
                }
                html += '</div>';
                
                document.getElementById('alerts-list').innerHTML = html;
            } catch (error) {
                document.getElementById('alerts-list').innerHTML = 'Error loading alerts';
            }
        }
        
        async function addSensorReading() {
            const spo2 = document.getElementById('spo2-input').value;
            const hr = document.getElementById('hr-input').value;
            
            try {
                const response = await fetch(API_BASE + '/sensor-readings', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ spo2: parseFloat(spo2), heart_rate: parseInt(hr) })
                });
                
                const result = await response.json();
                const msgBox = document.getElementById('sensor-message');
                msgBox.innerHTML = '<div class="alert alert-success">✅ Reading added successfully!</div>';
                setTimeout(() => msgBox.innerHTML = '', 3000);
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
                setTimeout(() => {
                    loadAlerts();
                    document.getElementById('alert-message-box').innerHTML = '';
                }, 2000);
            } catch (error) {
                document.getElementById('alert-message-box').innerHTML = '<div class="alert alert-error">❌ Error: ' + error.message + '</div>';
            }
        }
        
        async function testCriticalAlert() {
            const spo2 = document.getElementById('test-spo2').value;
            await addSensorReadingDirect(parseFloat(spo2), 80);
        }
        
        async function addSensorReadingDirect(spo2, hr) {
            try {
                await fetch(API_BASE + '/sensor-readings', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ spo2: spo2, heart_rate: hr })
                });
                alert('✅ Test alert triggered! Check the alerts section.');
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
        
        // Load components on page load
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
    # Initialize dashboard
    DashboardHandler.dashboard = SkiOxDashboard(DATABASE)
    
    # Create server
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        print(f"""
╔════════════════════════════════════════════════════════════╗
║         SkiOx Dashboard Started Successfully! 🚀           ║
╚════════════════════════════════════════════════════════════╝

📊 Dashboard running at:
   🌐 http://127.0.0.1:{PORT}/
   
📡 API Endpoints:
   GET  /api/dashboard         - Full dashboard data
   GET  /api/components        - List all components
   GET  /api/sensor-readings   - Latest sensor data
   POST /api/sensor-readings   - Add new reading
   POST /api/components/toggle - Toggle component status
   POST /api/alerts            - Create new alert

🛑 Stop server: Press Ctrl+C

        """)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✅ Server stopped gracefully")
            sys.exit(0)

if __name__ == '__main__':
    run_server()
