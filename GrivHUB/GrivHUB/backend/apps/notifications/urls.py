from django.urls import re_path

from . import views


urlpatterns = [
    re_path(r"^$", views.notifications_list_view, name="notifications-list"),
    re_path(r"^unread-count/?$", views.unread_count_view, name="notifications-unread-count"),
    re_path(
        r"^(?P<notification_id>[A-Za-z0-9_-]+)/read/?$",
        views.mark_notification_read_view,
        name="notification-read",
    ),
    re_path(r"^read-all/?$", views.mark_all_notifications_read_view, name="notifications-read-all"),
]
