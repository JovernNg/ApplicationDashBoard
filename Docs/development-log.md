# Development Log

## Project Initialisation

Date: 22/09/2026

### Work completed

 Created project directory.
 Initialised Git repository.
 Created Python virtual environment.
 Installed Django 5.2.
 Created requirements.txt.

### Problems encountered

None.

### Decisions

The project will use a single Django application called `operations`

### Milestone 1 - Project Setup, Authentication and Role-Based Access

Date: 22 September 2026
Status: Completed


### Objective

The objective of this milestone was to initialise the Django project and implement the basic authentication and role-based access control required by the system.
The system uses two main user roles:
Administrator
Operations User
The Administrator is intended to have access to management functions, while the Operations User has more restricted operational access.

### Work Completed

Created the Django project and operations application.
Created and activated a Python virtual environment.
Installed Django 5.2.
Configured SQLite as the development database.
Configured the project's templates directory.
Configured the Singapore timezone.
Enabled Django's built-in authentication system.
Created login and logout functionality.
Created a protected dashboard page.
Created the Administrator and Operations User groups.
Created a reusable administrator_required permission decorator.
Created helper functions for checking Administrator and Operations User roles.
Created an Administrator-only test page.
Created a superuser account for development and testing.
Created an Operations User account for development and testing.
Added Bootstrap styling to the initial interface.
Added automated tests for authentication and role permissions.
Initialised Git version control for the project.

### Design Decisions

Django's built-in authentication and Group model were used instead of creating a custom authentication system.
This provides an established authentication mechanism while allowing the application to implement role-based permissions through the Administrator and Operations User groups.
A custom administrator_required decorator was created so that Administrator-only permissions can be applied consistently to views throughout the project.
The permission check is performed on the server side rather than relying only on whether interface buttons are visible.

### Testing Performed

The following authentication and permission behaviours were tested:
Unauthenticated users are redirected to the login page when attempting to access the dashboard.
Valid user credentials allow successful login.
Invalid credentials are rejected.
Administrator users can access Administrator-only pages.
Operations Users receive an HTTP 403 response when attempting to access Administrator-only pages.
Automated Django tests were created to verify authentication and permission behaviour.
The automated test suite was executed using:
python manage.py test
The tests completed successfully with an OK result.

### Problems Encountered

Missing auth_group Database Table
During initial role creation, Django returned the following error:
no such table: auth_group
This occurred because the role setup command attempted to access Django's built-in Group model before the database migrations had been applied.
The issue was resolved by running:
python manage.py migrate
before executing the role setup command.
This created Django's authentication, permission, session and administration database tables.
Django Test Discovery Conflict
When the automated tests were introduced, Django returned an import error similar to:
ImportError: 'tests' module incorrectly imported
The operations application contained both:
operations/tests.py
and:
operations/tests/
This caused a conflict because Python attempted to resolve two modules with the same operations.tests name.
The original Django-generated tests.py file was removed and the project retained the structured test package containing:
operations/tests/init.py
operations/tests/test_authentication.py
operations/tests/test_permissions.py
After removing the conflicting file, the test suite completed successfully.

### Outcome

Milestone 1 was completed successfully.
The project now has a working Django foundation with user authentication, login and logout, Administrator and Operations User roles, server-side role-based access control, protected pages, and automated authentication and permission tests.
This provides the access-control foundation required for later application and incident management functions.

### Milestone 2 - Application Management

Date: 22 September 2026
Status: Completed

### Objective

The objective of this milestone was to implement the application's application register.
The register allows operational applications to be stored together with information such as ownership, environment, support contact, operational status and availability.
Application modification functions are restricted to Administrators, while Operations Users are provided with read-only access.

### Work Completed

Created the Application database model.
Added fields for application name, description, owner, environment, support contact, operational status, availability percentage, creation timestamp and last updated timestamp.
Created the Healthy, Degraded, Down and Maintenance application statuses.
Added validation to restrict availability values to between 0% and 100%.
Made application names unique.
Created and applied the initial application database migration.
Registered the Application model with the Django administration interface.
Created an ApplicationForm using Django's ModelForm.
Created an application list page.
Created an application detail page.
Created an Administrator-only application registration page.
Created an Administrator-only application editing page.
Added application navigation to the main interface.
Added Bootstrap styling to the application list, detail and form pages.
Added status badges to improve the visibility of application operational states.
Restricted application creation and editing through server-side permission checks.
Hid application management controls from Operations Users.
Added automated tests for application access and permissions.

