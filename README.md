cd "/Users/anupkumar/Desktop/SkiOx- DashBoard"

# Install & Setup
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py shell < load_sample_data.py

# Run Server
python manage.py runserver

# Access Dashboard
http://127.0.0.1:8000/# SkiOx Dashboard

A comprehensive Django-based monitoring and control dashboard for the **SkiOx IoT Emergency Oxygen Delivery System**. This system tracks all components, sensor readings, battery status, and system health in real-time.

## Features

- **Real-time Monitoring**: Live system status, sensor data, and battery monitoring
- **Component Management**: Track all 26 components from the SkiOx system
- **Sensor Data Visualization**: SpO2 levels and heart rate charts
- **Alert System**: Critical, warning, and informational alerts with resolution tracking
- **System Logs**: Detailed activity logging for debugging and audit trails
- **REST API**: Complete API for data access and system control
- **Responsive Design**: Bootstrap 5 powered responsive UI
- **Admin Panel**: Django admin interface for data management

## Project Structure

```
skiox_dashboard/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── config/                   # Django configuration
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI application
├── dashboard/               # Main app
│   ├── models.py            # Database models
│   ├── views.py             # Views and API endpoints
│   ├── serializers.py       # REST serializers
│   ├── urls.py              # App URL routing
│   ├── admin.py             # Admin interface
│   ├── templates/
│   │   └── dashboard/
│   │       ├── base.html    # Base template
│   │       ├── index.html   # Dashboard home
│   │       ├── components.html
│   │       ├── sensor_data.html
│   │       ├── alerts.html
│   │       └── logs.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── main.js
└── README.md
```

## SkiOx System Components

### Core Components
- **ESP32 Dev Board** - Main microcontroller
- **SpO2 Sensor (MAX30102)** - Blood oxygen level monitoring
- **Relay Module** - System control relay
- **Solenoid Valve** - Oxygen delivery valve
- **Li-Ion Battery** - 3.7V 2600mAh power source

### Power Management
- **TP4056 Module** - Battery charging controller
- **MT3608 Boost Converter** - 3.7V to 12V converter
- **AMS1117-3.3 LDO** - 3.3V voltage regulator

### Optional Components
- **OLED Display** - 0.96" I2C display
- **Active Buzzer** - 5V audio alert
- **Red LED** - Visual indicator

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Guide

1. **Clone the repository**
   ```bash
   cd /Users/anupkumar/Desktop/SkiOx-DashBoard/skiox_dashboard
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create migrations**
   ```bash
   python manage.py makemigrations
   ```

5. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

   The dashboard will be available at: `http://127.0.0.1:8000/`

## Usage

### Web Interface
- **Dashboard (/)**: Main overview page with system status
- **Components (/components/)**: Component management and status
- **Sensor Data (/sensor-data/)**: SpO2 and heart rate monitoring
- **Alerts (/alerts/)**: Alert management and history
- **Logs (/logs/)**: System activity logs
- **Admin (/admin/)**: Django admin interface

### API Endpoints

#### Component Status
```
GET  /api/components/                    # List all components
GET  /api/components/{id}/               # Get specific component
POST /api/components/                    # Create component
GET  /api/components/active_components/  # Get active components
GET  /api/components/component_summary/  # Get summary statistics
```

#### Sensor Data
```
GET  /api/sensors/                       # List all readings
POST /api/sensors/                       # Create reading
GET  /api/sensors/latest/                # Get latest reading
GET  /api/sensors/statistics/            # Get sensor statistics
GET  /api/sensors/abnormal_readings/     # Get abnormal readings
```

#### System Status
```
GET  /api/system/                        # List system status
GET  /api/system/current_status/         # Get current status
POST /api/system/activate_oxygen_delivery/   # Activate oxygen
POST /api/system/deactivate_oxygen_delivery/ # Deactivate oxygen
```

#### Battery Status
```
GET  /api/battery/                       # List battery status
GET  /api/battery/current_battery/       # Get current battery info
```

#### Alerts
```
GET  /api/alerts/                        # List all alerts
POST /api/alerts/                        # Create alert
GET  /api/alerts/unresolved_alerts/      # Get unresolved alerts
POST /api/alerts/{id}/resolve/           # Mark as resolved
GET  /api/alerts/alert_summary/          # Get alert summary
```

