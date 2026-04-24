from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (
    ComponentStatus, SensorReading, SystemStatus,
    BatteryStatus, Alert, SystemLog
)
from .serializers import (
    ComponentStatusSerializer, SensorReadingSerializer, SystemStatusSerializer,
    BatteryStatusSerializer, AlertSerializer, SystemLogSerializer, DashboardSummarySerializer
)


# ========== Web Views ==========

class DashboardIndexView(TemplateView):
    """Main dashboard page"""
    template_name = 'dashboard/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['system_status'] = SystemStatus.objects.last()
        context['battery_status'] = BatteryStatus.objects.last()
        context['latest_sensor'] = SensorReading.objects.first()
        context['active_alerts'] = Alert.objects.filter(is_resolved=False).count()
        context['components'] = ComponentStatus.objects.all()
        return context


class ComponentsView(TemplateView):
    """Components monitoring page"""
    template_name = 'dashboard/components.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['components'] = ComponentStatus.objects.all()
        return context


class SensorDataView(TemplateView):
    """Sensor data monitoring page"""
    template_name = 'dashboard/sensor_data.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_reading'] = SensorReading.objects.first()
        context['readings_count'] = SensorReading.objects.count()
        return context


class AlertsView(ListView):
    """Alerts page"""
    model = Alert
    template_name = 'dashboard/alerts.html'
    context_object_name = 'alerts'
    paginate_by = 25
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unresolved_count'] = Alert.objects.filter(is_resolved=False).count()
        return context


class LogsView(ListView):
    """System logs page"""
    model = SystemLog
    template_name = 'dashboard/logs.html'
    context_object_name = 'logs'
    paginate_by = 50


# ========== API ViewSets ==========

class ComponentStatusViewSet(viewsets.ModelViewSet):
    """API ViewSet for component status management"""
    queryset = ComponentStatus.objects.all()
    serializer_class = ComponentStatusSerializer
    
    @action(detail=False, methods=['get'])
    def active_components(self, request):
        """Get all active components"""
        active = self.queryset.filter(is_online=True, status='ACTIVE')
        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def component_summary(self, request):
        """Get component status summary"""
        summary = {
            'total_components': self.queryset.count(),
            'active': self.queryset.filter(is_online=True, status='ACTIVE').count(),
            'inactive': self.queryset.filter(status='INACTIVE').count(),
            'errors': self.queryset.filter(status='ERROR').count(),
            'warnings': self.queryset.filter(status='WARNING').count(),
        }
        return Response(summary)


class SensorReadingViewSet(viewsets.ModelViewSet):
    """API ViewSet for sensor data"""
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingSerializer
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get latest sensor reading"""
        latest = self.queryset.first()
        serializer = self.get_serializer(latest)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def abnormal_readings(self, request):
        """Get abnormal sensor readings"""
        abnormal = self.queryset.filter(is_normal=False)
        serializer = self.get_serializer(abnormal, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get sensor reading statistics"""
        readings = self.queryset.all()
        if readings.exists():
            avg_spo2 = sum(r.spo2_level for r in readings) / readings.count()
            avg_hr = sum(r.heart_rate for r in readings) / readings.count()
            stats = {
                'total_readings': readings.count(),
                'avg_spo2': round(avg_spo2, 2),
                'avg_heart_rate': round(avg_hr, 2),
                'min_spo2': min(r.spo2_level for r in readings),
                'max_spo2': max(r.spo2_level for r in readings),
                'min_heart_rate': min(r.heart_rate for r in readings),
                'max_heart_rate': max(r.heart_rate for r in readings),
            }
            return Response(stats)
        return Response({'error': 'No readings available'}, status=status.HTTP_404_NOT_FOUND)


