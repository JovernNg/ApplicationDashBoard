# Performance Test Results

Date: 24 September 2026

System:
Application Operations and Incident Management Dashboard

## Objective

The purpose of performance testing is to evaluate whether the main application pages meet the defined local response-time target of less than 2 seconds.

## Test Environment

Operating System:
Windows

Python:
3.14.5

Django:
5.2.17

Database:
SQLite

Application Server:
Django development server / Django test client

Test Location:
Local machine

Number of measured requests per page:
5

Warm-up:
One unrecorded request before measurement

## Performance Target

Main application pages should respond in less than:

2000 ms

within the controlled local test environment.

## Results

| Page | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Average | Median | Maximum | Result |
|------|------:|------:|------:|------:|------:|--------:|-------:|--------:|--------|
| Dashboard | | | | | | | | | |
| Application List | | | | | | | | | |
| Application Detail | | | | | | | | | |
| Incident List | | | | | | | | | |
| Incident Detail | | | | | | | | | |

## Method

Response time was measured using Python's high-resolution performance timer and Django's test client.

One warm-up request was made before the recorded measurements.

Five requests were then measured for each page.

Average, median, minimum and maximum response times were calculated.

## Limitations

The measurements represent server-side response performance in a controlled local environment.

They do not represent public internet latency, production server load or performance with a large production dataset.

Client-side rendering and external resources such as Chart.js are not fully represented by Django test-client timing.

## Result

Complete after measurements have been collected.