from django.contrib import admin
from .models import (
    ComponentStatus, SensorReading, SystemStatus,
    BatteryStatus, Alert, SystemLog
)


@admin.register(ComponentStatus)
class ComponentStatusAdmin(admin.ModelAdmin):
    list_display = ('component_name', 'status', 'is_online', 'last_updated')
    list_filter = ('status', 'is_online', 'last_updated')
    readonly_fields = ('created_at', 'last_updated')
    search_fields = ('component_name',)


@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ('spo2_level', 'heart_rate', 'is_normal', 'sensor_quality', 'timestamp')
    list_filter = ('is_normal', 'timestamp')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)


@admin.register(SystemStatus)
class SystemStatusAdmin(admin.ModelAdmin):
    list_display = ('system_state', 'is_active', 'oxygen_delivery_active', 'last_updated')
    list_filter = ('system_state', 'is_active', 'oxygen_delivery_active')
    readonly_fields = ('created_at', 'last_updated')
    ordering = ('-last_updated',)


@admin.register(BatteryStatus)
class BatteryStatusAdmin(admin.ModelAdmin):
    list_display = ('battery_percentage', 'voltage', 'charging', 'health', 'last_updated')
    list_filter = ('charging', 'health', 'last_updated')
    readonly_fields = ('created_at', 'last_updated')
    ordering = ('-last_updated',)


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('alert_type', 'title', 'is_resolved', 'created_at')
    list_filter = ('alert_type', 'is_resolved', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'resolved_at')
    ordering = ('-created_at',)


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ('log_level', 'component', 'message', 'timestamp')
    list_filter = ('log_level', 'component', 'timestamp')
    search_fields = ('message', 'component')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
