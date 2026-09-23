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

### Milestone 5 - Controlled Incident Workflow
Date: 23 September 2026
Status: Completed

### Objective

The objective of this milestone was to implement a controlled incident workflow so that incident status changes follow a defined sequence instead of allowing users to move freely between states.
The required incident lifecycle is:
New → Assigned → In Progress → Resolved → Closed
The workflow also introduces assignment rules, resolution requirements, automatic timestamps and role-based 
restrictions on who can modify an incident.

### Work Completed

Created a dedicated workflow service in operations/services/workflow.py.
Defined the valid incident status transitions.
Configured the allowed workflow as:
New → Assigned
Assigned → In Progress
In Progress → Resolved
Resolved → Closed
Closed → No further transition
Created reusable workflow functions for incident assignment and status transition.
Added validation to prevent incidents from skipping workflow states.
Added validation requiring an assigned user before an incident can enter the Assigned state.
Configured assignment of a New incident to automatically change its status to Assigned.
Added validation requiring resolution notes before an incident can move to Resolved.
Configured the system to automatically record the resolved timestamp when an incident is resolved.
Configured the system to automatically record the closed timestamp when an incident is closed.
Prevented Resolved and Closed incidents from being reassigned.
Created incident-level permission logic for workflow actions.
Configured Administrators to manage any incident.
Configured Operations Users to manage only incidents assigned to them.
Created an IncidentAssignmentForm.
Created an IncidentTransitionForm.
Restricted the transition form so that users can only select the next permitted workflow state.
Configured the transition form to display Resolution Notes only when the next valid status is Resolved.
Created an Administrator-only incident assignment page.
Created an incident status transition page.
Updated the incident detail page to display assignment and status update controls.
Configured the incident detail page to hide workflow controls when the current user does not have permission to perform the action.
Updated the incident detail page to display:
Assigned user
Resolved timestamp
Resolution notes
Closed timestamp
Extended the audit trail with Incident Assigned and Incident Status Changed actions.
Configured incident assignment to create an audit record.
Configured incident status transitions to create audit records.
Added automated workflow tests.

### Design Decisions

A dedicated workflow service was created instead of placing all status logic directly in the Django views.
This separates the workflow rules from the user interface and makes the rules reusable and easier to test.
The permitted workflow is intentionally linear:
New → Assigned → In Progress → Resolved → Closed
Users cannot skip intermediate states.
For example, an Assigned incident cannot move directly to Resolved.
This ensures that incident handling follows the intended operational process.
The Administrator is responsible for assigning incidents.
Operations Users cannot assign incidents themselves.
Once an incident has been assigned, the assigned Operations User can progress the incident through the workflow.
An Operations User who is not assigned to the incident cannot modify its workflow state.
This restriction is enforced on the server side and is not based only on whether a button is visible.
Resolution notes are required before an incident can enter the Resolved state.
This ensures that a resolution record exists before the incident is considered resolved.
The resolved and closed timestamps are generated automatically by the system rather than entered manually by users.
This reduces the possibility of inconsistent or inaccurate workflow timestamps.
Workflow Behaviour
A newly reported incident begins in the New state.
At this stage, the incident has no assigned user.
An Administrator assigns the incident to a user.
The assignment automatically changes the incident from:
New → Assigned
The assigned Operations User can then change the incident from:
Assigned → In Progress
Once investigation and remediation are complete, the assigned user can change the incident from:
In Progress → Resolved
Resolution notes must be entered before this transition is accepted.
When the incident becomes Resolved, the system automatically records the resolved timestamp.
The final permitted transition is:
Resolved → Closed
When this occurs, the system automatically records the closed timestamp.
A Closed incident has no further permitted transitions.
Access Control
Administrators can assign incidents.
Administrators can manage incident workflow for any incident.
Operations Users cannot assign incidents.
Operations Users can modify the workflow only when the incident is assigned to them.
Operations Users who are not assigned to the incident receive an HTTP 403 response if they attempt to access the transition function directly.
Logged-out users cannot access workflow functions.
These controls are enforced through server-side permission checks.

### Testing Performed

The following workflow behaviours were tested:
An Administrator can assign an incident.
Assigning a New incident automatically moves it to Assigned.
The assigned user is stored correctly.
An Operations User cannot assign an incident.
The assigned Operations User can move an incident from Assigned to In Progress.
A different Operations User cannot change the incident status.
An incident cannot skip directly from Assigned to Resolved.
An incident cannot skip required workflow stages.
Resolution notes are required before an incident can be resolved.
Submitting an empty resolution note is rejected.
Resolving an incident automatically records the resolved timestamp.
Resolution notes are stored with the incident.
A Resolved incident can move to Closed.
Closing an incident automatically records the closed timestamp.
A Closed incident cannot move to another status.
Incident assignment generates an audit record.
Incident status changes generate audit records.
The Milestone 5 workflow tests were executed using:
python manage.py test operations.tests.test_workflow -v 2
The full project test suite was executed using:
python manage.py test
The tests completed successfully with an OK result.
Audit Trail Integration
Two additional audit actions were introduced:
Incident Assigned
Incident Status Changed
When an Administrator assigns an incident, the audit trail records the incident, application, user performing the assignment, assigned username, action and timestamp.
If assignment changes a New incident to Assigned, a separate Incident Status Changed audit entry is also generated.
Status transitions are also recorded.
For example:
Incident status changed from Assigned to In Progress.
Another example is:
Incident status changed from In Progress to Resolved.
This provides a historical record of the incident lifecycle.

