# SkiOx Dashboard API Documentation

## Overview

The SkiOx Dashboard provides a comprehensive REST API for all components of the IoT Emergency Oxygen Delivery System. All responses are in JSON format.

## Base URL

```
http://localhost:8000/api/
```

## Authentication

Currently, the API does not require authentication in development mode. For production, implement token-based or session-based authentication.

## Response Format

### Success Response
```json
{
  "id": 1,
  "field1": "value1",
  "field2": "value2"
}
```

### Error Response
```json
{
  "error": "Error message",
  "detail": "Detailed error information"
}
```

---

## Endpoints

### System Status

#### Get Current System Status
```
GET /api/system/current_status/
```

**Response:**
```json
{
  "id": 1,
  "is_active": true,
  "system_state": "MONITORING",
  "system_state_display": "Monitoring",
  "oxygen_valve_open": false,
  "relay_engaged": false,
  "oxygen_delivery_active": false,
  "system_uptime": "02:30:00",
  "last_updated": "2026-04-24T10:30:00Z"
}
```

#### List All System Status Records
```
GET /api/system/
```

#### Create System Status
```
POST /api/system/
```

**Request Body:**
```json
{
  "is_active": true,
  "system_state": "MONITORING",
  "oxygen_valve_open": false,
  "relay_engaged": false,
  "oxygen_delivery_active": false,
  "system_uptime": "02:30:00"
}
```

#### Activate Oxygen Delivery
```
POST /api/system/activate_oxygen_delivery/
```

**Response:**
```json
{
  "status": "Oxygen delivery activated"
}
```

#### Deactivate Oxygen Delivery
```
POST /api/system/deactivate_oxygen_delivery/
```

**Response:**
```json
{
  "status": "Oxygen delivery deactivated"
}
```

---

### Sensor Data

#### Get Latest Sensor Reading
```
GET /api/sensors/latest/
```

**Response:**
```json
{
  "id": 10,
  "spo2_level": 95.5,
  "heart_rate": 72,
  "is_normal": true,
  "sensor_quality": 98,
  "timestamp": "2026-04-24T10:30:00Z"
}
```

#### List All Sensor Readings
```
GET /api/sensors/
```

**Query Parameters:**
- `page`: Pagination (default: 1)
- `limit`: Results per page (default: 20)

**Response:**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/sensors/?page=2",
  "previous": null,
  "results": [
    {
      "id": 10,
      "spo2_level": 95.5,
      "heart_rate": 72,
      "is_normal": true,
      "sensor_quality": 98,
      "timestamp": "2026-04-24T10:30:00Z"
    }
  ]
}
```

#### Create New Sensor Reading
```
POST /api/sensors/
```

**Request Body:**
```json
{
  "spo2_level": 96.0,
  "heart_rate": 75,
  "is_normal": true,
  "sensor_quality": 99
}
```

#### Get Sensor Statistics
```
GET /api/sensors/statistics/
```

**Response:**
```json
{
  "total_readings": 100,
  "avg_spo2": 95.2,
  "avg_heart_rate": 72.5,
  "min_spo2": 92.0,
  "max_spo2": 98.5,
  "min_heart_rate": 60,
  "max_heart_rate": 85
}
```

#### Get Abnormal Readings
```
GET /api/sensors/abnormal_readings/
```

**Response:**
```json
[
  {
    "id": 5,
    "spo2_level": 88.0,
    "heart_rate": 110,
    "is_normal": false,
    "sensor_quality": 70,
    "timestamp": "2026-04-24T09:00:00Z"
  }
]
```

---

### Components

#### List All Components
```
GET /api/components/
```

**Response:**
```json
[
  {
    "id": 1,
    "component_name": "ESP32",
    "component_display": "ESP32 Dev Board",
    "status": "ACTIVE",
    "status_display": "Active",
    "is_online": true,
    "last_updated": "2026-04-24T10:30:00Z"
  }
]
```

#### Get Specific Component
```
GET /api/components/{id}/
```

#### Update Component
```
PATCH /api/components/{id}/
```

**Request Body:**
```json
{
  "status": "ERROR",
  "is_online": false
}
```

#### Get Active Components
```
GET /api/components/active_components/
```

#### Get Component Summary
```
GET /api/components/component_summary/
```

**Response:**
```json
{
  "total_components": 11,
  "active": 10,
  "inactive": 0,
  "errors": 1,
  "warnings": 0
}
```

---

### Battery Status

#### Get Current Battery Status
```
GET /api/battery/current_battery/
```

**Response:**
```json
{
  "id": 1,
  "battery_percentage": 85,
  "voltage": 4.15,
  "charging": false,
  "health": "GOOD",
  "health_display": "Good",
  "charge_cycles": 12,
  "last_updated": "2026-04-24T10:30:00Z"
}
```

#### List Battery Status History
```
GET /api/battery/
```

#### Update Battery Status
```
PATCH /api/battery/{id}/
```

**Request Body:**
```json
{
  "battery_percentage": 80,
  "voltage": 4.10,
  "charging": true,
  "health": "FAIR"
}
```

---

### Alerts

#### List All Alerts
```
GET /api/alerts/
```

**Response:**
```json
[
  {
    "id": 1,
    "alert_type": "WARNING",
    "alert_type_display": "Warning",
    "title": "Battery Low",
    "description": "Battery level is below 30%",
    "is_resolved": false,
    "created_at": "2026-04-24T10:00:00Z",
    "resolved_at": null
  }
]
```

#### Create Alert
```
POST /api/alerts/
```

**Request Body:**
```json
{
  "alert_type": "WARNING",
  "title": "Sensor Error",
  "description": "SpO2 sensor signal quality low",
  "is_resolved": false
}
```

#### Get Unresolved Alerts
```
GET /api/alerts/unresolved_alerts/
```

#### Get Alert Summary
```
GET /api/alerts/alert_summary/
```

**Response:**
```json
{
  "critical": 0,
  "warning": 1,
  "info": 3,
  "total_unresolved": 4
}
```

#### Resolve Alert
```
POST /api/alerts/{id}/resolve/
```

**Response:**
```json
{
  "status": "Alert resolved"
}
```

---

### System Logs

#### List System Logs
```
GET /api/logs/
```

**Response:**
```json
[
  {
    "id": 1,
    "log_level": "INFO",
    "log_level_display": "Information",
    "message": "System started",
    "component": "ESP32",
    "timestamp": "2026-04-24T10:00:00Z"
  }
]
```

#### Get Error Logs
```
GET /api/logs/error_logs/
```

---

### Dashboard Summary

#### Get Complete Dashboard Summary
```
GET /api/summary/
```

**Response:**
```json
{
  "system_status": {
    "id": 1,
    "is_active": true,
    "system_state": "MONITORING",
    "system_state_display": "Monitoring",
    "oxygen_valve_open": false,
    "relay_engaged": false,
    "oxygen_delivery_active": false,
    "system_uptime": "02:30:00",
    "last_updated": "2026-04-24T10:30:00Z"
  },
  "latest_sensor_reading": {
    "id": 10,
    "spo2_level": 95.5,
    "heart_rate": 72,
    "is_normal": true,
    "sensor_quality": 98,
    "timestamp": "2026-04-24T10:30:00Z"
  },
  "battery_status": {
    "id": 1,
    "battery_percentage": 85,
    "voltage": 4.15,
    "charging": false,
    "health": "GOOD",
    "health_display": "Good",
    "charge_cycles": 12,
    "last_updated": "2026-04-24T10:30:00Z"
  },
  "active_alerts_count": 4,
  "active_components": 10,
  "timestamp": "2026-04-24T10:30:00.123456Z"
}
```

---

## Error Codes

| Code | Error | Description |
|------|-------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request parameters |
| 404 | Not Found | Resource not found |
| 500 | Server Error | Internal server error |

---

## Usage Examples

### Python with Requests
```python
import requests