### Design Decisions

Application creation and modification functions are restricted to the Administrator role.
Operations Users can view application records but cannot modify them.
This separation was implemented at both the interface and server levels. Management buttons are hidden from Operations Users, while the underlying views are also protected using the administrator_required decorator.
This means that manually entering a protected URL does not bypass the permission system.
The application status field uses predefined values instead of free-text input to maintain consistent operational status data.
The defined values are:
Healthy
Degraded
Down
Maintenance
Application names were configured as unique to prevent multiple records from representing the same application.

### Testing Performed

The following behaviours were tested manually and through automated Django tests:
Administrator can view the application register.
Operations User can view the application register.
Administrator can register a new application.
Administrator can edit an existing application.
Administrator can change an application's operational status.
Operations User cannot register an application.
Operations User cannot edit an application.
Direct access to Administrator-only application management URLs returns HTTP 403 for Operations Users.
Availability values greater than 100% are rejected.
Availability values below 0% are rejected.
Duplicate application names are rejected.
The test suite was executed using:
python manage.py test

### Problems Encountered

Missing Application Detail View
When starting the Django development server after adding the application URLs, Django returned:
AttributeError: module 'operations.views' has no attribute 'application_detail'
The URL configuration referenced views.application_detail, but the corresponding view had not yet been added to operations/views.py.
The missing application_detail view was added and Django's system check was then able to complete normally.
Form Navigation Caused by HTML Structure
When the application registration page was first displayed, clicking inside the application name field unexpectedly returned the user to the dashboard.
The problem was caused by incorrect HTML structure in the shared base.html template. A navigation link was affecting content outside the intended navigation area.
The base template was replaced with correctly structured HTML containing properly closed navigation links.
After correcting the template structure, the application form fields behaved normally.
Low Text Contrast
Some dashboard text appeared as light grey text against a white background, which reduced readability.
The shared base template and dashboard styling were adjusted to use dark text on light backgrounds while retaining light text inside the dark navigation bar.
This improved readability and provided better visual contrast.
Missing Django Messages Import
After successfully submitting the application registration form, Django returned:
NameError: name 'messages' is not defined
The application had been saved successfully, but the view attempted to display a success message without importing Django's messages framework.
The issue was resolved by adding:
from django.contrib import messages
to operations/views.py.
The application creation flow then successfully validates the submitted form, saves the application, displays a success message and redirects the user to the application list.

### Outcome

Milestone 2 was completed successfully.
The system now provides a functional application register with persistent application records, application status tracking, availability values, application list and detail pages, Administrator-only creation and editing, read-only Operations User access, input validation, role-based protection, improved interface readability and automated application permission tests.
The application management functionality provides the foundation required for incidents to be associated with individual applications in the next development stages.

### Milestone 3 - Audit Trail

Date: 22 September 2026
Status: Completed

### Objective

The objective of this milestone was to implement an audit trail that records important application management activities performed within the system.
The audit trail is intended to provide accountability by recording who performed an action, which application was affected, what type of action occurred, a description of the change and the time the action was recorded.

### Work Completed

Created the AuditLog database model.
Added audit log fields for user, application, action, details and creation timestamp.
Created audit action types for Application Created, Application Updated and Application Status Changed.
Configured audit records to remain available even if the related user or application is later removed.
Created and applied the database migration for the audit log.
Created a reusable audit logging service.
Integrated audit logging into application creation.
Integrated audit logging into application editing.
Added separate logging for application status changes.
Added logging of other changed application fields.
Created an Administrator-only audit log page.
Added the audit log to the application management interface.
Registered the audit log with the Django administration interface.
Configured audit log records as read-only in Django Admin.
Prevented audit records from being manually added, edited or deleted through Django Admin.
Added automated tests for audit logging and audit log access permissions.

### Design Decisions

A dedicated AuditLog model was created instead of storing audit information directly inside the Application model.
This allows each application to have multiple historical audit entries and provides a structure that can later be reused for incident and workflow activities.
The audit log records the user who performed the action through Django's user model.
The relationship to the user uses SET_NULL behaviour. This means that if a user account is deleted in the future, the audit record itself will remain available.
The application relationship also uses SET_NULL so that historical audit records are not automatically deleted if an application record is removed.
A reusable log_action service was created so that audit records are generated in a consistent way throughout the system.
Application status changes are recorded separately from ordinary application updates. This makes operational status changes easier to identify within the audit trail.
For example, changing an application from Healthy to Degraded creates an Application Status Changed record rather than only recording a general update.
Audit records are intended to be system-generated. Therefore, no normal interface is provided to manually edit or delete them.