### Problems Encountered

During testing of the incident transition functionality, Django returned a TemplateDoesNotExist error for:
operations/incident_transition_form.html
The transition view and URL were functioning correctly, but the corresponding template file had not been created in the expected template directory.
The missing file was created at:
templates/operations/incident_transition_form.html
After creating the template, the transition page loaded successfully and workflow testing continued normally.

### Security Considerations

Workflow validation is implemented within the server-side workflow service.
This means invalid transitions cannot be performed simply by modifying the browser interface or manually submitting a different status value.
The system checks the current incident state against the defined list of permitted transitions.
Object-level access control is also applied to workflow changes.
An Operations User can only manage an incident when the incident is assigned to that user.
This provides stronger access control than simply hiding management controls from the interface.

### Outcome

Milestone 5 was completed successfully.
The system now provides a controlled incident lifecycle with:
Sequential workflow enforcement
Administrator-controlled assignment
Assigned-user workflow permissions
Prevention of invalid status changes
Mandatory resolution notes
Automatic resolved timestamps
Automatic closed timestamps
Workflow audit logging
Object-level access restrictions
Automated workflow tests
The incident management functionality now enforces business rules rather than allowing unrestricted status changes.
The next milestone will implement the SLA engine, including priority-based SLA targets, deadline calculation, At Risk thresholds and SLA breach detection.

### Milestone 6 - SLA Engine
Date: 23 September 2026
Status: Completed

### Objective

The objective of this milestone was to implement a Service Level Agreement (SLA) calculation engine for incidents.
The SLA engine determines how long an incident has been open relative to its priority-based target and classifies the incident as Within SLA, At Risk or Breached.
The SLA logic also stops counting elapsed time once an incident reaches the Resolved state.

### Work Completed

Created a dedicated SLA service in operations/services/sla.py.
Defined the following SLA targets:
Critical = 2 hours
High = 4 hours
Medium = 8 hours
Low = 24 hours
Created reusable functions to calculate:
SLA target duration
SLA deadline
SLA reference time
SLA status
SLA elapsed percentage
Configured the SLA deadline to be calculated from the incident reporting timestamp.
Configured SLA calculations to use calendar time rather than business hours.
Implemented the following SLA status rules:
Below 75% elapsed = Within SLA
Exactly 75% elapsed = At Risk
Between 75% and less than 100% elapsed = At Risk
Exactly 100% elapsed = Breached
Above 100% elapsed = Breached
Configured the SLA clock to stop when the incident reaches Resolved.
Configured resolved incidents to continue displaying the SLA state that existed at the resolution time instead of continuing to accumulate elapsed time.
Added SLA information to the incident list page.
Added SLA information to the incident detail page.
Added SLA target display.
Added SLA deadline display.
Added SLA status badges.
Added an SLA elapsed progress indicator.
Added automated SLA tests for priority targets, thresholds, deadline handling and resolution-time behaviour.

### Design Decisions

The SLA information is calculated dynamically instead of being stored as duplicated database values.
The system already stores the incident priority, reporting timestamp and resolution timestamp, so the SLA deadline and status can be derived from those values.
This avoids storing data that could become inconsistent with the incident record.
The SLA rules are implemented in a dedicated service rather than directly inside the Django views.
This allows the calculations to be reused by the incident list, incident detail page, dashboard and future reporting functionality.
The SLA target is selected according to incident priority.
The defined targets are:
Critical = 2 hours
High = 4 hours
Medium = 8 hours
Low = 24 hours
The At Risk threshold is defined as 75% of the SLA target.
The implementation uses an inclusive threshold.
This means that an incident becomes At Risk exactly when 75% of its available SLA time has elapsed.
The deadline check is also inclusive.
This means that an incident is classified as Breached exactly when the SLA deadline is reached rather than only after the deadline has passed.
SLA Calculation Behaviour
For a Critical incident with a two-hour SLA target:
Reported at 20:00
75% threshold = 21:30
SLA deadline = 22:00
From 20:00 until before 21:30, the incident is classified as Within SLA.
At exactly 21:30, the incident becomes At Risk.
Between 21:30 and before 22:00, the incident remains At Risk.
At exactly 22:00, the incident becomes Breached.
The incident remains Breached after the deadline unless it was resolved earlier.
Resolution-Time Behaviour
The SLA clock stops when an incident reaches Resolved.
For example, if a Critical incident is reported at 20:00 and resolved at 21:00, the elapsed SLA time is one hour out of a two-hour target.
The incident therefore remains:
50% elapsed
Within SLA
If the same incident is viewed several hours later, the elapsed percentage remains 50% because the SLA reference time is the recorded resolution timestamp.
If the incident is resolved at 21:45, the elapsed percentage is approximately 87.5%.
The incident is therefore classified as At Risk.
If the incident is resolved exactly at 22:00, the incident is classified as Breached because the SLA deadline has been reached.

