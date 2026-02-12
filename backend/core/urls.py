from django.urls import path
from .views import (
    home,
    change_request_list,
    change_request_create,
    change_request_detail,
    change_request_edit,
    change_request_submit,
    change_request_approve,
    change_request_reject,
    change_request_pdf,
)

urlpatterns = [
    path("", home, name="home"),
    path("change-requests/", change_request_list, name="change_request_list"),
    path("change-requests/new/", change_request_create, name="change_request_create"),
    path("change-requests/<int:pk>/", change_request_detail, name="change_request_detail"),
    path("change-requests/<int:pk>/edit/", change_request_edit, name="change_request_edit"),
    path("change-requests/<int:pk>/submit/", change_request_submit, name="change_request_submit"),
    path("change-requests/<int:pk>/approve/", change_request_approve, name="change_request_approve"),
    path("change-requests/<int:pk>/reject/", change_request_reject, name="change_request_reject"),
    path("change-requests/<int:pk>/pdf/", change_request_pdf, name="change_request_pdf"),
]