# Base URL
BASE_URL = 'http://localhost:8000/api'

# Get latest sensor reading
response = requests.get(f'{BASE_URL}/sensors/latest/')
reading = response.json()
print(f"SpO2: {reading['spo2_level']}%")

# Create new sensor reading
data = {
    'spo2_level': 96.0,
    'heart_rate': 75,
    'is_normal': True,
    'sensor_quality': 99
}
response = requests.post(f'{BASE_URL}/sensors/', json=data)
print(response.json())

# Get system status
response = requests.get(f'{BASE_URL}/system/current_status/')
status = response.json()
print(f"System: {status['system_state_display']}")

# Activate oxygen delivery
response = requests.post(f'{BASE_URL}/system/activate_oxygen_delivery/')
print(response.json())
```

### JavaScript with Fetch
```javascript
const BASE_URL = 'http://localhost:8000/api';

// Get latest sensor reading
fetch(`${BASE_URL}/sensors/latest/`)
  .then(response => response.json())
  .then(data => {
    console.log(`SpO2: ${data.spo2_level}%`);
    console.log(`HR: ${data.heart_rate} BPM`);
  });

// Create new sensor reading
const data = {
  spo2_level: 96.0,
  heart_rate: 75,
  is_normal: true,
  sensor_quality: 99
};

fetch(`${BASE_URL}/sensors/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data)
})
.then(response => response.json())
.then(data => console.log(data));
```

### cURL
```bash
# Get latest reading
curl http://localhost:8000/api/sensors/latest/

# Get system status
curl http://localhost:8000/api/system/current_status/

# Get sensor statistics
curl http://localhost:8000/api/sensors/statistics/

# Create new reading
curl -X POST http://localhost:8000/api/sensors/ \
  -H "Content-Type: application/json" \
  -d '{"spo2_level": 96.0, "heart_rate": 75, "is_normal": true, "sensor_quality": 99}'
```

---

## Rate Limiting

In production, implement rate limiting:
- 100 requests per hour per IP
- 10 requests per second for bulk operations

---

## Pagination

For endpoints that return lists, pagination is supported via query parameters:

```
GET /api/sensors/?page=2&limit=20
```

Default: page=1, limit=20

---

## Filtering

Supported filters (when applicable):
- `status`: Filter by status
- `alert_type`: Filter by alert type
- `log_level`: Filter by log level
- `component`: Filter by component

Example:
```
GET /api/components/?status=ACTIVE
```

---

## Version Information

- **API Version**: 1.0
- **Django Version**: 5.0+
- **DRF Version**: 3.14+
- **Last Updated**: April 2026

---

## Support

For API issues or questions, refer to the main README.md or consult the Django REST Framework documentation.