### Testing Performed

The following audit behaviours were tested:
Creating an application generates an Application Created audit record.
The user who created the application is recorded.
The application associated with the action is recorded.
Editing application information generates an Application Updated audit record.
Changing an application's operational status generates an Application Status Changed audit record.
Status change details contain both the previous and new status.
Administrators can access the audit log page.
Operations Users receive an HTTP 403 response when attempting to access the audit log page.
Audit records are displayed in reverse chronological order.
Audit records display the action, user, application, details and timestamp.
The automated test suite was executed using:
python manage.py test
The tests completed successfully with an OK result.

### Problems Encountered

No major implementation errors were encountered during the audit trail milestone.
The main consideration was ensuring that application status changes were recorded separately from other application changes.
The application edit view was therefore designed to inspect Django's changed_data values before creating audit records.
If the status field is changed, a dedicated Application Status Changed audit entry is created.
If other application fields are changed, a separate Application Updated record is created containing the names of the fields that were modified.
This means that one form submission can generate more than one audit record when both the operational status and other application information are changed.
Example Audit Behaviour
When an Administrator creates an application, an audit record similar to the following is created:
Application Created
The details record that the application was registered and include its initial status.
When an Administrator changes an application owner, an audit record similar to the following is created:
Application Updated
The audit details identify the field that was changed.
When an Administrator changes an application from Healthy to Degraded, an audit record similar to the following is created:
Application Status Changed
The audit details record that the status changed from Healthy to Degraded.
Security and Access Control
The audit log page is restricted to Administrator users.
Operations Users cannot access the audit page, even if they manually enter the audit log URL.
This restriction is enforced through the existing administrator_required server-side permission decorator.
Audit records are not editable through the main application interface.
The Django administration interface was also configured so that audit records cannot be manually created, edited or deleted.
This helps preserve the audit trail as a record of actions generated by the application.

### Outcome

Milestone 3 was completed successfully.
The system now provides an audit trail that records important application management actions, including application creation, application updates, application status changes, the user responsible for the action, the application affected by the action, a description of the activity and the timestamp of the activity.
Administrators can review audit records through a dedicated audit log page, while Operations Users are prevented from accessing the audit trail.
The audit logging structure can now be extended in later milestones to record incident creation, incident assignment, workflow transitions, resolution activities and other operational actions.

### Milestone 4 - Incident Management

Date: 22 September 2026
Status: Completed

### Objective

The objective of this milestone was to implement the incident management functionality of the system.
The incident management module allows authenticated users to report operational incidents against registered applications. Each incident records the affected application, title, description, priority, status, reporting user and relevant timestamps.
This milestone also introduced automatic incident numbering and extended the audit trail so that incident creation is recorded.

### Work Completed

Created the Incident database model.
Added incident fields for incident number, affected application, title, description, priority, status, reporting user, assigned user, reporting timestamp, last updated timestamp, resolution timestamp, closure timestamp and resolution notes.
Created the following incident priority levels:
Critical
High
Medium
Low
Created the following incident status values:
New
Assigned
In Progress
Resolved
Closed
Configured newly created incidents to automatically start with the New status.
Created automatic incident number generation using the format:
INC-YYYYMMDD-XXXX
The final number is based on the incident database identifier.
Created and applied the database migration for the Incident model.
Configured incidents to reference registered applications.
Configured the application relationship using PROTECT behaviour so that an application with related incidents cannot be accidentally removed while incidents still depend on it.
Created an IncidentCreateForm using Django's ModelForm.
Restricted the incident creation form to the fields required when reporting a new incident.
The creation form includes:
Application
Title
Description
Priority
Status, assignment, resolution information and closure information are not directly entered during incident creation.
Created an incident list page.
Created an incident detail page.
Created an incident reporting page.
Added Incidents to the main navigation bar.
Added Bootstrap styling to the incident pages.
Added priority badges to make incident severity easier to identify visually.
Allowed both Administrator and Operations User accounts to report incidents.
Restricted incident functionality to authenticated users.
Automatically recorded the currently logged-in user as the reporting user.
Extended the audit logging service so that audit records can reference incidents.
Added an Incident Created audit action.
Integrated audit logging into incident creation.
Updated the audit log page so that incident-related audit records can display the associated incident number.
Registered the Incident model with Django Admin for development and inspection purposes.
Added automated tests for incident creation, access, numbering, default status and audit logging.

