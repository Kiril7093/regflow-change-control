import io
from datetime import datetime

from django.utils import timezone
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def _wrap_lines(text: str, width: int = 105) -> list[str]:
    words = (text or "").split()
    lines: list[str] = []
    cur: list[str] = []
    n = 0
    for w in words:
        add = len(w) + (1 if cur else 0)
        if n + add > width:
            lines.append(" ".join(cur))
            cur = [w]
            n = len(w)
        else:
            cur.append(w)
            n += add
    if cur:
        lines.append(" ".join(cur))
    return lines or ["(none)"]


def _fmt_dt(dt) -> str:
    if not dt:
        return "(none)"
    # Django stores datetimes in UTC; present in local timezone for readability
    try:
        dt_local = timezone.localtime(dt)
        return dt_local.strftime("%b %d, %Y %I:%M %p %Z")
    except Exception:
        # fallback for naive datetimes
        if isinstance(dt, datetime):
            return dt.strftime("%b %d, %Y %I:%M %p")
        return str(dt)


def build_change_request_pdf(*, cr, events) -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    w, h = letter

    left = 72
    y = h - 72

    def line(txt: str, dy: int = 14):
        nonlocal y
        c.drawString(left, y, txt)
        y -= dy
        if y < 72:
            c.showPage()
            y = h - 72

    now_local = timezone.localtime(timezone.now()).strftime("%b %d, %Y %I:%M %p %Z")

    line("RegFlow — Change Request Package", 18)
    line(f"Generated: {now_local}", 18)

    line(f"CR#{cr.id}: {cr.title}", 18)
    line(f"Status: {cr.get_status_display()}")
    line(f"Type: {cr.get_change_type_display()}")
    line(f"Created by: {cr.created_by.username}")
    line(f"Created at: {_fmt_dt(cr.created_at)}")
    line(f"Updated at: {_fmt_dt(cr.updated_at)}", 18)

    line("Rationale:", 16)
    for ln in _wrap_lines(cr.rationale, width=110):
        line(ln)
    y -= 10

    line("Audit trail:", 16)
    if events:
        for e in events:
            base = f"{_fmt_dt(e.created_at)} — {e.get_event_type_display()} by {e.actor.username}"
            msg = f"{base}: {e.message}" if e.message else base
            for ln in _wrap_lines(msg, width=110):
                line(ln)
            y -= 4
    else:
        line("(no audit events)")

    c.save()
    return buf.getvalue()