#### System Logs
```
GET  /api/logs/                          # List all logs
GET  /api/logs/error_logs/               # Get error/critical logs
```

#### Dashboard Summary
```
GET  /api/summary/                       # Get complete dashboard summary
```

## Database Models

### ComponentStatus
Tracks the status of each SkiOx component
- component_name
- status (ACTIVE, INACTIVE, ERROR, WARNING, MAINTENANCE)
- is_online
- last_updated

### SensorReading
Stores SpO2 and heart rate readings
- spo2_level (0-100%)
- heart_rate (BPM)
- is_normal
- sensor_quality
- timestamp

### SystemStatus
Overall system state
- is_active
- system_state (IDLE, MONITORING, DELIVERING, ERROR, SHUTDOWN)
- oxygen_valve_open
- relay_engaged
- oxygen_delivery_active
- system_uptime

### BatteryStatus
Battery information
- battery_percentage
- voltage
- charging
- health (GOOD, FAIR, POOR)
- charge_cycles

### Alert
System alerts and notifications
- alert_type (CRITICAL, WARNING, INFO)
- title
- description
- is_resolved
- created_at
- resolved_at

### SystemLog
Activity logging
- log_level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- message
- component
- timestamp

## Configuration

### Django Settings
Edit `config/settings.py`:
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Add your domain
- `SECRET_KEY`: Change to a secure random key
- `DATABASES`: Configure your database
- `CORS_ALLOWED_ORIGINS`: Configure CORS for frontend

## API Testing

### Using cURL
```bash
# Get system status
curl http://127.0.0.1:8000/api/system/current_status/

# Get latest sensor reading
curl http://127.0.0.1:8000/api/sensors/latest/

# Get battery status
curl http://127.0.0.1:8000/api/battery/current_battery/
```

### Using Python Requests
```python
import requests

# Get sensor data
response = requests.get('http://127.0.0.1:8000/api/sensors/statistics/')
print(response.json())

# Activate oxygen delivery
response = requests.post(
    'http://127.0.0.1:8000/api/system/activate_oxygen_delivery/',
    headers={'X-CSRFToken': csrf_token}
)
```

## Data Entry Guide

### Adding Sample Data

1. **Via Admin Panel** (`/admin/`)
   - Login with superuser credentials
   - Add components, readings, and alerts

2. **Via API**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/sensors/ \
     -H "Content-Type: application/json" \
     -d '{"spo2_level": 95.5, "heart_rate": 72, "is_normal": true, "sensor_quality": 98}'
   ```

3. **Via Django Shell**
   ```bash
   python manage.py shell
   ```

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

## Production Deployment

1. Set `DEBUG = False` in settings
2. Update `ALLOWED_HOSTS`
3. Update `SECRET_KEY`
4. Configure static file serving
5. Use a production WSGI server (Gunicorn, uWSGI)
6. Set up a database (PostgreSQL recommended)
7. Configure email for alerts
8. Use HTTPS with proper SSL certificates

### Deploy with Gunicorn
```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Database Issues
```bash
# Reset database
python manage.py flush
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

### Module Import Errors
```bash
pip install -r requirements.txt --upgrade
```

## Contributing

When contributing to the SkiOx Dashboard:

1. Create a new branch for your feature
2. Follow PEP 8 style guide
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

## License

This project is part of the NIET BTech CSE-IoT curriculum.

## Project Information

- **Project Name**: SkiOx - IoT Emergency Oxygen Delivery System
- **Institution**: NIET (Noida Institute of Engineering and Technology)
- **Program**: BTech CSE-IoT
- **Student**: Anup Kumar
- **Roll No**: 2301331550025

## Support

For issues, questions, or suggestions:
1. Check the existing documentation
2. Review API endpoint documentation
3. Check Django logs for errors
4. Consult the troubleshooting section

## Notes

- Keep in mind the important notes from the component shopping list
- MAX30102 sensor (NOT MAX30100) is required
- 1N4007 flyback diode is critical for solenoid protection
- TP4056 must be the 2-chip version with protection circuit
- Always verify component compatibility before integration

---

**Last Updated**: April 2026
**Version**: 1.0.0
