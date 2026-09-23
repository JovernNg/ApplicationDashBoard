# Final Demonstration Checklist

## Before Demonstration

Run:

python manage.py seed_demo_data

Run:

python manage.py test

Run:

python manage.py check

Start server:

python manage.py runserver

Open:

http://127.0.0.1:8000/

## Primary Demonstration Account

Username:
demo_admin

Password:
DemoPass123!

## Suggested Demonstration Flow

1. Login.

2. Show Dashboard.

3. Explain six summary cards.

4. Show Applications by Status chart.

5. Show Open Incidents by Priority chart.

6. Open the breached Critical incident.

7. Show SLA target, deadline and breach state.

8. Show Incident Timeline.

9. Show controlled workflow.

10. Show Search and Filtering.

11. Show Audit Log.

12. Logout.

13. Login as demo_operator2.

14. Demonstrate role restrictions.

15. Attempt access to an incident assigned to demo_operator1.

16. Explain object-level authorization.

## Important Demonstration Points

Do not spend significant time showing Django Admin.

Focus on the application interface.

Highlight:

Controlled workflow

SLA engine

Role-based authorization

Object-level authorization

Audit trail

Timeline

Dashboard analytics

Search and filtering

Testing evidence