### User Interface Changes

The incident list was updated to display the SLA condition for each incident.
The SLA states are displayed using visual badges:
Within SLA
At Risk
Breached
The incident list also displays the calculated SLA deadline.
The incident detail page was updated to display:
SLA target
SLA deadline
SLA status
SLA elapsed percentage
SLA progress indicator
The progress bar provides a visual representation of the percentage of the SLA target that has elapsed.
SLA Progress Indicator
The first version of the SLA progress indicator displayed a Bootstrap progress bar using the calculated SLA percentage.
During testing, a newly created incident showed an almost empty progress bar.
This initially appeared to be a display issue, but the calculated value was correct because only a very small percentage of the SLA target had elapsed.
The interface was improved so that the numeric elapsed percentage is displayed above the progress bar.
This allows the user to see the exact SLA elapsed value even when the filled section of the bar is very small.
The interface also displays the SLA target duration beside the elapsed percentage.
For example:
0.1% elapsed
2 hour target
CSS Template Validation Issue
While implementing the SLA progress bar, VS Code reported the following CSS validation warning:
property value expected css(css-propertyvalueexpected)
The warning was caused by Django template syntax being used directly inside an inline CSS width value.
The original approach used a value similar to:
style="width: {{ sla_progress }}%;"
Django could render this correctly in the browser, but the VS Code CSS validator could not interpret the Django template expression.
The implementation was changed to store the calculated percentage in a custom HTML data attribute.
JavaScript then reads the value and applies it to the progress bar width.
This removed the CSS validation warning while retaining the dynamic progress behaviour.
The JavaScript also constrains the displayed progress value between 0% and 100%.

### Testing Performed

The following SLA behaviours were tested:
Critical incidents have a two-hour SLA target.
High incidents have a four-hour SLA target.
Medium incidents have an eight-hour SLA target.
Low incidents have a twenty-four-hour SLA target.
The SLA deadline is calculated correctly from the reported timestamp.
An incident below 75% elapsed is classified as Within SLA.
An incident at exactly 75% elapsed is classified as At Risk.
An incident above 75% but below the deadline remains At Risk.
An incident at exactly the SLA deadline is classified as Breached.
An incident after the SLA deadline is classified as Breached.
The SLA clock stops when the incident reaches Resolved.
A resolved incident does not later become Breached simply because more real time passes.
A resolved incident preserves its SLA status based on the resolution timestamp.
The SLA progress percentage is calculated correctly.
The automated SLA tests were executed using:
python manage.py test operations.tests.test_sla -v 2
The complete project test suite was executed using:
python manage.py test
The tests completed successfully with an OK result.
Security and Data Integrity Considerations
Users do not manually enter SLA deadlines or SLA statuses.
The SLA deadline is calculated by the system using the incident priority and reporting timestamp.
The SLA status is also calculated by the system.
This prevents users from manually altering an incident's SLA classification.
Resolution timestamps are generated by the controlled incident workflow rather than entered manually through the incident creation interface.
This means the SLA engine relies on timestamps that are generated by the system-controlled workflow.

### Problems Encountered

A display issue was identified with the SLA elapsed progress bar.
When an incident had only just been created, the elapsed percentage was very close to zero and the progress bar appeared empty.
The underlying calculation was correct, but the display did not clearly communicate the small percentage.
The incident detail interface was updated to show the numeric elapsed percentage separately from the progress bar.
A second issue involved the VS Code CSS validator reporting an error when Django template syntax was placed directly inside an inline CSS width value.
The progress bar implementation was changed to use a data attribute and JavaScript to apply the width after the page loads.
After this change, the progress bar displayed correctly and the CSS validation warning was removed.

### Outcome

Milestone 6 was completed successfully.
The system now provides priority-based SLA calculations with:
Critical two-hour target
High four-hour target
Medium eight-hour target
Low twenty-four-hour target
Automatic SLA deadline calculation
Within SLA classification
At Risk classification
Breached classification
75% At Risk threshold
Exact-deadline breach handling
Resolution-time clock stopping
SLA status display in the incident register
SLA information on the incident detail page
Visual SLA progress indication
Automated SLA boundary tests
The SLA engine now provides the logic required for dashboard breach counts and future SLA-focused reporting.
The next milestone will implement the incident update timeline so that users can record chronological operational updates against an incident.

### Milestone 7 - Incident Updates and Timeline
Date: 23 September 2026
Status: Completed

### Objective

