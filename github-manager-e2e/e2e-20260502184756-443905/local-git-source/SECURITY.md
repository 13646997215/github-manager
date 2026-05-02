# Security Policy

## Scope
ROS2-Agent touches shell execution, validation automation, future gateway / cron integration, and robot-development workflows.

## Supported baseline
- Ubuntu 22.04
- ROS2 Humble
- Python 3.10+

## Reporting a vulnerability
Do not open public issues for security-sensitive problems.
Report privately with affected files, reproduction steps, and impact.

## Security priorities
- unsafe shell execution defaults
- destructive automation behavior
- credential leakage in docs, logs, or fixtures
- report/export pipelines exposing unintended local data
- unsafe future gateway / cron integrations
- unsafe assumptions around real-hardware control
