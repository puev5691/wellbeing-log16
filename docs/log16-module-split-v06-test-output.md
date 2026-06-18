test_apply_review_decision (test_log16_cards.TestCards.test_apply_review_decision) ... ok
test_read_write_move_card (test_log16_cards.TestCards.test_read_write_move_card) ... ok
test_safe_read_json_invalid (test_log16_cards_safe.TestSafeReadJson.test_safe_read_json_invalid) ... ok
test_safe_read_json_missing (test_log16_cards_safe.TestSafeReadJson.test_safe_read_json_missing) ... ok
test_safe_read_json_valid (test_log16_cards_safe.TestSafeReadJson.test_safe_read_json_valid) ... ok
test_paths (test_log16_cli.TestLog16Cli.test_paths) ... ok
test_status_json (test_log16_cli.TestLog16Cli.test_status_json) ... ok
test_parse_answer_bridge (test_log16_cli_bridge.TestLog16CliBridge.test_parse_answer_bridge) ... ok
test_parse_dashboard_bridge (test_log16_cli_bridge.TestLog16CliBridge.test_parse_dashboard_bridge) ... ok
test_parse_pult_bridge (test_log16_cli_bridge.TestLog16CliBridge.test_parse_pult_bridge) ... ok
test_import_modules (test_log16_imports.TestImports.test_import_modules) ... ok
test_status_counts_live_layout_names (test_log16_status.TestStatusCounts.test_status_counts_live_layout_names) ... ok

----------------------------------------------------------------------
Ran 12 tests in 0.027s

OK
{
  "repo_root": "/data/wellbeing/repos/wellbeing-log16",
  "runtime_root": "/data/wellbeing/obs/log16",
  "legacy_runtime_root": "/data/wellbeing/obs/consultant/outbox/log16-kernel",
  "outbox_root": "/data/wellbeing/obs/consultant/outbox",
  "mode": "lab"
}
{
  "themes": 3,
  "tasks_proposed": 0,
  "tasks_routed": 0,
  "tasks_dispatched": 6,
  "tasks_done": 1,
  "requests_pending": 0,
  "requests_done": 10,
  "responses_review": 9,
  "responses_approved": 0,
  "responses_revision": 1,
  "responses_rejected": 0,
  "responses_failed": 0,
  "runner_reports": 4,
  "pult_runs": 12
}
# log16 pult status

Created: 2026-06-18T20:19:28

## Counts

- themes_captured: 3
- tasks_proposed: 0
- tasks_routed: 0
- tasks_dispatched: 6
- tasks_done: 1
- requests_pending: 0
- requests_done: 10
- requests_failed: 0
- responses_needs_review: 9
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

