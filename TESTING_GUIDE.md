# SkiOx Dashboard - Testing Guide

## Unit Testing

### Run All Tests
```bash
python manage.py test
```

### Run Specific App Tests
```bash
python manage.py test dashboard
```

### Run with Verbose Output
```bash
python manage.py test --verbosity=2
```

### Test Coverage
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

---

## Manual Testing Checklist

### Dashboard Page Testing
- [ ] Load dashboard home page
- [ ] Verify all cards display correctly
- [ ] Check system status updates
- [ ] Test battery status display
- [ ] Verify components table loads
- [ ] Test component details modal
- [ ] Check oxygen delivery buttons
- [ ] Verify real-time updates

### Component Management Testing
- [ ] Load components page
- [ ] Verify component summary cards
- [ ] Test component list display
- [ ] Check online/offline status indicators
- [ ] Test refresh button
- [ ] Verify component details modal
- [ ] Test status filtering

### Sensor Data Testing
- [ ] Load sensor data page
- [ ] Verify latest reading cards
- [ ] Check chart displays
- [ ] Test statistics calculation
- [ ] Verify reading history table
- [ ] Check pagination
- [ ] Test auto-refresh

### Alerts Testing
- [ ] Load alerts page
- [ ] Verify alert summary counts
- [ ] Test alert type filtering
- [ ] Check status filtering
- [ ] Test view alert modal
- [ ] Verify alert resolution
- [ ] Check unresolved badge

### Logs Testing
- [ ] Load logs page
- [ ] Verify log display
- [ ] Test log level filtering
- [ ] Check component filtering
- [ ] Test search functionality
- [ ] Verify pagination

---

## API Testing

### Test Data Creation
```bash
# Load sample data
python manage.py shell < load_sample_data.py
```

### Test Endpoints with cURL

#### Component Endpoints
```bash
# List all components
curl http://localhost:8000/api/components/

# Get component summary
curl http://localhost:8000/api/components/component_summary/

# Get active components
curl http://localhost:8000/api/components/active_components/
```

#### Sensor Endpoints
```bash
# Get latest reading
curl http://localhost:8000/api/sensors/latest/

# Get statistics
curl http://localhost:8000/api/sensors/statistics/

# Get abnormal readings
curl http://localhost:8000/api/sensors/abnormal_readings/

# Create new reading
curl -X POST http://localhost:8000/api/sensors/ \
  -H "Content-Type: application/json" \
  -d '{"spo2_level": 95.5, "heart_rate": 72, "is_normal": true, "sensor_quality": 98}'
```

#### System Status Endpoints
```bash
# Get current status
curl http://localhost:8000/api/system/current_status/

# Activate oxygen delivery
curl -X POST http://localhost:8000/api/system/activate_oxygen_delivery/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: <csrf-token>"

# Deactivate oxygen delivery
curl -X POST http://localhost:8000/api/system/deactivate_oxygen_delivery/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: <csrf-token>"
```

#### Battery Endpoints
```bash
# Get current battery status
curl http://localhost:8000/api/battery/current_battery/
```

#### Alert Endpoints
```bash
# Get unresolved alerts
curl http://localhost:8000/api/alerts/unresolved_alerts/

# Get alert summary
curl http://localhost:8000/api/alerts/alert_summary/

# Resolve alert
curl -X POST http://localhost:8000/api/alerts/1/resolve/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: <csrf-token>"
```

#### System Log Endpoints
```bash
# Get error logs
curl http://localhost:8000/api/logs/error_logs/
```

#### Dashboard Summary
```bash
# Get complete summary
curl http://localhost:8000/api/summary/
```

---

## Browser Testing

### Chrome DevTools
1. Open DevTools (F12)
2. Check Console for errors
3. Check Network tab for API calls
4. Use Lighthouse for performance

### Firefox Developer Tools
1. Open DevTools (F12)
2. Monitor Network requests
3. Check Storage for session data
4. Use Performance profiling

---

## Load Testing

### Using Apache Bench
```bash
# Test dashboard page
ab -n 1000 -c 10 http://localhost:8000/

# Test API endpoint
ab -n 1000 -c 10 http://localhost:8000/api/sensors/latest/
```

### Using Locust
```bash
pip install locust
# Create locustfile.py and run tests
```

