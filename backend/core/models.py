from django.conf import settings
from django.db import models


class ChangeRequest(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        IN_REVIEW = "in_review", "In review"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    class ChangeType(models.TextChoices):
        SOP = "sop", "Lab SOP change"
        CALIBRATION = "calibration", "Equipment calibration change"
        SOFTWARE = "software", "Software change"
        MED_DEVICE_DOC = "med_device_doc", "Medical device document change"

    title = models.CharField(max_length=200)
    rationale = models.TextField(blank=True)
    change_type = models.CharField(max_length=40, choices=ChangeType.choices, default=ChangeType.SOP)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="change_requests_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"CR#{self.pk} {self.title}"


class AuditEvent(models.Model):
    class EventType(models.TextChoices):
        CREATED = "created", "Created"
        EDITED = "edited", "Edited"
        SUBMITTED = "submitted", "Submitted for review"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    change_request = models.ForeignKey(ChangeRequest, on_delete=models.CASCADE, related_name="audit_events")
    event_type = models.CharField(max_length=20, choices=EventType.choices)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    message = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]

    def __str__(self) -> str:
        return f"CR#{self.change_request_id} {self.event_type} by {self.actor_id}"