### Design Decisions

Incidents are linked to applications using a database relationship rather than storing the application name directly within the incident.
This ensures that every incident references an existing application record and avoids duplicating application information.
The Application relationship uses PROTECT behaviour.
This prevents an application from being deleted while incidents still reference it, helping to preserve incident history and referential integrity.
Incident numbers are generated automatically by the system instead of being entered manually by users.
The incident number uses the format:
INC-YYYYMMDD-XXXX
This provides a readable identifier containing the incident date and a unique numeric component.
New incidents automatically receive the New status.
Users cannot choose the incident status during the reporting process.
This was done because incident status changes will be controlled by the workflow logic introduced in the next milestone.
The incident creation form also does not allow the user to manually enter an assigned user, resolved timestamp, closure timestamp or resolution notes.
These fields are reserved for later stages of the controlled incident workflow.
Both Administrator and Operations User accounts are allowed to report incidents.
This reflects the intended operational use of the system, where operational staff should be able to record incidents without requiring an Administrator to create each record.

### Testing Performed

The following incident management behaviours were tested:
An Administrator can report a new incident.
An Operations User can report a new incident.
A logged-out user cannot access the incident reporting page.
A newly created incident is linked to the selected application.
The user who reported the incident is recorded.
A unique incident number is generated automatically.
The generated incident number begins with INC-.
The incident number includes a date component.
The incident number includes the incident database identifier.
New incidents automatically receive the New status.
Authenticated users can view the incident register.
Authenticated users can view incident details.
Incident information is displayed with the associated application.
Incident priority values are restricted to Critical, High, Medium and Low.
Incident status values are restricted to New, Assigned, In Progress, Resolved and Closed.
Creating an incident generates an Incident Created audit record.
The audit record contains the user who reported the incident.
The audit record references the affected application.
The audit record references the created incident.
The automated incident test suite was executed using:
python manage.py test operations.tests.test_incidents -v 2
The complete project test suite was executed using:
python manage.py test
The tests completed successfully with an OK result.
Automatic Incident Numbering
When an incident is first saved, the database assigns it a unique primary key.
The system then creates an incident number using the reporting date and the primary key.
An example incident number is:
INC-20260922-0001
A later incident could receive:
INC-20260922-0002
This means users do not have to manually create or maintain incident identifiers.
Incident Creation Behaviour
When an authenticated user reports an incident, the system performs the following process:
The submitted incident form is validated.
The currently logged-in user is assigned as the reporting user.
The incident status is automatically set to New.
The incident is stored in the database.
A unique incident number is generated.
An Incident Created audit record is created.
A success message is displayed.
The user is redirected to the incident detail page.
Audit Trail Integration
The existing audit trail was extended so that an audit record can reference both an application and an incident.
When an incident is created, an audit record is generated with the Incident Created action.
The audit details include the generated incident number and the selected priority.
For example:
Incident INC-20260922-0001 was reported with Critical priority.
The audit log records the reporting user, affected application, incident, action details and timestamp.
Security and Access Control
Incident reporting requires an authenticated user session.
Logged-out users are redirected to the login page.
Both Administrator and Operations User accounts are permitted to report incidents.
Users cannot manually enter an incident number.
Users cannot manually select the initial incident status.
Users cannot manually set resolution or closure timestamps during creation.
Users cannot enter resolution notes during initial incident creation.
These restrictions reduce the ability to bypass the intended incident workflow.
Further restrictions on incident assignment and status transitions will be introduced in the controlled workflow milestone.

### Problems Encountered

No major implementation problems were encountered during this milestone.
Care was required when extending the existing AuditLog model because audit records previously referenced only applications.
The audit model and logging service were updated so that incident records could also be referenced without affecting the existing application audit functionality.
The incident creation form was deliberately kept separate from the later workflow fields to prevent users from bypassing the intended incident lifecycle.

### Outcome

Milestone 4 was completed successfully.
The system now provides a functional incident register with:
Application-linked incidents
Automatically generated incident numbers
Incident titles and descriptions
Priority classification
Default New status
Reporting user tracking
Incident list and detail pages
Incident reporting by authenticated users
Audit logging for incident creation
Automated incident tests
The incident management functionality now provides the foundation required for the controlled workflow in the next milestone.
The next stage will implement the permitted incident lifecycle:
New → Assigned → In Progress → Resolved → Closed
Milestone 5 will also enforce valid transitions, assignment requirements and resolution requirements rather than allowing incident states to be changed freely.