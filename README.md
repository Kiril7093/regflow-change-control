# RegFlow — Change Control MVP

A small eQMS-style Change Control app demonstrating a realistic regulated workflow:

**Create → Edit Draft → Submit → Approve/Reject → Immutable Audit Trail → PDF Export**

## What this demonstrates (portfolio value)

- End-to-end workflow states: Draft → In review → Approved/Rejected
- Immutable audit trail (who did what, when)
- One-click “audit package” PDF export including metadata + audit trail
- Admin UI for inspection + basic user UI for daily use
- CI (GitHub Actions): lint + Django checks/tests

> Note: This is a portfolio MVP designed to reflect regulated-workflow patterns.  
> It does **not** claim certification or compliance on its own.

## Quick start (local, SQLite)

From the project root:

```bash
cd ~/projects/regflow/regflow
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
cp .env.example .env