The objective of this milestone was to implement a chronological incident update timeline so that operational users can record ongoing investigation and recovery activity against an incident.
The timeline is intended to provide a clear history of operational actions taken during the incident lifecycle.
Each update records:
Incident
User
Update text
Timestamp

### Work Completed

Created the IncidentUpdate database model.
Added fields for:
Incident
User
Operational update text
Creation timestamp
Configured incident updates to be linked to an Incident record.
Configured each update to record the user who created it.
Configured the update timestamp to be generated automatically by the system.
Created and applied the database migration for the IncidentUpdate model.
Created an IncidentUpdateForm.
Restricted the update form so that users only enter the operational update text.
Configured the system to determine the incident, user and timestamp automatically.
Created an incident update creation page.
Added an Add Update control to the incident detail page.
Added an Incident Timeline section to the incident detail page.
Configured updates to be displayed in chronological order.
Configured the timeline to display:
Username
Timestamp
Operational update text
Added permissions so that only authorised users can add updates.
Configured Administrators to add updates to any active incident.
Configured Operations Users to add updates only to incidents assigned to them.
Configured unassigned Operations Users to receive HTTP 403 when attempting to add an update directly.
Prevented updates from being added to Closed incidents.
Added a new audit action:
Incident Update Added
Configured each operational update to generate an audit record.
Registered IncidentUpdate with Django Admin.
Configured IncidentUpdate records as read-only in Django Admin.
Added automated tests for incident update creation, permissions, timeline display and audit logging.

### Design Decisions

Incident updates were implemented as separate database records rather than storing a single update field within the Incident model.
This allows each incident to contain multiple timestamped operational updates and preserves the sequence of actions taken during investigation and recovery.
The IncidentUpdate model has a many-to-one relationship with Incident.
This means one incident can contain multiple update records.
The update text is entered by the authorised user, while the related incident, username and timestamp are generated by the system.
This prevents users from manually altering the ownership or timestamp of a timeline entry.
Updates are displayed chronologically from oldest to newest.
This was selected because it allows the timeline to be read naturally as the incident progresses from initial investigation through remediation.
Access Control
Administrators can add operational updates to any incident that is not Closed.
Operations Users can add an operational update only when the incident is assigned to them.
An Operations User who is not assigned to the incident cannot create an update.
This restriction is enforced by server-side permission checking.
A user therefore cannot bypass the restriction by manually entering the update URL.
Closed incidents do not allow new operational updates.
The existing timeline remains visible after closure so that the incident history can still be reviewed.
Incident Timeline Behaviour
When an authorised user adds an update, the system performs the following process:
The update form is validated.
The current incident is associated with the update.
The logged-in user is recorded as the update author.
The update is stored in the database.
The creation timestamp is generated automatically.
The incident's last updated timestamp is refreshed.
An Incident Update Added audit record is created.
A success message is displayed.
The user is redirected to the incident detail page.
The new update appears within the Incident Timeline.
Example Timeline Behaviour
An assigned Operations User may initially add:
Investigated application logs. Multiple payment requests are failing when communicating with the external payment gateway.
A later update may contain:
Payment gateway connectivity has been restored. Transaction validation is currently in progress.
Both updates remain stored and are displayed in chronological order.
The timeline therefore provides an operational history of the incident rather than only displaying its current state.
Audit Trail Integration
The AuditLog action choices were extended with:
Incident Update Added
Whenever an operational update is created, an audit entry is generated.
The audit record includes:
User performing the action
Application related to the incident
Incident
Action
Timestamp
Audit details
An example audit detail is:
Operational update added to incident INC-20260923-0004.
This allows the audit trail to record both workflow actions and operational timeline activity.

### Testing Performed

The following incident timeline behaviours were tested:
An assigned Operations User can add an incident update.
An Administrator can add an incident update.
An Operations User who is not assigned to the incident cannot add an update.
An unauthorised Operations User receives HTTP 403.
A logged-out user cannot access the update creation page.
An empty operational update is rejected.
A valid update is stored in the IncidentUpdate table.
The update records the correct incident.
The update records the correct user.
The update timestamp is generated automatically.
The incident detail page displays timeline updates.
Multiple updates are displayed in chronological order.
Creating an update generates an Incident Update Added audit record.
A Closed incident rejects new operational updates.
Existing updates remain visible after incident closure.
The Milestone 7 update tests were executed using:
python manage.py test operations.tests.test_incident_updates -v 2
The complete project test suite was executed using:
python manage.py test
The tests completed successfully with an OK result.

### Problems Encountered

Incident Detail Template Syntax Error
While adding the Incident Timeline section to the incident detail page, Django returned a TemplateSyntaxError.
The error reported:
Invalid block tag: 'endfor', expected 'endblock'
This indicated that the Django template control tags were not correctly paired.
The issue was caused by an incorrect for-loop structure within the timeline section.
The incident detail template was replaced with a corrected version containing properly matched:
{% if %}
{% for %}
{% endfor %}
{% else %}
{% endif %}
tags.
After correcting the template structure, the incident detail page loaded normally and displayed the timeline correctly.

