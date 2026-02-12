from django.contrib import admin

from .models import AuditEvent, ChangeRequest


class AuditEventInline(admin.TabularInline):
    model = AuditEvent
    extra = 0
    readonly_fields = ("event_type", "actor", "message", "created_at")


@admin.register(ChangeRequest)
class ChangeRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "change_type", "status", "created_by", "created_at", "updated_at")
    list_filter = ("change_type", "status")
    search_fields = ("title", "rationale")
    autocomplete_fields = ("created_by",)
    inlines = [AuditEventInline]


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ("id", "change_request", "event_type", "actor", "created_at")
    list_filter = ("event_type",)
    search_fields = ("message",)
    autocomplete_fields = ("change_request", "actor")
