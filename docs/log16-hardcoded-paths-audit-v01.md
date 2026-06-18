# Hardcoded path audit

Pattern:
/data/wellbeing/obs/consultant/outbox/log16-kernel

Matches:
./scripts/audit-hardcoded-paths.sh:5:PATTERN="/data/wellbeing/obs/consultant/outbox/log16-kernel"
./scripts/report-current-root-usage.sh:5:LEGACY="/data/wellbeing/obs/consultant/outbox/log16-kernel"
./config/paths.json:3:  "legacy_runtime_root": "/data/wellbeing/obs/consultant/outbox/log16-kernel",
./config/paths.example.json:3:  "legacy_runtime_root": "/data/wellbeing/obs/consultant/outbox/log16-kernel",
grep: ./docs/log16-hardcoded-paths-audit-v01.md: файл ввода также используется и для вывода
./docs/log16-code-vs-runtime-split-v01.md:7:    /data/wellbeing/obs/consultant/outbox/log16-kernel
./docs/log16-productization-plan-v01.md:23:- убрать hardcoded `/data/wellbeing/obs/consultant/outbox/log16-kernel`;
./docs/log16-current-program-inventory-v01.md:9:    /data/wellbeing/obs/consultant/outbox/log16-kernel
./src/log16_legacy/bin/log16-webui.py:16:ROOT = Path("/data/wellbeing/obs/consultant/outbox/log16-kernel")
./src/log16_legacy/bin/log16-status.sh:4:ROOT="/data/wellbeing/obs/consultant/outbox/log16-kernel"
./src/log16_legacy/bin/log16-runner-participant-pathway.sh:5:/data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-create-participant-pathway-requests.py
./src/log16_legacy/bin/log16-runner-participant-pathway.sh:9:/data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-agent-runner.py --case participant_pathway
./src/log16_legacy/bin/log16-dashboard.py:18:ROOT = Path("/data/wellbeing/obs/consultant/outbox/log16-kernel")
./src/log16_legacy/bin/log16-import-latest-v05-2.sh:5:IMPORTER="/data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-import-v05-run.sh"
./src/log16_legacy/bin/log16-import-latest-v05-2.sh:22:/data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-status.sh
./src/log16_legacy/bin/log16-extend-entity-registry-v01.py:7:ROOT = Path("/data/wellbeing/obs/consultant/outbox/log16-kernel")
./src/log16_legacy/bin/log16-smoke-test.sh:3:ROOT="/data/wellbeing/obs/consultant/outbox/log16-kernel"
./src/log16_legacy/bin/log16-import-v05-run.sh:7:python3 /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-import-v05-run.py "$1"
./src/log16_legacy/bin/log16-agent-runner-check.sh:4:ROOT="/data/wellbeing/obs/consultant/outbox/log16-kernel"
./src/log16_legacy/bin/log16-dispatch-routed-tasks.sh:3:exec /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-dispatch-routed-tasks.py "$@"
./src/log16_legacy/bin/log16-create-participant-pathway-requests.py:8:ROOT = Path("/data/wellbeing/obs/consultant/outbox/log16-kernel")
./src/log16_legacy/bin/log16-gui.sh:3:exec python3 /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-gui.py
./src/log16_legacy/bin/log16-topic-to-task-demo.sh:3:exec /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-topic-to-task-core.py \
./src/log16_legacy/bin/log16-dashboard-check.sh:4:ROOT="/data/wellbeing/obs/consultant/outbox/log16-kernel"
./src/log16_legacy/bin/log16-last-report.sh:4:ROOT="/data/wellbeing/obs/consultant/outbox/log16-kernel"
./src/log16_legacy/bin/log16-webui-check.sh:14:  /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-webui.py \
./src/log16_legacy/bin/log16-webui-check.sh:15:  /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-webui.sh \
./src/log16_legacy/bin/log16-webui-check.sh:16:  /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-webui-open.sh \
./src/log16_legacy/bin/log16-webui-check.sh:17:  /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-ask-import-v05-2.sh \
./src/log16_legacy/bin/log16-webui-check.sh:18:  /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-case-summary.sh
./src/log16_legacy/bin/log16-webui-check.sh:27:python3 -m py_compile /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-webui.py
./src/log16_legacy/bin/log16-topic-to-task.sh:3:exec /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-topic-to-task-core.py "$@"
./src/log16_legacy/bin/log16-topic-task-triage.py:13:ROOT = Path("/data/wellbeing/obs/consultant/outbox/log16-kernel")
./src/log16_legacy/bin/log16-case-summary.sh:3:exec /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-case-summary.py "$@"
./src/log16_legacy/bin/log16-participant-pathway-case.sh:3:exec /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-case-summary.py --pattern participant_pathway "$@"
./src/log16_legacy/bin/log16-topic-task-triage.sh:3:exec /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-topic-task-triage.py "$@"
./src/log16_legacy/bin/log16-pult:3:exec /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-pult.py "$@"
./src/log16_legacy/bin/log16-dispatch-participant-pathway.sh:3:exec /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-dispatch-questions.py --pattern participant_pathway "$@"
./src/log16_legacy/bin/log16-pult-check.sh:4:ROOT="/data/wellbeing/obs/consultant/outbox/log16-kernel"
./src/log16_legacy/bin/log16-dispatch-questions.py:12:ROOT = Path("/data/wellbeing/obs/consultant/outbox/log16-kernel")
./src/log16_legacy/bin/log16-routed-task-dispatch-check.sh:4:ROOT="/data/wellbeing/obs/consultant/outbox/log16-kernel"
./src/log16_legacy/bin/log16-agent-runner-generic-check.sh:4:ROOT="/data/wellbeing/obs/consultant/outbox/log16-kernel"
./src/log16_legacy/bin/log16-agent-runner-generic-check.sh:18:p=Path("/data/wellbeing/obs/consultant/outbox/log16-kernel/entity-registry/entity-registry.json")
./src/log16_legacy/bin/log16-runner-participant-communication.sh:3:exec /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-agent-runner.py --case participant_communication "$@"
./src/log16_legacy/bin/log16-topic-to-task-check.sh:4:ROOT="/data/wellbeing/obs/consultant/outbox/log16-kernel"
./src/log16_legacy/bin/log16-case-summary.py:8:ROOT = Path("/data/wellbeing/obs/consultant/outbox/log16-kernel")
./src/log16_legacy/bin/log16-agent-runner.py:14:ROOT = Path("/data/wellbeing/obs/consultant/outbox/log16-kernel")
./src/log16_legacy/bin/log16-topic-to-task-core.py:12:ROOT = Path("/data/wellbeing/obs/consultant/outbox/log16-kernel")
./src/log16_legacy/bin/log16-dashboard.sh:3:exec /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-dashboard.py
./src/log16_legacy/bin/log16-synthesize-participant-pathway.sh:3:exec /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-synthesize-participant-pathway.py "$@"
./src/log16_legacy/bin/log16-pult.py:13:ROOT = Path("/data/wellbeing/obs/consultant/outbox/log16-kernel")
./src/log16_legacy/bin/log16-dispatch-routed-tasks.py:12:ROOT = Path("/data/wellbeing/obs/consultant/outbox/log16-kernel")
./src/log16_legacy/bin/log16-webui.sh:4:exec python3 /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-webui.py --host 127.0.0.1 --port "$PORT"
./src/log16_legacy/bin/log16-gui-check.sh:17:  /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-gui.py \
./src/log16_legacy/bin/log16-gui-check.sh:18:  /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-gui.sh \
./src/log16_legacy/bin/log16-gui-check.sh:19:  /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-ask-import-v05-2.sh \
./src/log16_legacy/bin/log16-gui-check.sh:20:  /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-case-summary.sh
./src/log16_legacy/bin/log16-runner-topic-to-task-system.sh:3:exec /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-agent-runner.py --case topic_to_task_system "$@"
./src/log16_legacy/bin/log16-synthesize-participant-pathway.py:11:ROOT = Path("/data/wellbeing/obs/consultant/outbox/log16-kernel")
./src/log16_legacy/bin/log16-gui.py:14:ROOT = Path("/data/wellbeing/obs/consultant/outbox/log16-kernel")
./src/log16_legacy/bin/log16-ask-import-v05-2.sh:5:IMPORTER="/data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-import-v05-run.sh"
./src/log16_legacy/bin/log16-ask-import-v05-2.sh:6:STATUS="/data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-status.sh"
./src/log16_legacy/bin/log16-dispatch-questions.sh:3:exec /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-dispatch-questions.py "$@"
./src/log16_legacy/bin/log16-topic-task-triage-check.sh:4:ROOT="/data/wellbeing/obs/consultant/outbox/log16-kernel"
./src/log16_legacy/bin/log16-import-v05-run.py:5:ROOT = Path('/data/wellbeing/obs/consultant/outbox/log16-kernel')
./src/log16/paths.py:7:LEGACY_RUNTIME_ROOT = Path("/data/wellbeing/obs/consultant/outbox/log16-kernel")
./src/log16/config.py:10:DEFAULT_LEGACY_RUNTIME_ROOT = Path("/data/wellbeing/obs/consultant/outbox/log16-kernel")
./README.md:34:    /data/wellbeing/obs/consultant/outbox/log16-kernel
