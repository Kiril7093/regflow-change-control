from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ChangeRequestForm
from .models import AuditEvent, ChangeRequest
from .pdf import build_change_request_pdf


def home(request):
    return render(request, "core/home.html")


@login_required
def change_request_list(request):
    qs = ChangeRequest.objects.select_related("created_by").order_by("-created_at")
    change_requests = ChangeRequest.objects.all().order_by("-updated_at", "-id")
    return render(request, "core/change_request_list.html", {"change_requests": qs})


@login_required
def change_request_detail(request, pk: int):
    cr = get_object_or_404(ChangeRequest.objects.select_related("created_by"), pk=pk)
    events = cr.audit_events.select_related("actor").all()
    return render(request, "core/change_request_detail.html", {"cr": cr, "events": events})


@login_required
def change_request_pdf(request, pk: int):
    cr = get_object_or_404(ChangeRequest.objects.select_related("created_by"), pk=pk)
    events = cr.audit_events.select_related("actor").all()
    pdf_bytes = build_change_request_pdf(cr=cr, events=events)

    resp = HttpResponse(pdf_bytes, content_type="application/pdf")
    resp["Content-Disposition"] = f'attachment; filename="regflow_CR-{cr.id}.pdf"'
    return resp


@login_required
def change_request_create(request):
    if request.method == "POST":
        form = ChangeRequestForm(request.POST)
        if form.is_valid():
            cr = form.save(commit=False)
            cr.created_by = request.user
            cr.save()

            AuditEvent.objects.create(
                change_request=cr,
                event_type=AuditEvent.EventType.CREATED,
                actor=request.user,
                message="Created change request",
            )

            return redirect("change_request_detail", pk=cr.pk)
    else:
        form = ChangeRequestForm()

    return render(request, "core/change_request_form.html", {"form": form, "mode": "create"})


@login_required
def change_request_edit(request, pk: int):
    cr = get_object_or_404(ChangeRequest, pk=pk)

    if cr.created_by_id != request.user.id:
        return HttpResponse("Forbidden", status=403)
    if cr.status != ChangeRequest.Status.DRAFT:
        return HttpResponse("Cannot edit after submission.", status=400)

    if request.method == "POST":
        form = ChangeRequestForm(request.POST, instance=cr)
        if form.is_valid():
            form.save()

            AuditEvent.objects.create(
                change_request=cr,
                event_type=AuditEvent.EventType.EDITED,
                actor=request.user,
                message="Edited change request",
            )

            return redirect("change_request_detail", pk=cr.pk)
    else:
        form = ChangeRequestForm(instance=cr)

    return render(request, "core/change_request_form.html", {"form": form, "mode": "edit", "cr": cr})


@login_required
def change_request_submit(request, pk: int):
    cr = get_object_or_404(ChangeRequest, pk=pk)

    if request.method != "POST":
        return HttpResponse("Method not allowed", status=405)

    if cr.created_by_id != request.user.id:
        return HttpResponse("Forbidden", status=403)

    if cr.status != ChangeRequest.Status.DRAFT:
        return HttpResponse("Only Draft requests can be submitted.", status=400)

    cr.status = ChangeRequest.Status.IN_REVIEW
    cr.save(update_fields=["status", "updated_at"])

    AuditEvent.objects.create(
        change_request=cr,
        event_type=AuditEvent.EventType.SUBMITTED,
        actor=request.user,
        message="Submitted for review",
    )

    return redirect("change_request_detail", pk=cr.pk)


@login_required
def change_request_approve(request, pk: int):
    cr = get_object_or_404(ChangeRequest, pk=pk)

    if request.method != "POST":
        return HttpResponse("Method not allowed", status=405)

    if cr.status != ChangeRequest.Status.IN_REVIEW:
        return HttpResponse("Only In review requests can be approved.", status=400)

    cr.status = ChangeRequest.Status.APPROVED
    cr.save(update_fields=["status", "updated_at"])

    AuditEvent.objects.create(
        change_request=cr,
        event_type=AuditEvent.EventType.APPROVED,
        actor=request.user,
        message="Approved",
    )

    return redirect("change_request_detail", pk=cr.pk)


@login_required
def change_request_reject(request, pk: int):
    cr = get_object_or_404(ChangeRequest, pk=pk)

    if request.method != "POST":
        return HttpResponse("Method not allowed", status=405)

    if cr.status != ChangeRequest.Status.IN_REVIEW:
        return HttpResponse("Only In review requests can be rejected.", status=400)

    cr.status = ChangeRequest.Status.REJECTED
    cr.save(update_fields=["status", "updated_at"])

    AuditEvent.objects.create(
        change_request=cr,
        event_type=AuditEvent.EventType.REJECTED,
        actor=request.user,
        message="Rejected",
    )

    return redirect("change_request_detail", pk=cr.pk)