### Missing Manual Test User

During manual access-control testing, the operator2 user account did not exist in the normal development database.
The automated tests created operator2 dynamically within Django's temporary test database, so the account was available during automated testing but not during normal browser testing.
A second Operations User account was therefore created manually for development testing and added to the Operations User group.
This allowed the object-level access rule to be tested manually by assigning an incident to operator1 and attempting to modify it while logged in as operator2.
The manual test confirmed that an unassigned Operations User receives HTTP 403 when attempting to add an incident update.

### Security Considerations

Incident timeline entries cannot be created anonymously.
The user associated with an update is determined from the authenticated session rather than from user-submitted form data.
The timestamp is generated automatically by Django.
The incident relationship is determined by the requested incident URL and is not entered manually in the update form.
This prevents the user from directly selecting a different incident identifier within the form.
Object-level permission checks prevent Operations Users from updating incidents that are assigned to another user.
Django's default template escaping is retained when displaying update text.
This will also support later cross-site scripting testing within the security testing milestone.

### Data Integrity Considerations

Incident updates use a ForeignKey relationship to the Incident model.
If an incident is deleted, its related IncidentUpdate records are also removed through the configured CASCADE relationship.
The user relationship uses SET_NULL behaviour.
This means that if a user account is removed, the timeline record itself remains while the user reference becomes null.
This preserves the operational update history.

### Outcome

Milestone 7 was completed successfully.
The system now provides a chronological incident timeline with:
Multiple operational updates per incident
User attribution
Automatic timestamps
Assigned-user access control
Administrator access
Closed-incident restrictions
Timeline display on the incident detail page
Audit trail integration
Read-only historical records through Django Admin
Automated incident update tests
The incident module now provides both the current operational state and a chronological record of investigation and remediation activity.
The next milestone will implement the dashboard analytics functionality, including application health statistics, open incident counts, critical incident counts, SLA breach counts, recent incidents and visual charts.

### Milestone 8 - Dashboard Analytics

Date: 23 September 2026
Status: Completed

### Objective

The objective of this milestone was to transform the existing landing page into an operational dashboard that summarises the current state of applications, incidents and SLA performance.
The dashboard provides a single view of the information most relevant to operations users, including application health, open incident workload, critical incidents, SLA breaches and recent incident activity.

### Work Completed

Replaced the placeholder dashboard with a full operational dashboard.
Created six summary cards for:
Total Applications
Healthy Applications
Problem Applications
Open Incidents
Critical Incidents
SLA Breaches
Defined Problem Applications as applications with either Degraded or Down status.
Excluded Maintenance applications from the Problem Applications count.
Defined Open Incidents as incidents in the following states:
New
Assigned
In Progress
Excluded Resolved and Closed incidents from the Open Incidents count.
Configured the Critical Incidents card to count only open Critical incidents.
Configured the SLA Breaches card to count only open incidents that are currently classified as Breached by the SLA engine.
Added an Applications by Status chart.
Added an Open Incidents by Priority chart.
Integrated Chart.js into the dashboard.
Used Django's json_script functionality to safely transfer chart data from the server to JavaScript.
Added a Recent Incidents table.
Configured the Recent Incidents table to display the five most recently reported incidents.
Added links from the recent incident records to their corresponding incident detail pages.
Added SLA status badges to recent incident records.
Added application status data for:
Healthy
Degraded
Down
Maintenance
Added incident priority data for:
Critical
High
Medium
Low
Added automated tests for dashboard authentication, summary counts, SLA breach calculations, chart data and recent incidents.

### Design Decisions

