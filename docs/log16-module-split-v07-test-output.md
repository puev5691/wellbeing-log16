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
test_check_json_skip_bins (test_log16_cli_check.TestLog16CliCheck.test_check_json_skip_bins) ... ok
test_health_check_temp_layout_without_bins (test_log16_health.TestLog16Health.test_health_check_temp_layout_without_bins) ... ok
test_import_modules (test_log16_imports.TestImports.test_import_modules) ... ok
test_status_counts_live_layout_names (test_log16_status.TestStatusCounts.test_status_counts_live_layout_names) ... ok

----------------------------------------------------------------------
Ran 14 tests in 0.036s

OK
{
  "ok": true,
  "checks": [
    {
      "name": "runtime_root",
      "ok": true,
      "detail": "/data/wellbeing/obs/log16"
    },
    {
      "name": "themes_captured",
      "ok": true,
      "detail": "/data/wellbeing/obs/log16/themes/captured"
    },
    {
      "name": "tasks_dispatched",
      "ok": true,
      "detail": "/data/wellbeing/obs/log16/derived-tasks/dispatched"
    },
    {
      "name": "requests_pending",
      "ok": true,
      "detail": "/data/wellbeing/obs/log16/entity-requests/pending"
    },
    {
      "name": "requests_done",
      "ok": true,
      "detail": "/data/wellbeing/obs/log16/entity-requests/done"
    },
    {
      "name": "responses_needs_review",
      "ok": true,
      "detail": "/data/wellbeing/obs/log16/entity-responses/needs_review"
    },
    {
      "name": "responses_approved",
      "ok": true,
      "detail": "/data/wellbeing/obs/log16/entity-responses/approved"
    },
    {
      "name": "responses_revision_requested",
      "ok": true,
      "detail": "/data/wellbeing/obs/log16/entity-responses/revision_requested"
    },
    {
      "name": "reviews",
      "ok": true,
      "detail": "/data/wellbeing/obs/log16/reviews"
    },
    {
      "name": "reviewed_docs",
      "ok": true,
      "detail": "/data/wellbeing/obs/log16/reviewed-docs"
    },
    {
      "name": "runner_reports",
      "ok": true,
      "detail": "/data/wellbeing/obs/log16/runner-reports"
    },
    {
      "name": "bin_log16",
      "ok": true,
      "detail": "/data/wellbeing/obs/log16/bin/log16"
    },
    {
      "name": "bin_log16_pult",
      "ok": true,
      "detail": "/data/wellbeing/obs/log16/bin/log16-pult"
    },
    {
      "name": "bin_log16_dashboard",
      "ok": true,
      "detail": "/data/wellbeing/obs/log16/bin/log16-dashboard.sh"
    },
    {
      "name": "bin_log16_dashboard_py",
      "ok": true,
      "detail": "/data/wellbeing/obs/log16/bin/log16-dashboard.py"
    }
  ]
}
