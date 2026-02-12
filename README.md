# RegFlow — Change Control MVP

A small eQMS-style Change Control app demonstrating a realistic regulated workflow:

**Create → Edit Draft → Submit → Approve/Reject → Immutable Audit Trail → PDF Export**

## What this demonstrates (portfolio value)

- End-to-end workflow states: Draft → In review → Approved/Rejected
- Immutable audit trail (who did what, when)
- One-click “audit package” PDF export including metadata + audit trail
- Admin UI for inspection + basic user UI for daily use

## Quick start (local, SQLite)

From the project root ():



Generate a secret key (recommended):



Run migrations + create an admin user:



Start the server:



Open:
- Home: http://127.0.0.1:8000/
- Change Requests: http://127.0.0.1:8000/change-requests/
- Admin: http://127.0.0.1:8000/admin/

## 60-second demo script

1. Log in at 
2. Create a **Draft** change request
3. Edit it (still Draft)
4. **Submit for review** (status becomes *In review*)
5. **Approve** or **Reject**
6. On the detail page, click **View PDF** to export the audit package

The PDF includes the change request metadata + full audit trail.