The dashboard calculations are performed dynamically from the existing Application and Incident records rather than storing separate dashboard statistics in the database.
This avoids duplicated information and ensures that dashboard values reflect the current system state.
Problem Applications are defined as applications with either Degraded or Down status.
Maintenance was intentionally excluded because Maintenance represents a planned operating state and does not necessarily indicate an unexpected application problem.
Open Incidents are defined as incidents in the following workflow states:
New
Assigned
In Progress
Resolved and Closed incidents are excluded because they are no longer considered active operational workload.
The Critical Incidents summary card counts only open incidents with Critical priority.
This means that a Critical incident that has already been Resolved or Closed does not contribute to the current operational critical incident count.
The SLA Breaches card also focuses on current operational workload.
Only open incidents that are currently classified as Breached are included in the count.
Historical incidents that previously breached but have since been Resolved or Closed are not included in this dashboard metric.
This was chosen because the dashboard is intended to represent the current operational situation rather than historical SLA reporting.
Dashboard Summary Cards
The dashboard displays six summary cards.
Total Applications shows the total number of applications registered in the system.
Healthy Applications shows the number of applications currently in Healthy status.
Problem Applications shows the combined number of Degraded and Down applications.
Open Incidents shows the number of incidents currently in New, Assigned or In Progress status.
Critical Incidents shows the number of open incidents with Critical priority.
SLA Breaches shows the number of open incidents whose SLA status is currently Breached.
These summary cards provide a rapid overview of the current operational environment.
Applications by Status Chart
A doughnut chart was added to display the distribution of applications across the available operational states.
The chart displays:
Healthy
Degraded
Down
Maintenance
The values are calculated from the current Application records.
This provides a visual summary of application health across the registered application estate.
Open Incidents by Priority Chart
A bar chart was added to display the number of open incidents grouped by priority.
The priority categories are:
Critical
High
Medium
Low
Only incidents in New, Assigned or In Progress status are included.
Resolved and Closed incidents are excluded.
This allows operations users to quickly understand the current incident workload by severity.
Recent Incidents
A Recent Incidents table was added to the dashboard.
The table displays the five most recently reported incidents.
For each incident, the dashboard displays:
Incident number
Application
Title
Priority
Status
SLA status
Reported timestamp
The incident number links directly to the incident detail page.
This allows users to quickly move from the dashboard summary into the detailed incident record.
SLA Integration
The dashboard reuses the SLA calculation service implemented in Milestone 6.
Each recent incident is evaluated using the existing SLA logic.
The SLA status displayed is one of:
Within SLA
At Risk
Breached
The SLA Breaches summary card uses the same SLA service to count currently open incidents that have exceeded their SLA deadline.
This avoids duplicating SLA calculation logic inside the dashboard.
Chart Data Handling
Chart.js was used to render the dashboard charts.
The application status labels and counts are generated in the Django view.
The incident priority labels and counts are also generated in the Django view.
Django's json_script template feature is used to transfer these values safely into JavaScript.
This approach was selected instead of directly inserting Python or Django values into JavaScript strings.
It provides a cleaner separation between server-side calculations and client-side chart rendering.
User Interface Changes
The previous placeholder dashboard was replaced with a structured layout containing:
Six summary cards
Two analytical charts
A recent incidents table
Bootstrap cards and responsive grid classes were used to keep the dashboard readable on different screen sizes.
Dark text is used on the light dashboard cards to avoid the contrast issue encountered earlier in the project.
Application and incident status information is supported by Bootstrap badges and border colours to make operational conditions easier to distinguish visually.

### Testing Performed

The following dashboard behaviours were tested:
The dashboard requires authentication.
Logged-out users are redirected to the login page.
The total application count is calculated correctly.
The Healthy Applications count is calculated correctly.
The Problem Applications count includes Degraded and Down applications.
Maintenance applications are excluded from the Problem Applications count.
The Open Incidents count includes New, Assigned and In Progress incidents.
Resolved incidents are excluded from the Open Incidents count.
Closed incidents are excluded from the Open Incidents count.
The Critical Incidents count includes only open Critical incidents.
The SLA Breaches count includes open incidents whose SLA status is Breached.
The Recent Incidents section displays recent incident records.
The application status chart receives the correct application status data.
The incident priority chart receives the correct open incident priority data.
The Milestone 8 dashboard tests were executed using:
python manage.py test operations.tests.test_dashboard -v 2
The complete project test suite was executed using:
python manage.py test
The tests completed successfully with an OK result.

### Problems Encountered

Missing Administrator Test View
After modifying operations/views.py during dashboard development, Django returned an AttributeError stating that:
operations.views had no attribute administrator_test
The URL configuration still referenced the Administrator test view created during Milestone 1, but the function had been accidentally removed from the views file during later edits.
The administrator_test view was restored.
This preserved the original Administrator permission test page and maintained compatibility with the existing Milestone 1 permission tests.
Dashboard Returned None
After restoring the Administrator test view, accessing the dashboard returned the following error:
The view operations.views.dashboard didn't return an HttpResponse object. It returned None instead.
The issue occurred because the dashboard function did not reach a valid return render(...) statement after the previous edits.
The dashboard and Administrator test functions were reorganised so that the dashboard function ended with:
return render(...)
before the separate administrator_test view definition began.
After correcting the function structure, the dashboard loaded normally.
Security and Data Integrity Considerations
The dashboard requires an authenticated user session.
Dashboard statistics are derived from database queries rather than being accepted from user input.
The SLA breach count reuses the existing server-side SLA calculation logic.
Chart values are transferred to JavaScript using Django's json_script functionality.
This avoids manually constructing JavaScript from unescaped template values.
The dashboard does not provide direct modification functionality.
Users must navigate to the relevant application or incident pages to perform authorised management actions.
Performance Considerations
The dashboard performs several aggregate database queries to calculate application and incident statistics.
Related application, reporting user and assigned user information is retrieved using select_related for incident data.
This reduces unnecessary database queries when displaying recent incident information.
The dashboard currently calculates SLA breach status dynamically for open incidents.
This approach is appropriate for the current prototype dataset and will be evaluated further during the performance testing milestone.

### Outcome

