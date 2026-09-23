# Security Test Results

Date: 24 September 2026

System:
Application Operations and Incident Management Dashboard

Environment:
Local development environment

Framework:
Django 5.2.17

Database:
SQLite


## Objective

The objective of security testing is to evaluate whether the application correctly enforces authentication, authorization, object-level access controls and common web application protections.

The testing does not attempt to prove that the system is completely free from security vulnerabilities.

Instead, it evaluates defined security controls and records the results observed within the tested environment.


## Security Test Cases

| ID | Test | Expected Result | Actual Result | Status |
|----|------|-----------------|---------------|--------|
| ST-01 | Access dashboard without authentication | Redirect to login | | |
| ST-02 | Access incident list without authentication | Redirect to login | | |
| ST-03 | Operations User opens application creation URL directly | HTTP 403 | | |
| ST-04 | Operations User opens application edit URL directly | HTTP 403 | | |
| ST-05 | Operations User opens Audit Log URL directly | HTTP 403 | | |
| ST-06 | Unassigned operator opens incident transition URL | HTTP 403 | | |
| ST-07 | Unassigned operator opens incident update URL | HTTP 403 | | |
| ST-08 | POST incident update without CSRF token | HTTP 403 and no update created | | |
| ST-09 | Store script payload in incident timeline | Payload displayed as escaped text and not executed | | |
| ST-10 | Submit SQL-injection-style search input | Treated as search data without query manipulation | | |
| ST-11 | Access protected page after logout | Redirect to login | | |
| ST-12 | Tamper with incident status during creation | Incident remains New | | |
| ST-13 | Tamper with incident assignee during creation | Incident remains unassigned | | |
| ST-14 | Tamper with reported user during creation | Current authenticated user remains reporter | | |
| ST-15 | Add update to Closed incident using direct POST | Update rejected | | |
| ST-16 | Change Incident using Django Admin | Modification denied | | |
| ST-17 | Change Application using Django Admin | Modification denied | | |
| ST-18 | Review Django Admin operational models | Records are view-only | | |
| ST-19 | OWASP ZAP passive scan | Findings recorded | | |
| ST-20 | OWASP ZAP active scan against local application | Findings recorded | | |


## Automated Security Testing

Dedicated security tests were executed using:

python manage.py test operations.tests.test_security -v 2

The complete regression suite was executed using:

python manage.py test

Record the final test count and result after testing.


## Authentication Testing

Protected operational pages were tested without an authenticated user session.

Unauthenticated requests are expected to redirect to the login page.


## Authorization Testing

Administrator-only functions were accessed while authenticated as an Operations User.

These tests include application management and access to the Audit Log.

The expected result is HTTP 403 Forbidden.


## Object-Level Authorization Testing

An incident assigned to one Operations User was accessed by another Operations User using manually constructed URLs.

The expected result is HTTP 403 Forbidden for modification functions.


## CSRF Testing

A Django test client with CSRF enforcement enabled was used to submit a state-changing POST request without a CSRF token.

The expected result is HTTP 403 and no database modification.


## XSS Testing

A stored script-style payload was added to an incident timeline entry.

The expected result is that the payload is HTML-escaped when rendered and no script executes.


## SQL Injection Style Testing

Injection-style text was submitted through the incident search functionality.

The expected behaviour is that the supplied input is treated as ordinary search text.

This test does not demonstrate the absence of every possible SQL injection vulnerability.


## Parameter Tampering Testing

Additional protected fields were manually supplied during incident creation.

The incident creation form should ignore these values.

Incident status, reporter and assignment state remain controlled by server-side application logic.


## Session Testing

An authenticated session was logged out and protected pages were then requested again.

The expected behaviour is redirection to the login page.


## Administrative Interface Hardening

Operational domain records are configured as read-only within Django Admin.

This prevents the administrative interface from bypassing application workflow and audit controls.


## OWASP ZAP Testing

OWASP ZAP will be used against the locally hosted application.

Any alerts should be recorded by:

Alert name

Risk level

Affected URL

Description

Whether the alert is applicable to the prototype

Corrective action if required


## Overall Result

Automated security tests:
To be completed

Manual security tests:
To be completed

ZAP findings:
To be completed

Overall assessment:
To be completed after testing