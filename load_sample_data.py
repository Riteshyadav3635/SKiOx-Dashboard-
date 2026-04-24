"""
Load sample data into the SkiOx Dashboard
Run with: python manage.py shell < load_sample_data.py
"""

from datetime import datetime, timedelta
from django.utils import timezone
from dashboard.models import (
    ComponentStatus, SensorReading, SystemStatus,
    BatteryStatus, Alert, SystemLog
)

print("Loading sample data...")

# Clear existing data (optional)
# ComponentStatus.objects.all().delete()
# SensorReading.objects.all().delete()
# SystemStatus.objects.all().delete()
# BatteryStatus.objects.all().delete()
# Alert.objects.all().delete()
# SystemLog.objects.all().delete()

# Define all components
components = [
    ('ESP32', 'ESP32 Dev Board'),
    ('SPO2_SENSOR', 'SpO2 Sensor (MAX30102)'),
    ('RELAY', 'Relay Module'),
    ('SOLENOID', 'Solenoid Valve'),
    ('BATTERY', 'Li-Ion Battery'),
    ('TP4056', 'TP4056 Charging Module'),
    ('MT3608', 'MT3608 Boost Converter'),
    ('LDO', 'AMS1117-3.3 LDO'),
    ('OLED', 'OLED Display'),
    ('BUZZER', 'Active Buzzer'),
    ('LED', 'Red LED'),
]

# Create components if they don't exist
print("\nCreating components...")
for comp_code, comp_name in components:
    obj, created = ComponentStatus.objects.get_or_create(
        component_name=comp_code,
        defaults={
            'status': 'ACTIVE',
            'is_online': True,
        }
    )
    if created:
        print(f"  Created: {comp_name}")
    else:
        print(f"  Exists: {comp_name}")

# Create system status
print("\nCreating system status...")
system_status, created = SystemStatus.objects.get_or_create(
    id=1,
    defaults={
        'is_active': True,
        'system_state': 'IDLE',
        'oxygen_valve_open': False,
        'relay_engaged': False,
        'oxygen_delivery_active': False,
        'system_uptime': timedelta(hours=2, minutes=30),
    }
)
print(f"  System Status: {'Created' if created else 'Updated'}")

# Create battery status
print("\nCreating battery status...")
battery_status, created = BatteryStatus.objects.get_or_create(
    id=1,
    defaults={
        'battery_percentage': 85,
        'voltage': 4.2,
        'charging': False,
        'health': 'GOOD',
        'charge_cycles': 12,
    }
)
print(f"  Battery Status: {'Created' if created else 'Updated'}")

# Create sample sensor readings
print("\nCreating sensor readings...")
for i in range(10):
    timestamp = timezone.now() - timedelta(minutes=i*5)
    spo2_value = 95 + (i % 5) - 2
    hr_value = 70 + (i % 10) - 5
    
    reading, created = SensorReading.objects.get_or_create(
        timestamp=timestamp,
        defaults={
            'spo2_level': spo2_value,
            'heart_rate': hr_value,
            'is_normal': spo2_value >= 95 and 60 <= hr_value <= 100,
            'sensor_quality': 95 + (i % 5),
        }
    )
    if created:
        print(f"  Reading {i+1}: SpO2={spo2_value}%, HR={hr_value} BPM")

# Create sample alerts
print("\nCreating alerts...")
alerts_data = [
    ('INFO', 'System Initialization', 'SkiOx system initialized successfully'),
    ('INFO', 'Components Online', 'All 11 core components are online'),
    ('WARNING', 'Battery Low', 'Battery level is below 30%'),
    ('CRITICAL', 'Sensor Error', 'SpO2 sensor signal quality low'),
]

for alert_type, title, description in alerts_data:
    alert, created = Alert.objects.get_or_create(
        title=title,
        defaults={
            'alert_type': alert_type,
            'description': description,
            'is_resolved': False,
        }
    )
    if created:
        print(f"  Alert: {alert_type} - {title}")
    else:
        print(f"  Alert exists: {title}")

# Create sample system logs
print("\nCreating system logs...")
logs_data = [
    ('INFO', 'ESP32', 'System started'),
    ('INFO', 'SPO2_SENSOR', 'Sensor calibration completed'),
    ('INFO', 'BATTERY', 'Battery voltage: 4.15V'),
    ('DEBUG', 'RELAY', 'Relay test completed'),
    ('INFO', 'TP4056', 'Charging enabled'),
    ('INFO', 'MT3608', 'Boost converter active'),
    ('DEBUG', 'I2C', 'I2C devices detected'),
    ('INFO', 'SYSTEM', 'All systems operational'),
]

for log_level, component, message in logs_data:
    log, created = SystemLog.objects.get_or_create(
        message=message,
        component=component,
        defaults={
            'log_level': log_level,
        }
    )
    if created:
        print(f"  Log: [{log_level}] {component} - {message}")

print("\n" + "="*50)
print("Sample data loading complete!")
print("="*50)
print("\nSummary:")
print(f"  - Components: {ComponentStatus.objects.count()}")
print(f"  - Sensor Readings: {SensorReading.objects.count()}")
print(f"  - System Status: {SystemStatus.objects.count()}")
print(f"  - Battery Status: {BatteryStatus.objects.count()}")
print(f"  - Alerts: {Alert.objects.count()}")
print(f"  - System Logs: {SystemLog.objects.count()}")
print("\nYou can now access the dashboard at: http://127.0.0.1:8000/")
