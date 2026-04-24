from rest_framework import serializers
from .models import (
    ComponentStatus, SensorReading, SystemStatus, 
    BatteryStatus, Alert, SystemLog
)


class ComponentStatusSerializer(serializers.ModelSerializer):
    component_display = serializers.CharField(source='get_component_name_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = ComponentStatus
        fields = ['id', 'component_name', 'component_display', 'status', 'status_display', 
                  'is_online', 'last_updated', 'created_at']
        read_only_fields = ['id', 'created_at', 'last_updated']


class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = ['id', 'spo2_level', 'heart_rate', 'is_normal', 'sensor_quality', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class SystemStatusSerializer(serializers.ModelSerializer):
    system_state_display = serializers.CharField(source='get_system_state_display', read_only=True)
    
    class Meta:
        model = SystemStatus
        fields = ['id', 'is_active', 'system_state', 'system_state_display', 'oxygen_valve_open',
                  'relay_engaged', 'oxygen_delivery_active', 'system_uptime', 'last_updated', 'created_at']
        read_only_fields = ['id', 'created_at', 'last_updated']


class BatteryStatusSerializer(serializers.ModelSerializer):
    health_display = serializers.CharField(source='get_health_display', read_only=True)
    
    class Meta:
        model = BatteryStatus
        fields = ['id', 'battery_percentage', 'voltage', 'charging', 'health', 'health_display',
                  'charge_cycles', 'last_updated', 'created_at']
        read_only_fields = ['id', 'created_at', 'last_updated']


class AlertSerializer(serializers.ModelSerializer):
    alert_type_display = serializers.CharField(source='get_alert_type_display', read_only=True)
    
    class Meta:
        model = Alert
        fields = ['id', 'alert_type', 'alert_type_display', 'title', 'description', 
                  'is_resolved', 'created_at', 'resolved_at']
        read_only_fields = ['id', 'created_at']


class SystemLogSerializer(serializers.ModelSerializer):
    log_level_display = serializers.CharField(source='get_log_level_display', read_only=True)
    
    class Meta:
        model = SystemLog
        fields = ['id', 'log_level', 'log_level_display', 'message', 'component', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class DashboardSummarySerializer(serializers.Serializer):
    """Serializer for dashboard summary data"""
    system_status = SystemStatusSerializer()
    latest_sensor_reading = SensorReadingSerializer()
    battery_status = BatteryStatusSerializer()
    active_alerts_count = serializers.IntegerField()
    active_components = serializers.IntegerField()
