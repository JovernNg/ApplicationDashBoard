# Usability Test Plan

## Objective

The purpose of the usability evaluation is to assess whether users can complete common operational tasks using the Application Operations and Incident Management Dashboard.

The evaluation focuses on:

Task completion

Task completion time

User difficulties

Participant comments

Overall perceived usability using the System Usability Scale (SUS)

## Participants

Target:
3 to 5 volunteer participants

Participants will be identified using anonymous participant identifiers:

P1
P2
P3
P4
P5

No participant names should be included in the results table.

## Test Environment

Application:
Application Operations and Incident Management Dashboard

Environment:
Local development environment

Browser:
Record browser used

Device:
Desktop or laptop

## Instructions to Participants

Participants should attempt each task using the interface without being told exactly which control to select.

Assistance should only be provided if the participant is unable to continue.

Any assistance should be recorded in the observations.

Participants are evaluating the system interface rather than being personally evaluated.

## Tasks

### UT-01 - Login

Log into the system using the supplied account.

Success condition:
Dashboard is displayed.

### UT-02 - Identify Operational Status

Using the dashboard, identify:

The number of open incidents.

The number of Critical incidents.

Success condition:
Participant correctly identifies both values.

### UT-03 - Find an Incident

Locate the specified incident using the search and filtering functionality.

Success condition:
Participant reaches the correct incident detail page.

### UT-04 - Report an Incident

Create a new incident for the specified application using the supplied title, description and priority.

Success condition:
Incident is successfully created in New status.

### UT-05 - Review SLA Information

Open the specified incident and identify:

Priority

Current status

SLA deadline

SLA state

Success condition:
Participant correctly identifies the requested information.

### UT-06 - Add Operational Update

Add the supplied operational update to an incident assigned to the participant's account.

Success condition:
Update appears in the Incident Timeline.

### UT-07 - Update Incident Status

Move the assigned incident from Assigned to In Progress.

Success condition:
Incident status becomes In Progress.

## Measurements

For every task record:

Successful completion

Completion time

Errors or incorrect navigation

Whether assistance was required

Participant comments

Observer comments

## Post-Test Questionnaire

After completing the tasks, participants will complete the System Usability Scale questionnaire.

Additional optional feedback:

What did you find easiest?

What did you find most difficult?

Was anything confusing?

What would you improve?