class SystemStatusViewSet(viewsets.ModelViewSet):
    """API ViewSet for system status"""
    queryset = SystemStatus.objects.all()
    serializer_class = SystemStatusSerializer
    
    @action(detail=False, methods=['get'])
    def current_status(self, request):
        """Get current system status"""
        current = self.queryset.last()
        if current:
            serializer = self.get_serializer(current)
            return Response(serializer.data)
        return Response({'error': 'No system status available'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def activate_oxygen_delivery(self, request):
        """Activate oxygen delivery"""
        system = self.queryset.last()
        if system:
            system.oxygen_delivery_active = True
            system.oxygen_valve_open = True
            system.relay_engaged = True
            system.system_state = 'DELIVERING'
            system.save()
            return Response({'status': 'Oxygen delivery activated'})
        return Response({'error': 'No system status available'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def deactivate_oxygen_delivery(self, request):
        """Deactivate oxygen delivery"""
        system = self.queryset.last()
        if system:
            system.oxygen_delivery_active = False
            system.oxygen_valve_open = False
            system.relay_engaged = False
            system.system_state = 'MONITORING'
            system.save()
            return Response({'status': 'Oxygen delivery deactivated'})
        return Response({'error': 'No system status available'}, status=status.HTTP_404_NOT_FOUND)


class BatteryStatusViewSet(viewsets.ModelViewSet):
    """API ViewSet for battery status"""
    queryset = BatteryStatus.objects.all()
    serializer_class = BatteryStatusSerializer
    
    @action(detail=False, methods=['get'])
    def current_battery(self, request):
        """Get current battery status"""
        current = self.queryset.last()
        if current:
            serializer = self.get_serializer(current)
            return Response(serializer.data)
        return Response({'error': 'No battery status available'}, status=status.HTTP_404_NOT_FOUND)


class AlertViewSet(viewsets.ModelViewSet):
    """API ViewSet for alerts"""
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    
    @action(detail=False, methods=['get'])
    def unresolved_alerts(self, request):
        """Get unresolved alerts"""
        unresolved = self.queryset.filter(is_resolved=False)
        serializer = self.get_serializer(unresolved, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Mark alert as resolved"""
        alert = self.get_object()
        alert.is_resolved = True
        alert.resolved_at = timezone.now()
        alert.save()
        return Response({'status': 'Alert resolved'})
    
    @action(detail=False, methods=['get'])
    def alert_summary(self, request):
        """Get alert summary"""
        summary = {
            'critical': self.queryset.filter(alert_type='CRITICAL', is_resolved=False).count(),
            'warning': self.queryset.filter(alert_type='WARNING', is_resolved=False).count(),
            'info': self.queryset.filter(alert_type='INFO', is_resolved=False).count(),
            'total_unresolved': self.queryset.filter(is_resolved=False).count(),
        }
        return Response(summary)


class SystemLogViewSet(viewsets.ReadOnlyModelViewSet):
    """API ViewSet for system logs (Read-only)"""
    queryset = SystemLog.objects.all()
    serializer_class = SystemLogSerializer
    
    @action(detail=False, methods=['get'])
    def error_logs(self, request):
        """Get error and critical logs"""
        logs = self.queryset.filter(log_level__in=['ERROR', 'CRITICAL'])
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)


class DashboardSummaryView(APIView):
    """API endpoint for complete dashboard summary"""
    
    def get(self, request):
        """Get dashboard summary data"""
        try:
            system_status = SystemStatus.objects.last()
            latest_reading = SensorReading.objects.first()
            battery_status = BatteryStatus.objects.last()
            active_alerts = Alert.objects.filter(is_resolved=False).count()
            active_components = ComponentStatus.objects.filter(is_online=True).count()
            
            data = {
                'system_status': SystemStatusSerializer(system_status).data if system_status else None,
                'latest_sensor_reading': SensorReadingSerializer(latest_reading).data if latest_reading else None,
                'battery_status': BatteryStatusSerializer(battery_status).data if battery_status else None,
                'active_alerts_count': active_alerts,
                'active_components': active_components,
                'timestamp': timezone.now().isoformat(),
            }
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
