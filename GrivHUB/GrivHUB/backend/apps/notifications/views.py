from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def notifications_list_view(request):
    return JsonResponse({"notifications": [], "count": 0})


@require_http_methods(["GET"])
def unread_count_view(request):
    return JsonResponse({"count": 0, "unread_count": 0})


@require_http_methods(["PATCH"])
def mark_notification_read_view(request, notification_id):
    return JsonResponse({"success": True, "notification_id": notification_id})


@require_http_methods(["POST"])
def mark_all_notifications_read_view(request):
    return JsonResponse({"success": True, "updated": 0})
