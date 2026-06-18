# log16 root native patch post-check

target_runtime: /data/wellbeing/obs/log16
legacy_runtime: /data/wellbeing/obs/consultant/outbox/log16-kernel
backup_bin: /data/wellbeing/obs/log16/backups/bin-before-root-native-patch-0618-1929
rollback: /data/wellbeing/repos/wellbeing-log16/scripts/log16-root-native-patch-rollback-0618-1929.sh

legacy_is_symlink: YES
legacy_points_to: /data/wellbeing/obs/log16

hardcoded old path in live bin:

python compile:
OK: /data/wellbeing/obs/log16/bin/log16-webui.py
OK: /data/wellbeing/obs/log16/bin/log16-dashboard.py
OK: /data/wellbeing/obs/log16/bin/log16-extend-entity-registry-v01.py
OK: /data/wellbeing/obs/log16/bin/log16-create-participant-pathway-requests.py
OK: /data/wellbeing/obs/log16/bin/log16-topic-task-triage.py
OK: /data/wellbeing/obs/log16/bin/log16-dispatch-questions.py
OK: /data/wellbeing/obs/log16/bin/log16-case-summary.py
OK: /data/wellbeing/obs/log16/bin/log16-agent-runner.py
OK: /data/wellbeing/obs/log16/bin/log16-topic-to-task-core.py
OK: /data/wellbeing/obs/log16/bin/log16-pult.py
OK: /data/wellbeing/obs/log16/bin/log16-dispatch-routed-tasks.py
OK: /data/wellbeing/obs/log16/bin/log16-synthesize-participant-pathway.py
OK: /data/wellbeing/obs/log16/bin/log16-gui.py
OK: /data/wellbeing/obs/log16/bin/log16-import-v05-run.py

pult status via native path:
# log16 pult status

Created: 2026-06-18T19:29:36

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

- /data/wellbeing/obs/log16/runner-reports/runner__20260617-152335__agent_syndicate/runner-summary.md
- /data/wellbeing/obs/log16/runner-reports/runner__20260617-143216__participant_communication/runner-summary.md
- /data/wellbeing/obs/log16/runner-reports/runner__20260617-142951__topic_to_task_system/runner-summary.md
- /data/wellbeing/obs/log16/runner-reports/runner__20260616-174323__participant_pathway/runner-summary.md

