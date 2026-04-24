from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API Router
router = DefaultRouter()
router.register(r'components', views.ComponentStatusViewSet, basename='component')
router.register(r'sensors', views.SensorReadingViewSet, basename='sensor')
router.register(r'system', views.SystemStatusViewSet, basename='system')
router.register(r'battery', views.BatteryStatusViewSet, basename='battery')
router.register(r'alerts', views.AlertViewSet, basename='alert')
router.register(r'logs', views.SystemLogViewSet, basename='log')

urlpatterns = [
    # Web Views
    path('', views.DashboardIndexView.as_view(), name='dashboard'),
    path('components/', views.ComponentsView.as_view(), name='components'),
    path('sensor-data/', views.SensorDataView.as_view(), name='sensor-data'),
    path('alerts/', views.AlertsView.as_view(), name='alerts'),
    path('logs/', views.LogsView.as_view(), name='logs'),
    
    # API Endpoints
    path('api/', include(router.urls)),
    path('api/summary/', views.DashboardSummaryView.as_view(), name='api-summary'),
]
