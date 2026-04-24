# SkiOx Dashboard - Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies
```bash
cd skiox_dashboard
pip install -r requirements.txt
```

### Step 2: Setup Database
```bash
python manage.py migrate
python manage.py createsuperuser  # Create admin account
```

### Step 3: Load Sample Data
```bash
python manage.py shell < load_sample_data.py
```

### Step 4: Run Server
```bash
python manage.py runserver
```

### Step 5: Access Dashboard
Open your browser and go to:
- **Dashboard**: http://127.0.0.1:8000/
- **Admin**: http://127.0.0.1:8000/admin/
- **API**: http://127.0.0.1:8000/api/

---

## Dashboard Pages

### 1. **Dashboard (Home)**
Main overview with:
- System status
- SpO2 and heart rate readings
- Battery status with progress bar
- Component status table
- Real-time control buttons

**URL**: `/`

### 2. **Components**
Detailed component management:
- Component summary cards
- Full component list
- Online/offline status
- Component categories

**URL**: `/components/`

### 3. **Sensor Data**
Sensor monitoring and analytics:
- Latest readings display
- SpO2 and HR charts
- Statistical analysis
- Reading history

**URL**: `/sensor-data/`

### 4. **Alerts**
Alert management system:
- Alert summary
- Unresolved alerts count
- Type filtering
- Alert resolution

**URL**: `/alerts/`

### 5. **Logs**
System activity logs:
- Log filtering by level
- Component-wise logs
- Error tracking
- Log statistics

**URL**: `/logs/`

---

## Key Features

### Real-Time Updates
- Auto-refresh every 5-10 seconds
- Live component status
- Sensor data streaming
- Alert notifications

### System Control
- Activate/deactivate oxygen delivery
- Control solenoid valve
- Manage relay module
- Monitor power delivery

### Analytics
- SpO2 trends
- Heart rate analysis
- Battery health metrics
- System uptime tracking

### REST API
Complete API for integration with ESP32:
- GET sensor readings
- POST new data
- UPDATE system status
- DELETE old records

---

## Component Specifications

### Core Components
| Component | Model | Qty |
|-----------|-------|-----|
| ESP32 Dev Board | ESP32-WROOM-32 | 1 |
| SpO2 Sensor | MAX30102 | 1 |
| Relay Module | 5V Single Channel | 1 |
| Solenoid Valve | 12V NC 1/4" | 1 |
| Li-Ion Battery | 3.7V 2600mAh | 1 |

### Power Management
| Component | Spec | Qty |
|-----------|------|-----|
| TP4056 Module | 2-chip version | 1 |
| MT3608 Boost | 3.7V to 12V | 1 |
| AMS1117-3.3 | 3.3V Regulator | 1 |

---

## Database Schema

### Component Status Table
```
- component_name (CharField)
- status (ACTIVE, INACTIVE, ERROR, WARNING, MAINTENANCE)
- is_online (Boolean)
- last_updated (DateTime)
- created_at (DateTime)
```

### Sensor Reading Table
```
- spo2_level (Float: 0-100%)
- heart_rate (Integer: BPM)
- is_normal (Boolean)
- sensor_quality (Integer: 0-100%)
- timestamp (DateTime)
```

### System Status Table
```
- is_active (Boolean)
- system_state (IDLE, MONITORING, DELIVERING, ERROR, SHUTDOWN)
- oxygen_valve_open (Boolean)
- relay_engaged (Boolean)
- oxygen_delivery_active (Boolean)
- system_uptime (Duration)
- last_updated (DateTime)
```

### Battery Status Table
```
- battery_percentage (Integer: 0-100%)
- voltage (Float)
- charging (Boolean)
- health (GOOD, FAIR, POOR)
- charge_cycles (Integer)
- last_updated (DateTime)
```

### Alert Table
```
- alert_type (CRITICAL, WARNING, INFO)
- title (CharField)
- description (TextField)
- is_resolved (Boolean)
- created_at (DateTime)
- resolved_at (DateTime, nullable)
```

### System Log Table
```
- log_level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- message (TextField)
- component (CharField)
- timestamp (DateTime)
```

---

## API Usage Examples

### Get Latest Sensor Reading
```bash
curl http://127.0.0.1:8000/api/sensors/latest/
```

### Response
```json
{
  "id": 1,
  "spo2_level": 95.5,
  "heart_rate": 72,
  "is_normal": true,
  "sensor_quality": 98,
  "timestamp": "2026-04-24T10:30:00Z"
}
```

### Create New Reading
```bash
curl -X POST http://127.0.0.1:8000/api/sensors/ \
  -H "Content-Type: application/json" \
  -d '{
    "spo2_level": 96.0,
    "heart_rate": 75,
    "is_normal": true,
    "sensor_quality": 99
  }'
```

### Get System Status
```bash
curl http://127.0.0.1:8000/api/system/current_status/
```

### Activate Oxygen Delivery
```bash
curl -X POST http://127.0.0.1:8000/api/system/activate_oxygen_delivery/ \
  -H "X-CSRFToken: <csrf-token>"
```

### Get Dashboard Summary
```bash
curl http://127.0.0.1:8000/api/summary/
```

---

## Troubleshooting

### Module Not Found Error
```bash
pip install -r requirements.txt --upgrade
```

### Port 8000 Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
# Or use different port
python manage.py runserver 8001
```

### Database Locked
```bash
python manage.py flush
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

---

## Development Tips

### Enable Auto-reload
The development server automatically reloads when you modify Python files.

### Debug Mode
Check `DEBUG = True` in `config/settings.py` for detailed error pages.

### Database Shell
```bash
python manage.py dbshell
```

### Python Shell with Django
```bash
python manage.py shell
# Then:
from dashboard.models import *
ComponentStatus.objects.all()
```

---

## Production Checklist

- [ ] Set `DEBUG = False`
- [ ] Change `SECRET_KEY`
- [ ] Update `ALLOWED_HOSTS`
- [ ] Use production database (PostgreSQL)
- [ ] Configure email settings
- [ ] Set up HTTPS
- [ ] Use Gunicorn or uWSGI
- [ ] Configure static file serving
- [ ] Set up error logging
- [ ] Configure backup strategy

---

## File Locations

```
skiox_dashboard/
├── manage.py                    # Django management
├── requirements.txt             # Dependencies
├── README.md                    # Full documentation
├── QUICK_START.md              # This file
├── load_sample_data.py         # Sample data loader
├── setup.sh                    # Auto-setup script
├── config/
│   └── settings.py             # Main settings
└── dashboard/
    ├── models.py               # Database models
    ├── views.py                # Views & APIs
    ├── urls.py                 # URL routing
    ├── admin.py                # Admin config
    ├── templates/dashboard/    # HTML templates
    └── static/                 # CSS & JS files
```

---

## Support & Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **Bootstrap Documentation**: https://getbootstrap.com/docs/
- **Chart.js Documentation**: https://www.chartjs.org/

---

## Important Notes

⚠️ **Critical Component Notes**:
- Use **MAX30102** (NOT MAX30100)
- **1N4007 diode** is CRITICAL for solenoid protection
- **TP4056 must be 2-chip** version with protection
- Always verify component compatibility

---

**Last Updated**: April 2026  
**Version**: 1.0.0
