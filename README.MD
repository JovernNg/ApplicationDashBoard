# Application Operations and Incident Management Dashboard

A web-based application operations and incident management dashboard developed as a Final Year Project.

The system provides a central interface for monitoring application health, managing operational incidents, enforcing incident workflow rules, tracking SLA performance, recording operational updates, maintaining an audit trail, and presenting operational information through dashboard analytics.

---

## Project Overview

The application was developed to demonstrate the design and implementation of a lightweight operations and incident management platform.

The system supports two application roles:

- Administrator
- Operations User

Administrators manage applications, assign incidents and review audit information.

Operations Users can report incidents and manage incidents assigned to them.

The system enforces workflow and authorization rules on the server rather than relying only on interface visibility.

---

## Main Features

### Authentication and Role-Based Access Control

The application uses Django authentication.

Two application roles are supported:

- Administrator
- Operations User

Administrator-only functionality is protected by server-side authorization checks.

Object-level authorization is also applied to incident management so that an Operations User can modify only incidents assigned to them.

---

### Application Management

Administrators can:

- Create applications
- Edit application details
- Update application operational status

Application statuses include:

- Healthy
- Degraded
- Down
- Maintenance

Each application can also record:

- Owner
- Environment
- Support contact
- Availability percentage
- Description

Application changes are recorded in the audit trail.

---

### Incident Management

Authenticated users can report incidents.

Each incident records:

- Automatically generated incident number
- Related application
- Title
- Description
- Priority
- Status
- Reporter
- Assigned user
- Reported timestamp
- Resolution timestamp
- Closure timestamp
- Resolution notes

Incident priorities are:

- Critical
- High
- Medium
- Low

---

### Controlled Incident Workflow

Incident status transitions follow the defined workflow:

```text
New
  ↓
Assigned
  ↓
In Progress
  ↓
Resolved
  ↓
Closed
```

Invalid workflow transitions are rejected.

Additional workflow rules include:

- New incidents must be assigned before work begins.
- Only Administrators can assign incidents.
- Operations Users can manage only incidents assigned to them.
- Resolution notes are required before an incident can be resolved.
- A resolved timestamp is generated automatically.
- A closure timestamp is generated automatically.
- Closed incidents cannot be reopened.
- Closed incidents cannot receive new operational updates.

---

### SLA Monitoring

The application includes a calendar-time SLA calculation engine.

SLA targets are:

| Priority | SLA Target |
|---|---:|
| Critical | 2 hours |
| High | 4 hours |
| Medium | 8 hours |
| Low | 24 hours |

SLA states are:

- Within SLA
- At Risk
- Breached

An incident becomes At Risk when 75% of its SLA target has elapsed.

An incident becomes Breached when its SLA deadline is reached.

The SLA clock stops when the incident is resolved.

The incident interface displays:

- SLA target
- SLA deadline
- SLA state
- Percentage of SLA time elapsed

---

### Incident Timeline

Assigned Operations Users and Administrators can add timestamped operational updates to active incidents.

Each update records:

- Incident
- User
- Update text
- Timestamp

Updates are displayed chronologically on the Incident Detail page.

Closed incidents remain viewable but cannot receive additional updates.

---

### Audit Trail

The system records important operational actions including:

- Application creation
- Application updates
- Application status changes
- Incident creation
- Incident assignment
- Incident status changes
- Incident operational updates

Audit entries record the user, application, incident, action, timestamp and descriptive details.

The application Audit Log is restricted to Administrators.

Operational records in Django Admin are configured as read-only so that workflow and audit controls cannot be bypassed through the administrative interface.

---

### Operations Dashboard

The main dashboard provides six operational summary cards:

- Total Applications
- Healthy Applications
- Problem Applications
- Open Incidents
- Critical Incidents
- SLA Breaches

Problem Applications are defined as applications with either:

- Degraded
- Down

status.

Maintenance applications are not counted as problem applications.

Open incidents are incidents in:

- New
- Assigned
- In Progress

states.

The dashboard also includes:

- Applications by Status chart
- Open Incidents by Priority chart
- Recent Incidents table
- SLA status indicators

Chart.js is used for dashboard visualisations.

---

### Search and Filtering

The incident list supports search by:

- Incident number
- Title
- Description

