import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
from backend.grievances.models import Grievance
from backend.apps.departments.models import Department
from backend.apps.incidents.models import Incident
from backend.apps.feedback.models import MLCorrection
from django.contrib.auth import get_user_model
from .services import get_analytics_service

logger = logging.getLogger("grievancehub.analytics")
User = get_user_model()


def _analytics_params(request):
    return {
        "start_date": request.query_params.get("start_date") or None,
        "end_date": request.query_params.get("end_date") or None,
        "department_id": request.query_params.get("department_id") or None,
        "category": request.query_params.get("category") or None,
        "group_by": request.query_params.get("group_by", "day"),
    }


def _service_response(request, method_name):
    service = get_analytics_service()
    params = _analytics_params(request)
    method = getattr(service, method_name)
    if method_name == "get_grievance_trends":
        result = method(params["group_by"], params["start_date"], params["end_date"], params["department_id"], params["category"])
    elif method_name in {"get_category_distribution", "get_status_distribution"}:
        result = method(params["start_date"], params["end_date"], params["department_id"])
    elif method_name in {"get_department_analytics", "get_routing_analytics", "get_geographic_analytics"}:
        result = method(params["start_date"], params["end_date"])
    elif method_name == "get_officer_workload_analytics":
        result = method(params["department_id"])
    else:
        result = method(params["start_date"], params["end_date"], params["department_id"])
    return Response(result)


@api_view(["GET"])
@permission_classes([AllowAny])
def analytics_trends_view(request):
    return _service_response(request, "get_grievance_trends")


@api_view(["GET"])
@permission_classes([AllowAny])
def analytics_categories_view(request):
    return _service_response(request, "get_category_distribution")


@api_view(["GET"])
@permission_classes([AllowAny])
def analytics_status_view(request):
    return _service_response(request, "get_status_distribution")


@api_view(["GET"])
@permission_classes([AllowAny])
def analytics_departments_view(request):
    return _service_response(request, "get_department_analytics")


@api_view(["GET"])
@permission_classes([AllowAny])
def analytics_resolution_times_view(request):
    return _service_response(request, "get_resolution_time_analytics")


@api_view(["GET"])
@permission_classes([AllowAny])
def analytics_officer_workload_view(request):
    return _service_response(request, "get_officer_workload_analytics")


@api_view(["GET"])
@permission_classes([AllowAny])
def analytics_reopens_view(request):
    return _service_response(request, "get_reopen_analytics")


@api_view(["GET"])
@permission_classes([AllowAny])
def analytics_routing_view(request):
    return _service_response(request, "get_routing_analytics")


@api_view(["GET"])
@permission_classes([AllowAny])
def analytics_locations_view(request):
    return _service_response(request, "get_geographic_analytics")


@api_view(["GET"])
@permission_classes([AllowAny])
def analytics_ml_overview_view(request):
    return Response(get_analytics_service().get_ml_model_monitoring())


@api_view(["GET"])
@permission_classes([AllowAny])
def analytics_ml_confusion_view(request):
    return Response(get_analytics_service().get_ml_confusion_matrix())


@api_view(["GET"])
@permission_classes([AllowAny])
def analytics_ml_confidence_view(request):
    return Response(get_analytics_service().get_ml_confidence_metrics())


@api_view(["GET"])
@permission_classes([AllowAny])
def analytics_data_quality_view(request):
    return Response(get_analytics_service().get_data_quality_audit())


