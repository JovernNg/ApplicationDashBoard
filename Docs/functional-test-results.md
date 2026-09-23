# Functional Test Results

Date: 24 September 2026
System: Application Operations and Incident Management Dashboard
Environment: Local Development Environment
Framework: Django 5.2.17
Database: SQLite

## Purpose

The purpose of functional testing is to verify that the completed system behaves according to the defined functional requirements and workflow rules.

Testing covers authentication, application management, incident management, incident workflow, operational updates, SLA functionality, dashboard functionality and search/filtering.

## Test Environment

Application server:
Django development server

Database:
SQLite

Browser:
Record browser used during manual testing

Operating system:
Windows

## Functional Test Cases

| ID | Test | Expected Result | Actual Result | Status |
|----|------|-----------------|---------------|--------|
| FT-01 | Access dashboard without login | User is redirected to login | | |
| FT-02 | Administrator creates application | Application created successfully | | |
| FT-03 | Operations User attempts to create application | HTTP 403 returned | | |
| FT-04 | Operations User reports incident | Incident created in New state | | |
| FT-05 | Administrator assigns incident | Incident changes from New to Assigned | | |
| FT-06 | Assigned user starts investigation | Incident changes from Assigned to In Progress | | |
| FT-07 | Resolve incident without resolution notes | Validation prevents resolution | | |
| FT-08 | Resolve incident with resolution notes | Incident changes to Resolved and timestamp recorded | | |
| FT-09 | Close resolved incident | Incident changes to Closed and closure timestamp recorded | | |
| FT-10 | Unassigned operator attempts incident transition | HTTP 403 returned | | |
| FT-11 | Assigned operator adds incident update | Update appears in timeline | | |
| FT-12 | Incident update created | Audit record is generated | | |
| FT-13 | Search incident by title | Matching incident is returned | | |
| FT-14 | Filter incidents by priority | Only matching incidents displayed | | |
| FT-15 | Filter unassigned incidents | Only unassigned incidents displayed | | |
| FT-16 | View dashboard | Current application and incident statistics displayed | | |
| FT-17 | View application status chart | Chart displays application status distribution | | |
| FT-18 | View incident priority chart | Chart displays open incident priority distribution | | |
| FT-19 | View incident SLA information | Correct SLA state and deadline displayed | | |
| FT-20 | View Closed incident | Historical details remain available and no new update can be added | | |

## Automated Functional Testing

Automated functional workflow tests were executed using:

python manage.py test operations.tests.test_functional_flows -v 2

Complete regression testing was executed using:

python manage.py test

Record the final test count and result after execution.

## Result Summary

Total manual functional tests:
20

Passed:
To be completed after manual execution

Failed:
To be completed after manual execution

Automated tests:
Record final number after execution

Overall result:
To be completed after testing

## Notes

Do not mark a test as Passed until the behaviour has been manually verified.

Any defects identified during functional testing should be recorded together with the corrective action and the test should then be repeated.