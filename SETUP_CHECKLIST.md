# SkiOx Dashboard - Setup Checklist

## Pre-Setup ✓

- [ ] Python 3.8+ installed
- [ ] pip installed
- [ ] git installed (for version control)
- [ ] Terminal/Command prompt ready
- [ ] Navigate to `/Users/anupkumar/Desktop/SkiOx-DashBoard/skiox_dashboard`

## Installation ✓

- [ ] Install pip dependencies: `pip install -r requirements.txt`
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate virtual environment:
  - **Mac/Linux**: `source venv/bin/activate`
  - **Windows**: `venv\Scripts\activate`

## Database Setup ✓

- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
  - Enter username
  - Enter email
  - Enter password (twice)

## Sample Data ✓

- [ ] Load sample data: `python manage.py shell < load_sample_data.py`
- [ ] Verify data in admin: http://127.0.0.1:8000/admin/

## Server Launch ✓

- [ ] Start development server: `python manage.py runserver`
- [ ] Verify message: "Starting development server at http://127.0.0.1:8000/"
- [ ] Check for any errors in terminal

## Access Points ✓

- [ ] Dashboard: http://127.0.0.1:8000/ ✓
- [ ] Admin Panel: http://127.0.0.1:8000/admin/ ✓
- [ ] API Documentation: http://127.0.0.1:8000/api/ ✓
- [ ] Components: http://127.0.0.1:8000/components/ ✓
- [ ] Sensor Data: http://127.0.0.1:8000/sensor-data/ ✓
- [ ] Alerts: http://127.0.0.1:8000/alerts/ ✓
- [ ] Logs: http://127.0.0.1:8000/logs/ ✓

## Dashboard Features ✓

### Main Dashboard Page
- [ ] System status card displays
- [ ] SpO2 level shows
- [ ] Heart rate shows
- [ ] Active alerts count displays
- [ ] Battery status shows progress bar
- [ ] Components table loads
- [ ] Oxygen delivery buttons present
- [ ] Real-time refresh working

### Components Page
- [ ] Component list loads
- [ ] Summary cards display counts
- [ ] Online/offline indicators work
- [ ] View details modal opens
- [ ] Component specs display

### Sensor Data Page
- [ ] Latest readings display
- [ ] Signal quality shows
- [ ] Charts load (if enabled)
- [ ] Statistics calculate
- [ ] Reading history table loads

### Alerts Page
- [ ] Alert summary counts display
- [ ] Unresolved alerts list
- [ ] Alert type filtering works
- [ ] Alert resolution button works
- [ ] Alert details modal opens

### Logs Page
- [ ] System logs display
- [ ] Log levels filter
- [ ] Component filter works
- [ ] Pagination displays

## API Testing ✓

### Test Endpoints
- [ ] GET /api/sensors/latest/ - Returns sensor data
- [ ] GET /api/system/current_status/ - Returns system status
- [ ] GET /api/battery/current_battery/ - Returns battery info
- [ ] GET /api/components/ - Returns components list
- [ ] GET /api/alerts/unresolved_alerts/ - Returns unresolved alerts
- [ ] GET /api/summary/ - Returns complete summary

### Test Commands
```bash
# Test in terminal
curl http://127.0.0.1:8000/api/sensors/latest/
curl http://127.0.0.1:8000/api/system/current_status/
curl http://127.0.0.1:8000/api/battery/current_battery/
```

- [ ] All curl commands return valid JSON
- [ ] No errors in terminal

## Admin Panel ✓

### Login
- [ ] Access /admin/ page
- [ ] Login with superuser credentials
- [ ] Dashboard displays

### Data Management
- [ ] View ComponentStatus
- [ ] View SensorReading
- [ ] View SystemStatus
- [ ] View BatteryStatus
- [ ] View Alert
- [ ] View SystemLog

### Create Records
- [ ] Add new component
- [ ] Add new sensor reading
- [ ] Add new alert
- [ ] Add new system log

## Browser Compatibility ✓

- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari
- [ ] Edge

## File Verification ✓

### Core Files
- [ ] manage.py exists
- [ ] config/settings.py exists
- [ ] config/urls.py exists
- [ ] dashboard/models.py exists
- [ ] dashboard/views.py exists
- [ ] dashboard/serializers.py exists

### Templates
- [ ] base.html exists
- [ ] index.html exists
- [ ] components.html exists
- [ ] sensor_data.html exists
- [ ] alerts.html exists
- [ ] logs.html exists

### Static Files
- [ ] style.css exists
- [ ] main.js exists

### Documentation
- [ ] README.md readable
- [ ] QUICK_START.md readable
- [ ] API_DOCUMENTATION.md readable
- [ ] TESTING_GUIDE.md readable

## Configuration ✓

### Django Settings
- [ ] DEBUG = True (development)
- [ ] SECRET_KEY is set
- [ ] ALLOWED_HOSTS configured
- [ ] INSTALLED_APPS includes 'dashboard'
- [ ] Database configured

### Static Files
- [ ] STATIC_URL = '/static/'
- [ ] MEDIA_URL = '/media/'

## Performance ✓

### Page Load Time
- [ ] Dashboard loads in < 2 seconds
- [ ] API responses in < 500ms
- [ ] Charts render smoothly

### Real-Time Updates
- [ ] Auto-refresh working every 5-10 seconds
- [ ] Browser console shows no errors

## Security Checklist ✓

### CSRF Protection
- [ ] Forms include CSRF token
- [ ] Token validation working

### User Authentication
- [ ] Admin requires login
- [ ] Session expires properly

### Data Validation
- [ ] Invalid inputs rejected
- [ ] Error messages display appropriately

### SQL Injection
- [ ] All queries parameterized
- [ ] Django ORM used throughout

## Optional Enhancements ✓

- [ ] Enable Django Debug Toolbar
- [ ] Add authentication to API
- [ ] Configure database logging
- [ ] Set up email alerts
- [ ] Add WebSocket for live updates
- [ ] Implement data export (CSV/JSON)
- [ ] Add chart animations
- [ ] Create data backup task

## Troubleshooting ✓

If any issues:
- [ ] Check terminal error messages
- [ ] Review browser console (F12)
- [ ] Check Django logs
- [ ] Verify all dependencies installed: `pip list`
- [ ] Review documentation
- [ ] Check requirements.txt matches installed packages

## Final Verification ✓

- [ ] No errors in terminal
- [ ] No errors in browser console (F12)
- [ ] All pages accessible
- [ ] All API endpoints working
- [ ] Admin panel functional
- [ ] Sample data visible
- [ ] Real-time updates working
- [ ] Responsive design working
- [ ] Project files organized
- [ ] Documentation complete

## Ready for Development! ✓

### Start Developing
- [ ] Review codebase structure
- [ ] Read README.md for architecture
- [ ] Check API_DOCUMENTATION.md for endpoints
- [ ] Start modifying as needed

### Next Steps
1. Integrate with ESP32
2. Configure production settings
3. Add more components
4. Extend with custom features
5. Deploy to production

## Deactivate Virtual Environment

When done:
```bash
deactivate
```

---

## Quick Command Reference

```bash
# Activate environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Run server
python manage.py runserver

# Access points
http://127.0.0.1:8000/             # Dashboard
http://127.0.0.1:8000/admin/       # Admin panel
http://127.0.0.1:8000/api/         # API

# Load sample data
python manage.py shell < load_sample_data.py

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Deactivate environment
deactivate
```

---

## Documentation References

- **README.md** - Full project documentation
- **QUICK_START.md** - Quick setup guide
- **API_DOCUMENTATION.md** - API endpoints
- **TESTING_GUIDE.md** - Testing procedures
- **PROJECT_SUMMARY.md** - Project structure

---

**Status**: ✅ COMPLETE

All files created and project ready for development!

**Date**: April 24, 2026  
**Version**: 1.0.0
