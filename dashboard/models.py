from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class ComponentStatus(models.Model):
    """Model to track status of SkiOx system components"""
    
    COMPONENT_CHOICES = [
        ('ESP32', 'ESP32 Dev Board'),
        ('SPO2_SENSOR', 'SpO2 Sensor (MAX30102)'),
        ('RELAY', 'Relay Module'),
        ('SOLENOID', 'Solenoid Valve'),
        ('BATTERY', 'Li-Ion Battery'),
        ('TP4056', 'TP4056 Charging Module'),
        ('MT3608', 'MT3608 Boost Converter'),
        ('LDO', 'AMS1117-3.3 LDO'),
        ('OLED', 'OLED Display (Optional)'),
        ('BUZZER', 'Active Buzzer (Optional)'),
        ('LED', 'Red LED (Optional)'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('ERROR', 'Error'),
        ('WARNING', 'Warning'),
        ('MAINTENANCE', 'Maintenance'),
    ]
    
    component_name = models.CharField(max_length=50, choices=COMPONENT_CHOICES, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='INACTIVE')
    is_online = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-last_updated']
        verbose_name = 'Component Status'
        verbose_name_plural = 'Component Statuses'
    
    def __str__(self):
        return f"{self.get_component_name_display()} - {self.status}"


class SensorReading(models.Model):
    """Model to store SpO2 and HR sensor readings"""
    
    spo2_level = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="SpO2 percentage (0-100%)"
    )
    heart_rate = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(300)],
        help_text="Heart Rate in BPM"
    )
    is_normal = models.BooleanField(default=True, help_text="Is reading within normal range?")
    sensor_quality = models.IntegerField(
        default=100,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Signal quality percentage"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Sensor Reading'
        verbose_name_plural = 'Sensor Readings'
    
    def __str__(self):
        return f"SpO2: {self.spo2_level}%, HR: {self.heart_rate} BPM - {self.timestamp}"


class SystemStatus(models.Model):
    """Model to track overall system status"""
    
    SYSTEM_STATE_CHOICES = [
        ('IDLE', 'Idle'),
        ('MONITORING', 'Monitoring'),
        ('DELIVERING', 'Delivering Oxygen'),
        ('ERROR', 'Error'),
        ('SHUTDOWN', 'Shutdown'),
    ]
    
    is_active = models.BooleanField(default=False)
    system_state = models.CharField(max_length=20, choices=SYSTEM_STATE_CHOICES, default='IDLE')
    oxygen_valve_open = models.BooleanField(default=False, help_text="Is solenoid valve open?")
    relay_engaged = models.BooleanField(default=False, help_text="Is relay module engaged?")
    oxygen_delivery_active = models.BooleanField(default=False)
    system_uptime = models.DurationField(default=timezone.timedelta(0))
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-last_updated']
        verbose_name = 'System Status'
        verbose_name_plural = 'System Statuses'
    
    def __str__(self):
        return f"System Status: {self.system_state}"


class BatteryStatus(models.Model):
    """Model to track battery status"""
    
    battery_percentage = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Battery charge percentage"
    )
    voltage = models.FloatField(default=0, help_text="Battery voltage in volts")
    charging = models.BooleanField(default=False)
    health = models.CharField(
        max_length=20,
        choices=[
            ('GOOD', 'Good'),
            ('FAIR', 'Fair'),
            ('POOR', 'Poor'),
        ],
        default='GOOD'
    )
    charge_cycles = models.IntegerField(default=0, help_text="Number of charge cycles")
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-last_updated']
        verbose_name = 'Battery Status'
        verbose_name_plural = 'Battery Statuses'
    
    def __str__(self):
        return f"Battery: {self.battery_percentage}% - {self.health}"


class Alert(models.Model):
    """Model to track system alerts and warnings"""
    
    ALERT_TYPE_CHOICES = [
        ('CRITICAL', 'Critical'),
        ('WARNING', 'Warning'),
        ('INFO', 'Information'),
    ]
    
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Alert'
        verbose_name_plural = 'Alerts'
    
    def __str__(self):
        return f"{self.alert_type}: {self.title}"


class SystemLog(models.Model):
    """Model to track system activity logs"""
    
    LOG_LEVEL_CHOICES = [
        ('DEBUG', 'Debug'),
        ('INFO', 'Information'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ]
    
    log_level = models.CharField(max_length=20, choices=LOG_LEVEL_CHOICES)
    message = models.TextField()
    component = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'System Log'
        verbose_name_plural = 'System Logs'
    
    def __str__(self):
        return f"[{self.log_level}] {self.component}: {self.message[:50]}"
