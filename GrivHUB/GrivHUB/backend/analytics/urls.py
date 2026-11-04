from django.urls import path
from backend.analytics import views

urlpatterns = [
    path('overview/', views.analytics_overview_view, name='analytics-overview'),
    path('msedcl-overview/', views.analytics_overview_view, name='msedcl-analytics-overview'),
    path('trends/', views.analytics_trends_view, name='analytics-trends'),
    path('categories/', views.analytics_categories_view, name='analytics-categories'),
    path('status-distribution/', views.analytics_status_view, name='analytics-status'),
    path('departments/', views.analytics_departments_view, name='analytics-departments'),
    path('resolution-times/', views.analytics_resolution_times_view, name='analytics-resolution-times'),
    path('officer-workload/', views.analytics_officer_workload_view, name='analytics-officer-workload'),
    path('reopens/', views.analytics_reopens_view, name='analytics-reopens'),
    path('routing/', views.analytics_routing_view, name='analytics-routing'),
    path('locations/', views.analytics_locations_view, name='analytics-locations'),
    path('ml/overview/', views.analytics_ml_overview_view, name='analytics-ml-overview'),
    path('ml/confusion-matrix/', views.analytics_ml_confusion_view, name='analytics-ml-confusion'),
    path('ml/confidence/', views.analytics_ml_confidence_view, name='analytics-ml-confidence'),
    path('data-quality/', views.analytics_data_quality_view, name='analytics-data-quality'),
    path('export/', views.analytics_export_view, name='analytics-export'),
    path('reports/generate/', views.analytics_report_view, name='analytics-report'),
]
