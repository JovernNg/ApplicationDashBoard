# Final System Validation

Date: 24 September 2026

System:
Application Operations and Incident Management Dashboard

## Purpose

The purpose of final validation is to confirm that the system is in a stable state after implementation, functional testing, security testing and evaluation preparation.

## Django System Check

Command:

python manage.py check

Result:

To be recorded.

## Migration Consistency

Command:

python manage.py makemigrations --check --dry-run

Expected:

No changes detected

Actual result:

To be recorded.

## Migration Status

Command:

python manage.py showmigrations operations

Result:

To be recorded.

## Regression Testing

Command:

python manage.py test -v 2

Total tests:

To be recorded.

Passed:

To be recorded.

Failed:

To be recorded.

Errors:

To be recorded.

Overall result:

To be recorded.

## Demonstration Dataset

Command:

python manage.py seed_demo_data

Demo users:

demo_admin

demo_operator1

demo_operator2

Demo applications:

4

Demo incidents:

6

The demonstration dataset includes:

Healthy application

Degraded application

Down application

Maintenance application

Critical incident

High priority incident

Medium priority incident

Low priority incident

New incident

Assigned incident

In Progress incident

Resolved incident

Closed incident

SLA Within state

SLA At Risk state

SLA Breached state

Incident timeline updates

Audit records

## Final Manual Checks

| Check | Result |
|---|---|
| Login | |
| Logout | |
| Dashboard | |
| Application list | |
| Application detail | |
| Application create | |
| Application edit | |
| Incident list | |
| Incident search | |
| Incident filtering | |
| Incident detail | |
| Incident assignment | |
| Incident transition | |
| Incident timeline | |
| SLA display | |
| Audit Log | |
| Administrator authorization | |
| Operations User authorization | |
| Object-level authorization | |
| Closed incident protection | |

## Known Limitations

Record only genuine remaining limitations.

Examples may include:

Local development deployment only.

SQLite used rather than a production database.

Small formative usability sample.

Performance evaluated in a controlled local environment.

No email or external monitoring integration.

## Final Status

To be completed after validation.