@api_view(["GET"])
@permission_classes([AllowAny])
def analytics_export_view(request):
    csv_data = get_analytics_service().export_grievances_csv(
        request.query_params.get("dataset_type", "grievances"),
        request.query_params.get("start_date"),
        request.query_params.get("end_date"),
        request.query_params.get("department_id"),
    )
    from django.http import HttpResponse
    response = HttpResponse(csv_data, content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="grievancehub-analytics.csv"'
    return response


@api_view(["GET"])
@permission_classes([AllowAny])
def analytics_report_view(request):
    return Response(get_analytics_service().generate_municipal_report(
        request.query_params.get("report_type", "executive"),
        request.query_params.get("start_date"),
        request.query_params.get("end_date"),
    ))

@api_view(['GET'])
@permission_classes([AllowAny])
def analytics_overview_view(request):
    queryset = Grievance.objects.select_related("assigned_department")
    total = queryset.count()
    resolved = Grievance.objects.filter(status=Grievance.Status.RESOLVED).count()
    closed = Grievance.objects.filter(status=Grievance.Status.CLOSED).count()
    in_progress = Grievance.objects.filter(status=Grievance.Status.IN_PROGRESS).count()
    pending = Grievance.objects.filter(status__in=[Grievance.Status.SUBMITTED, Grievance.Status.PENDING_ASSIGNMENT, Grievance.Status.ASSIGNED]).count()
    active = Grievance.objects.filter(status__in=[Grievance.Status.SUBMITTED, Grievance.Status.PENDING_ASSIGNMENT, Grievance.Status.ASSIGNED, Grievance.Status.IN_PROGRESS, Grievance.Status.REOPENED]).count()
    critical = queryset.filter(priority=Grievance.Priority.CRITICAL).count()
    sla_breaches = queryset.filter(
        due_at__lt=timezone.now(),
        status__in=[Grievance.Status.SUBMITTED, Grievance.Status.PENDING_ASSIGNMENT, Grievance.Status.ASSIGNED, Grievance.Status.IN_PROGRESS, Grievance.Status.REOPENED],
    ).count()

    sla_compliance_rate = round((resolved + closed) / max(1, total) * 100, 1)

    # Category distribution
    cat_counts = Grievance.objects.values('predicted_category').annotate(count=Count('id')).order_by('-count')
    category_distribution = {c['predicted_category'] or 'General Consumer Services': c['count'] for c in cat_counts}

    # Priority distribution
    prio_counts = Grievance.objects.values('priority').annotate(count=Count('id'))
    priority_distribution = {p['priority']: p['count'] for p in prio_counts}

    # Incidents count
    incidents_count = Incident.objects.count()
    corrections_count = MLCorrection.objects.count()

    status_counts = {
        row["status"]: row["count"]
        for row in queryset.values("status").annotate(count=Count("id"))
    }
    departments = {}
    for row in queryset.values("assigned_department_id", "assigned_department__code", "assigned_department__name").annotate(total=Count("id")):
        key = str(row["assigned_department_id"]) if row["assigned_department_id"] else "UNASSIGNED"
        departments[key] = {
            "code": row["assigned_department__code"] or "UNASSIGNED",
            "name": row["assigned_department__name"] or "Unassigned MSEDCL Complaints",
            "total": row["total"],
            "active": queryset.filter(assigned_department_id=row["assigned_department_id"], status__in=[Grievance.Status.SUBMITTED, Grievance.Status.PENDING_ASSIGNMENT, Grievance.Status.ASSIGNED, Grievance.Status.IN_PROGRESS, Grievance.Status.REOPENED]).count() if row["assigned_department_id"] else queryset.filter(assigned_department__isnull=True).count(),
            "resolved": queryset.filter(assigned_department_id=row["assigned_department_id"], status__in=[Grievance.Status.RESOLVED, Grievance.Status.CLOSED]).count() if row["assigned_department_id"] else queryset.filter(assigned_department__isnull=True, status__in=[Grievance.Status.RESOLVED, Grievance.Status.CLOSED]).count(),
        }
    monthly_trends = [
        {"month": row["month"].strftime("%Y-%m"), "count": row["count"]}
        for row in queryset.annotate(month=TruncMonth("created_at")).values("month").annotate(count=Count("id")).order_by("month")
    ]
    alerts = []
    for grievance in queryset.filter(priority=Grievance.Priority.CRITICAL, status__in=[Grievance.Status.SUBMITTED, Grievance.Status.PENDING_ASSIGNMENT, Grievance.Status.ASSIGNED, Grievance.Status.IN_PROGRESS])[:20]:
        alerts.append({"alert_id": f"critical-{grievance.id}", "alert_type": "CRITICAL_COMPLAINT", "severity": "CRITICAL", "title": "Critical electrical complaint", "description": grievance.title, "grievance_id": grievance.complaint_number})
    for grievance in queryset.filter(due_at__lt=timezone.now(), status__in=[Grievance.Status.SUBMITTED, Grievance.Status.PENDING_ASSIGNMENT, Grievance.Status.ASSIGNED, Grievance.Status.IN_PROGRESS])[:20]:
        alerts.append({"alert_id": f"sla-{grievance.id}", "alert_type": "SLA_BREACH", "severity": "HIGH", "title": "SLA breach", "description": grievance.title, "grievance_id": grievance.complaint_number})

    return Response({
        "summary": {
            "total_grievances": total,
            "pending": pending,
            "in_progress": in_progress,
            "resolved": resolved + closed,
            "critical": critical,
            "sla_breaches": sla_breaches,
        },
        "by_status": status_counts,
        "by_category": category_distribution,
        "by_department": departments,
        "monthly_trends": monthly_trends,
        "alerts": alerts,
        "total_grievances": total,
        "active_grievances": active,
        "in_progress": in_progress,
        "resolved_grievances": resolved + closed,
        "sla_compliance_rate": round((total - sla_breaches) / max(1, total) * 100, 1),
        "category_distribution": category_distribution,
        "priority_distribution": priority_distribution,
        "active_incidents": incidents_count,
        "human_ml_corrections": corrections_count,
        "total_consumers": User.objects.filter(role=User.Role.CONSUMER).count(),
        "total_officers": User.objects.filter(role=User.Role.OFFICER).count(),
    })
