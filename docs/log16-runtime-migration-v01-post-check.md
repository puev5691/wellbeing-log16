# log16 runtime migration post-check

legacy_runtime: /data/wellbeing/obs/consultant/outbox/log16-kernel
target_runtime: /data/wellbeing/obs/log16
backup_runtime: /data/wellbeing/obs/consultant/outbox/log16-kernel.backup-0618-1926

legacy_is_symlink: YES
legacy_points_to: /data/wellbeing/obs/log16

target_files: 245
target_dirs: 115
backup_files: 245
backup_dirs: 96

critical files:
OK: /data/wellbeing/obs/log16/bin/log16-pult
OK: /data/wellbeing/obs/log16/bin/log16-pult.py
OK: /data/wellbeing/obs/log16/bin/log16-dashboard.py
OK: /data/wellbeing/obs/log16/bin/log16-agent-runner.py
OK: /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-pult
OK: /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-dashboard.py

pult status via compatibility path:
# log16 pult status

Created: 2026-06-18T19:26:35

## Counts

- themes_captured: 3
- tasks_proposed: 0
- tasks_routed: 0
- tasks_dispatched: 6
- tasks_done: 1
- requests_pending: 0
- requests_done: 10
- requests_failed: 0
- responses_needs_review: 10
- responses_failed: 0
- runner_reports: 4

## Pending source cases

- none

## Meaning

- tasks_proposed: задачи ещё не разобраны triage.
- tasks_routed: задачи ждут dispatch; если они уже отработаны, запусти cleanup.
- tasks_dispatched: задачи уже превратились в requests/responses.
- requests_pending: есть что запускать runner.
- responses_needs_review: есть ответы Сущностей, требующие review.

## Latest runner reports

- /data/wellbeing/obs/consultant/outbox/log16-kernel/runner-reports/runner__20260617-152335__agent_syndicate/runner-summary.md
- /data/wellbeing/obs/consultant/outbox/log16-kernel/runner-reports/runner__20260617-143216__participant_communication/runner-summary.md
- /data/wellbeing/obs/consultant/outbox/log16-kernel/runner-reports/runner__20260617-142951__topic_to_task_system/runner-summary.md
- /data/wellbeing/obs/consultant/outbox/log16-kernel/runner-reports/runner__20260616-174323__participant_pathway/runner-summary.md