Milestone 8 was completed successfully.
The system now provides a functional operational dashboard containing:
Total application count
Healthy application count
Problem application count
Open incident count
Open Critical incident count
Current SLA breach count
Applications by Status chart
Open Incidents by Priority chart
Recent Incidents table
Recent incident SLA status
Links to detailed incident records
The dashboard now provides a central operational overview of the system rather than acting only as a navigation page.
The next milestone will implement incident search and filtering so that users can locate incidents by incident number, title or description and filter records by application, priority, status and assigned user.

# Milestone 9 - Incident Search and Filtering

**Date:** 24 September 2026  
**Status:** Completed

### Objective

The objective of this milestone was to improve incident management by allowing authenticated users to search and filter incident records efficiently.
The incident list previously displayed all incidents without any method to narrow down the results.
This milestone introduced search functionality and multiple filters so users can locate specific incidents or subsets of incidents more quickly.

### Work Completed

Added incident search functionality to the incident list page.
Configured search to check the following fields:
Incident number
Incident title
Incident description
Configured the search to be case-insensitive.
Added filtering by application.
Added filtering by incident priority.
Added filtering by incident status.
Added filtering by assigned user.
Added support for filtering incidents that are currently unassigned.
Allowed multiple filters to be combined together.
Configured the selected search and filter values to remain visible after the form is submitted.
Added a Clear button to reset all search and filter parameters.
Added a result count showing the number of incidents matching the current criteria.
Preserved existing SLA status and SLA deadline information within the filtered incident results.
Added automated tests for search behaviour, individual filters, combined filters and invalid query-string values.

### Search Behaviour
The incident search field checks multiple incident attributes using Django Q objects.
The search checks:
Incident number
Title
Description
The search uses case-insensitive matching.
This means a user can enter partial search terms rather than requiring an exact match.
For example:
payment
Payment
PAYMENT
can all return incidents containing the same matching text.
A partial incident number can also be used to locate an incident.
For example:
INC-202609
can match incidents whose generated incident numbers contain that value.

### Search Implementation

The search functionality was implemented using Django ORM Q objects.
The query combines multiple fields using OR conditions.
The logic is:
Incident number contains search term
OR
Title contains search term
OR
Description contains search term
This allows one search field to cover multiple incident attributes.
The use of the Django ORM avoids constructing raw SQL queries manually.

### Application Filtering

An Application dropdown was added to the incident search form.
The dropdown contains registered applications ordered by application name.
When an application is selected, only incidents associated with that application are displayed.
The application identifier is passed through the query string and validated before being applied to the query.

### Priority Filtering
A Priority dropdown was added.
The available values are taken directly from the Incident Priority choices defined in the model.
The available values are:
Critical
High
Medium
Low
Only valid priority values are applied to the database query.
Invalid priority values are ignored rather than causing the incident list page to fail.

### Status Filtering

A Status dropdown was added.
The filter uses the workflow states defined in the Incident model.
The available values include:
New
Assigned
In Progress
Resolved
Closed
Only incidents matching the selected status are displayed.
Invalid status values are ignored safely.

### Assigned User Filtering

An Assigned User dropdown was added.
Users who are currently assigned to at least one incident are included in the dropdown.
The list is ordered by username.
An additional Unassigned option was included.
Selecting Unassigned displays incidents where the assigned user field is null.
This allows Administrators and Operations Users to identify incidents that still require assignment.

### Combined Filtering

The search and filter options can be used together.
For example, a user may search for:
payment
while also selecting:
Application: Payment Portal
Priority: Critical
Status: In Progress
Assigned User: operator1
The filtering logic applies the selected criteria using AND behaviour.
This means the incident must satisfy all selected filters.
The search field itself still uses OR logic internally across incident number, title and description.
The overall behaviour is therefore:
Search match
AND
Application match
AND
Priority match
AND
Status match
AND
Assigned User match

### Filter State Preservation

After submitting the search form, the current search text and selected filters remain displayed.
This allows the user to see the criteria responsible for the current result set.
The selected values are passed back to the template through the view context.
The incident list template compares the current query-string values with each available dropdown option and marks the matching option as selected.

### Clear Search and Filters

A Clear button was added next to the search submission button.
The Clear button links directly back to the incident list page without any query parameters.
This resets:
Search text
Application filter
Priority filter
Status filter
Assigned User filter
The full incident list is then displayed again.

### Result Count

A result counter was added above the incident table.
The counter displays the number of incidents matching the current search and filter criteria.
For example:
1 result
or
4 results
This provides immediate feedback about the effect of the selected filters.

### No Results Behaviour

If no incidents match the current search or filter criteria, the table displays a message instead of remaining empty.
The message states:
No incidents match the current search or filters.
This makes it clear that the system has successfully processed the request but no matching records were found.
### SLA Integration
The existing SLA functionality from Milestone 6 was preserved.
Each incident displayed after search or filtering still contains:
SLA status
SLA deadline
The SLA status is calculated dynamically using the existing SLA service.
The possible displayed states remain:
Within SLA
At Risk
Breached
This confirms that introducing search and filtering did not remove or duplicate existing SLA logic.

