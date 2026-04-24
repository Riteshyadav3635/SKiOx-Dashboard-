cd /Users/anupkumar/Desktop/SkiOx-\ DashBoard
./run.sh# 🚀 SkiOx Dashboard - Quick Start Guide

## Option 1: Using the Run Script (Easiest)
```bash
cd /Users/anupkumar/Desktop/SkiOx-\ DashBoard
./run.sh
```

## Option 2: Direct Python Command
```bash
cd /Users/anupkumar/Desktop/SkiOx-\ DashBoard
python3 app.py
```

## Access the Dashboard
Once running, open your browser to:
```
http://127.0.0.1:8001/
```

## Features
- ✅ **No external dependencies** - Uses only Python standard library
- ✅ **Real-time monitoring** - Dashboard auto-refreshes every 5 seconds
- ✅ **REST API** - Integrate with IoT devices
- ✅ **SQLite database** - Persistent data storage
- ✅ **12 pre-loaded components** - SpO2, Heart Rate, regulators, alarms, etc.
- ✅ **Alert system** - Track system events and warnings
- ✅ **Critical Alerts** - Auto-notify rescue team when SpO2 drops below 94%
- ✅ **Component status management** - Toggle between active/standby

## API Endpoints

### Get Dashboard Data
```bash
curl http://127.0.0.1:8001/api/dashboard
```

### Get All Components
```bash
curl http://127.0.0.1:8001/api/components
```

### Get Latest Sensor Reading
```bash
curl http://127.0.0.1:8001/api/sensor-readings
```

### Add New Sensor Reading
```bash
curl -X POST http://127.0.0.1:8001/api/sensor-readings \
  -H "Content-Type: application/json" \
  -d '{"spo2": 98.5, "heart_rate": 72}'
```

**Note:** SpO2 values below 94% automatically trigger critical alerts to the rescue team.

### Toggle Component Status
```bash
curl -X POST http://127.0.0.1:8001/api/components/toggle \
  -H "Content-Type: application/json" \
  -d '{"id": 1}'
```

### Create Alert
```bash
curl -X POST http://127.0.0.1:8001/api/alerts \
  -H "Content-Type: application/json" \
  -d '{"message": "Test alert", "severity": "warning"}'
```

## Database
- Location: `skiox_data.db`
- Format: SQLite 3
- Auto-initialized on first run
- Contains: Components, Sensor Readings, Alerts, System Status

## Stopping the Server
Press `Ctrl+C` in the terminal

## Troubleshooting

### Port Already in Use
If port 8001 is busy, edit `app.py` and change `PORT = 8001` to another port (e.g., 8002, 8003)

### Permission Denied
```bash
chmod +x app.py run.sh
```

## Backend Components Monitored
1. Oxygen Tank
2. Primary/Backup Regulators
3. Main/Backup Flow Meters
4. Pressure Gauge
5. SpO2 & Heart Rate Monitors
6. Primary/Backup Alarms

## Critical Alert System

When SpO2 drops below 94%, the system automatically:
1. Creates a critical alert with 🚨 indicator
2. Marks alert with "error" severity level
3. Notifies the rescue team immediately
4. Logs historical SpO2 readings for medical review

**Threshold Configuration:** Edit `SPO2_CRITICAL_THRESHOLD` in `app.py` to adjust alert level.

---
**SkiOx Emergency Oxygen Delivery System Dashboard** | Fully Functional | No Installation Required