Search is case-insensitive and supports partial matching.

Incidents can also be filtered by:

- Application
- Priority
- Status
- Assigned user
- Unassigned state

Search and filter criteria can be combined.

---

## Technology Stack

The project uses:

- Python 3.14.5
- Django 5.2.17
- SQLite
- Bootstrap 5.3
- Chart.js 4.x
- HTML
- CSS
- JavaScript
- Git
- GitHub

Development was performed using Visual Studio Code.

---

## Project Structure

```text
ApplicationOperationsDashboard/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── operations/
│   ├── management/
│   │   └── commands/
│   │       ├── measure_performance.py
│   │       ├── seed_demo_data.py
│   │       └── setup_roles.py
│   │
│   ├── services/
│   │   ├── audit.py
│   │   ├── permissions.py
│   │   ├── sla.py
│   │   └── workflow.py
│   │
│   ├── templates/
│   │   └── operations/
│   │
│   ├── tests/
│   │
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── templates/
│   └── registration/
│       └── login.html
│
├── docs/
│   ├── development-log.md
│   ├── functional-test-results.md
│   ├── security-test-results.md
│   ├── performance-test-results.md
│   ├── usability-test-plan.md
│   ├── usability-test-results.md
│   ├── final-validation.md
│   └── demo-checklist.md
│
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Installation

## 1. Clone the Repository

```bash
git clone <repository-url>
cd ApplicationOperationsDashboard
```

---

## 2. Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Apply Database Migrations

```bash
python manage.py migrate
```

---

## 5. Create Application Roles

Run:

```bash
python manage.py setup_roles
```

This creates the application groups:

```text
Administrator
Operations User
```

---

## 6. Create a Superuser

A Django superuser can be created for development and inspection purposes:

```bash
python manage.py createsuperuser
```

The Django Admin interface is available at:

```text
http://127.0.0.1:8000/admin/
```

Operational domain records are configured as read-only within Django Admin.

Normal application management should be performed through the main application interface.

---

# Running the Application

Start the Django development server:

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

Login is required before accessing operational pages.

---

# Demonstration Data

A repeatable demonstration dataset can be generated using:

```bash
python manage.py seed_demo_data
```

The command creates:

- 4 demonstration applications
- 6 demonstration incidents
- Incident timeline updates
- Audit records
- Multiple SLA states
- Multiple workflow states
- Three demonstration user accounts

The demonstration dataset contains application states covering:

- Healthy
- Degraded
- Down
- Maintenance

It also contains incidents covering:

- Critical
- High
- Medium
- Low priorities
- New
- Assigned
- In Progress
- Resolved
- Closed states
- Within SLA
- At Risk
- Breached SLA conditions

---

## Demonstration Accounts

### Administrator

```text
Username: demo_admin
Password: DemoPass123!
```

### Operations User 1

```text
Username: demo_operator1
Password: DemoPass123!
```

### Operations User 2

```text
Username: demo_operator2
Password: DemoPass123!
```

These credentials are for local demonstration and development purposes only.

They must not be used as production credentials.

---

# Resetting the Demonstration Database

If a clean demonstration environment is required, back up the existing development database first.

Windows:

```bash
copy db.sqlite3 db_before_m13.sqlite3
```

Then reset application data:

```bash
python manage.py flush
```

Confirm the reset when prompted.

Recreate the controlled demonstration dataset:

```bash
python manage.py seed_demo_data
```

If Django Admin access is required after flushing the database, recreate the superuser:

```bash
python manage.py createsuperuser
```

The backup database can be restored if required by stopping the server and using:

```bash
copy /Y db_before_m13.sqlite3 db.sqlite3
```

---

# Automated Testing

Run the complete automated test suite using:

```bash
python manage.py test
```

For verbose output:

```bash
python manage.py test -v 2
```

The test suite covers areas including:

- Authentication
- Role-based permissions
- Application management
- Audit logging
- Incident management
- Incident workflow
- SLA calculations
- Incident timeline
- Dashboard analytics
- Search and filtering
- Integrated functional workflows
- Object-level authorization
- CSRF protection
- XSS handling
- SQL-injection-style input
- Session behaviour
- Protected field tampering
- Closed incident protection
- Administrative interface restrictions

The final validation should record the actual number of executed tests and the final result.

---

# Django System Checks

Run the standard system check:

```bash
python manage.py check
```

Check for unapplied model changes:

```bash
python manage.py makemigrations --check --dry-run
```

The expected result for the final project version is:

```text
No changes detected
```

Migration status can be checked using:

```bash
python manage.py showmigrations operations
```

---

# Deployment Security Check

Django's deployment security checks can be run using:

```bash
python manage.py check --deploy
```

The local project configuration may generate warnings relating to development settings such as:

- DEBUG
- HTTPS
- Secure cookies
- HSTS
- SECRET_KEY configuration

These should be interpreted as production deployment considerations rather than automatically removed from the local development environment.

---

# Performance Testing

The project includes a management command for measuring server-side response time for major pages.

Run:

```bash
python manage.py measure_performance --username demo_operator1 --runs 5
```

The command asks for the account password without displaying or storing it.

The measured pages include:

- Dashboard
- Application List
- Application Detail
- Incident List
- Incident Detail

One warm-up request is performed before recorded measurements.

The command reports:

- Individual request times
- Average
- Median
- Minimum
- Maximum

The project performance target is:

```text
Less than 2000 ms per main page
```

within the controlled local test environment.

Performance measurements represent local server-side response behaviour and are not intended to represent production internet performance or concurrent production workloads.

---

# Security Testing

Security testing includes automated and manual checks for:

- Authentication enforcement
- Administrator-only authorization
- Object-level incident authorization
- Direct URL manipulation
- CSRF protection
- Stored XSS handling
- SQL-injection-style search input
- Session invalidation
- POST parameter tampering
- Closed incident modification attempts
- Django Admin workflow bypass attempts

OWASP ZAP can also be used against the locally hosted development system for dynamic security analysis.

Security test results should describe observed behaviour rather than claim that the application is completely free from vulnerabilities.

---

# Usability Evaluation

The project includes a usability evaluation plan based on realistic operational tasks.

The evaluation is intended for a small formative sample of 3 to 5 volunteer participants.

Example tasks include:

- Logging into the system
- Reading dashboard information
- Finding an incident
- Reporting an incident
- Reviewing SLA information
- Adding an incident update
- Updating incident status

Evaluation measurements include:

- Task completion
- Completion time
- Assistance required
- Participant comments
- Observer comments
- System Usability Scale score

The usability evaluation should only be conducted after any required academic ethics or participant approval has been confirmed.

---

# Final Demonstration Preparation

Before demonstrating the final system:

```bash
python manage.py seed_demo_data
python manage.py check
python manage.py test
python manage.py runserver
```

The suggested demonstration flow is:

```text
Login
↓
Dashboard
↓
Application Health
↓
Incident List
↓
Search and Filtering
↓
Critical Incident
↓
SLA Information
↓
Incident Timeline
↓
Controlled Workflow
↓
Audit Log
↓
Role Restrictions
```

---

# Known Prototype Limitations

The project is a prototype developed and evaluated within a controlled academic environment.

Known limitations include:

- SQLite is used rather than a production-scale database.
- The Django development server is used for local evaluation.
- Performance testing is performed in a controlled local environment.
- Usability testing uses a small formative participant sample.
- The system does not integrate with external infrastructure monitoring platforms.
- The system does not automatically ingest incidents from monitoring tools.
- Email or external notification integration is not currently implemented.
- Production HTTPS and deployment hardening are outside the current prototype environment.

---

# Development Status

The main engineering milestones include:

```text
M0  Project Setup
M1  Authentication and Roles
M2  Application Management
M3  Audit Trail
M4  Incident Management
M5  Controlled Incident Workflow
M6  SLA Engine
M7  Incident Timeline
M8  Dashboard Analytics
M9  Search and Filtering
M10 Functional Testing
M11 Security Testing
M12 Performance and Usability Evaluation
M13 Final Demo Data and System Validation
```

The implementation is now considered feature-complete.

Further code changes should generally be limited to:

- Confirmed defect corrections
- Evaluation-supported usability improvements
- Documentation corrections
- Submission preparation

---

# Academic Project

This project was developed as a Final Year Project for a BSc Computing Science programme.

Project title:

**Design and Implementation of a Web-Based Application Operations and Incident Management Dashboard**