### Security Considerations

The incident list remains restricted to authenticated users.
The search and filtering functionality is read-only and does not directly modify incident data.
Query parameters are processed using the Django ORM.
Raw SQL queries are not constructed manually.
Application identifiers and assigned user identifiers are checked before filtering.
Priority and status values are validated against the defined model choices before being applied.
Invalid search-filter values are ignored rather than raising an application error.
This behaviour was tested automatically.

### Data Integrity Considerations

No database schema changes were required for this milestone.
Search and filtering operate only on existing incident and application data.
No new database records are created when users search or filter.
No existing incident records are modified.
Because no model fields were changed, no database migration was required.

### User Interface Changes

The incident list page was updated with a search and filter panel.
The panel contains:
Search field
Application dropdown
Priority dropdown
Status dropdown
Assigned User dropdown
Apply Search / Filters button
Clear button
The incident results table remains below the filter panel.
The incident table continues to display:
Incident number
Application
Title
Priority
Status
Assigned user
SLA status
SLA deadline
Reported timestamp
Incident numbers remain clickable links to the incident detail page.
Application names remain clickable links to the related application detail page.

### Testing Performed

Automated tests were added for the new search and filtering functionality.
The following behaviours were tested:
Search by incident title.
Search by incident description.
Search by incident number.
Filter by application.
Filter by priority.
Filter by status.
Filter by assigned user.
Filter by unassigned incidents.
Combined search and filtering.
Invalid query-string values do not crash the application.
The Milestone 9 tests were executed using:
python manage.py test operations.tests.test_search_filter -v 2
The complete project test suite was executed using:
python manage.py test
The tests completed successfully with an OK result.

### Search Test Example

Three incidents were created within the automated test environment.
One incident represented a Critical payment gateway failure.
One incident represented a High priority customer login issue.
One incident represented an unassigned Medium priority payment report delay.
Searching for:
gateway
returned only the payment gateway incident.
Searching for:
responding slowly
returned only the customer login incident.
This confirmed that title and description searching operated correctly.

### Application Filter Test

The automated test created incidents across two different applications.
Filtering by Payment Portal returned only incidents associated with the Payment Portal application.
Incidents associated with the Customer Portal were excluded.
This confirmed that application filtering used the correct application relationship.

### Assigned User Filter Test

Incidents were assigned to separate operator accounts.
Filtering by operator1 returned only incidents assigned to operator1.
Filtering using:
Unassigned
returned only incidents where no assigned user existed.
This confirmed that both normal assignment filtering and null assignment filtering worked correctly.

### Combined Filter Test

A combined test applied the following criteria:
Search: payment
Application: Payment Portal
Priority: Critical
Status: In Progress
Assigned User: operator1
Only the incident matching all selected criteria was returned.
This confirmed that multiple filters can be used simultaneously.

### Invalid Filter Handling

An automated test supplied invalid values for:
Application
Priority
Status
Assigned User
The incident list page still returned HTTP 200.
The invalid values were ignored rather than causing an exception.
This improves robustness when users manually modify query-string values in the browser.

### Problems Encountered

No major implementation errors were encountered during this milestone.
The primary consideration was ensuring that filtering did not remove the SLA data already calculated for the incident list.
To preserve this behaviour, the filtered QuerySet is evaluated first and then each returned incident is passed through the existing SLA calculation functions.
The existing SLA status labels and deadline values are attached to the result objects before they are sent to the template.
Another consideration was preventing malformed query-string values from causing invalid database lookups.
Numeric application and assigned-user filters are checked before use.
Priority and status values are checked against the model's available choices.
This ensured the page continued to load even when invalid values were supplied manually.

### Performance Considerations

Filtering is performed at the database level using Django QuerySets.
This means the system does not retrieve every incident and then filter the records in Python.
Application, priority, status and assigned-user conditions are converted into database query conditions.
Search conditions are also handled by the database.
The related Application, Reported User and Assigned User records continue to use select_related.
This reduces unnecessary additional database queries when rendering the incident results table.
The final result set is converted to a Python list only after database filtering has been applied.
SLA calculations are then performed only for the incidents that remain in the filtered result set.

### Outcome

Milestone 9 was completed successfully.
The incident management interface now supports:
Incident number search
Incident title search
Incident description search
Case-insensitive partial matching
Application filtering
Priority filtering
Status filtering
Assigned user filtering
Unassigned incident filtering
Combined search and filtering
Filter state preservation
Search and filter reset
Result count display
No-results feedback
Existing SLA status display
Existing SLA deadline display
Automated search and filtering tests
The incident list is now significantly easier to navigate when the number of incident records increases.
With Milestone 9 complete, the main planned user-facing functionality is implemented.
The next milestone will focus on systematic functional testing of the complete application, including authentication, role permissions, application management, incident workflows, SLA boundary behaviour, incident updates and dashboard functionality.