---

## Security Testing

### Check for Common Vulnerabilities
```bash
# Check dependencies for known vulnerabilities
pip install safety
safety check

# Django security check
python manage.py check --deploy
```

### SQL Injection Testing
- Test all filter inputs
- Verify parameterized queries are used
- Check admin panel security

### XSS Testing
- Test with malicious input in forms
- Verify HTML escaping in templates
- Check API responses

### CSRF Protection
- Verify CSRF tokens in forms
- Test with invalid/missing tokens
- Check API CSRF token handling

---

## Performance Testing

### Page Load Times
1. Open DevTools
2. Go to Network tab
3. Check Time to First Byte (TTFB)
4. Monitor Total Page Load Time

### Database Query Optimization
```bash
python manage.py shell
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as context:
    # Run queries
    pass

print(f"Number of queries: {len(context)}")
for query in context:
    print(query['sql'])
```

### Memory Usage
```bash
pip install memory-profiler
python -m memory_profiler manage.py runserver
```

---

## Integration Testing

### Test End-to-End Flow
1. Create sensor reading via API
2. Verify reading displays on dashboard
3. Create alert for abnormal reading
4. Verify alert appears on alerts page
5. Resolve alert via API
6. Verify resolution status updates

### Test Data Flow
1. ESP32 simulates sensor reading
2. POST to API endpoint
3. Data stored in database
4. Dashboard fetches and displays
5. Real-time updates trigger

---

## Regression Testing

### Before Making Changes
```bash
python manage.py test
python manage.py check --deploy
```

### After Making Changes
```bash
python manage.py test
# Manual test critical paths
# Run load tests
# Check for security issues
```

---

## Test Data Management

### Generate Random Data
```python
# In Django shell
from dashboard.models import *
from django.utils import timezone
import random

for i in range(100):
    SensorReading.objects.create(
        spo2_level=random.uniform(90, 100),
        heart_rate=random.randint(60, 100),
        is_normal=True,
        sensor_quality=random.randint(80, 100)
    )
```

### Clear Test Data
```bash
python manage.py flush
python manage.py migrate
```

---

## Continuous Integration

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: python manage.py test
```

---

## Debugging

### Django Debug Toolbar
```bash
pip install django-debug-toolbar
# Configure in settings.py
```

### SQL Query Logging
```python
# In settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### Print Debugging
```python
from pprint import pprint
pprint(my_data)
```

---

## Browser Console Testing

### Test API Calls
```javascript
// In browser console
fetch('http://localhost:8000/api/sensors/latest/')
  .then(r => r.json())
  .then(d => console.log(d))

// Or using async/await
const response = await fetch('http://localhost:8000/api/sensors/latest/')
const data = await response.json()
console.log(data)
```

### Test Dashboard Functions
```javascript
// Refresh system status
refreshSystemStatus()

// Load battery status
loadBatteryStatus()

// Refresh components
loadComponentSummary()
```

---

## Test Scenarios

### Normal Operation
- [ ] System starts
- [ ] Components come online
- [ ] Sensor readings stream in
- [ ] Dashboard updates in real-time
- [ ] Battery charges/discharges normally
- [ ] Oxygen delivery activates/deactivates

### Error Scenarios
- [ ] Sensor disconnects
- [ ] Battery critically low
- [ ] Relay fails
- [ ] System timeout
- [ ] Database connection lost

### Edge Cases
- [ ] Very high SpO2 (>100)
- [ ] Very low SpO2 (<80)
- [ ] Extreme heart rates
- [ ] No sensor readings for extended period
- [ ] Rapid status changes

---

## Test Reports

### Create Test Report
```bash
python manage.py test --verbosity=2 > test_report.txt
```

### Coverage Report
```bash
coverage report > coverage_report.txt
```

---

## Performance Benchmarks

### Expected Performance
- Page load: < 1 second
- API response: < 200ms
- Dashboard updates: < 2 seconds
- Database queries: < 100ms

### Monitor Metrics
- Response time
- Error rate
- CPU usage
- Memory usage
- Database load

---

## Version Compatibility

Test with:
- Python 3.8+
- Django 4.2+
- PostgreSQL 12+
- Chrome/Firefox (latest)
- Safari (latest)

---

**Last Updated**: April 2026
