# log16 migration dry-run v01

legacy_runtime: /data/wellbeing/obs/consultant/outbox/log16-kernel
target_runtime: /data/wellbeing/obs/log16

## Existence
legacy_exists: YES
target_exists: YES

## File counts
legacy_files: 245
legacy_dirs: 96
target_files: 0
target_dirs: 31

## Size
legacy_size: 1,8M
target_size: 124K

## Critical legacy files
OK: /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-pult
OK: /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-pult.py
OK: /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-dashboard.py
OK: /data/wellbeing/obs/consultant/outbox/log16-kernel/bin/log16-agent-runner.py

## Top-level legacy layout
/data/wellbeing/obs/consultant/outbox/log16-kernel
/data/wellbeing/obs/consultant/outbox/log16-kernel/answers
/data/wellbeing/obs/consultant/outbox/log16-kernel/answers/approved
/data/wellbeing/obs/consultant/outbox/log16-kernel/answers/deprecated
/data/wellbeing/obs/consultant/outbox/log16-kernel/answers/draft
/data/wellbeing/obs/consultant/outbox/log16-kernel/answers/needs_review
/data/wellbeing/obs/consultant/outbox/log16-kernel/bin
/data/wellbeing/obs/consultant/outbox/log16-kernel/bin/__pycache__
/data/wellbeing/obs/consultant/outbox/log16-kernel/dashboard-runs
/data/wellbeing/obs/consultant/outbox/log16-kernel/dashboard-runs/action-cleanup-20260617-152003
/data/wellbeing/obs/consultant/outbox/log16-kernel/dashboard-runs/action-cleanup-20260617-152816
/data/wellbeing/obs/consultant/outbox/log16-kernel/dashboard-runs/action-cleanup-20260617-152904
/data/wellbeing/obs/consultant/outbox/log16-kernel/dashboard-runs/action-run-pending-20260617-152007
/data/wellbeing/obs/consultant/outbox/log16-kernel/dashboard-runs/action-run-pending-20260617-152812
/data/wellbeing/obs/consultant/outbox/log16-kernel/dashboard-runs/action-run-pending-20260617-152847
/data/wellbeing/obs/consultant/outbox/log16-kernel/dashboard-runs/ask-20260617-152231
/data/wellbeing/obs/consultant/outbox/log16-kernel/dashboard-runs/tasks-20260617-152335
/data/wellbeing/obs/consultant/outbox/log16-kernel/derived-tasks
/data/wellbeing/obs/consultant/outbox/log16-kernel/derived-tasks/archived
/data/wellbeing/obs/consultant/outbox/log16-kernel/derived-tasks/dispatched
/data/wellbeing/obs/consultant/outbox/log16-kernel/derived-tasks/done
/data/wellbeing/obs/consultant/outbox/log16-kernel/derived-tasks/needs_review
/data/wellbeing/obs/consultant/outbox/log16-kernel/derived-tasks/proposed
/data/wellbeing/obs/consultant/outbox/log16-kernel/derived-tasks/rejected
/data/wellbeing/obs/consultant/outbox/log16-kernel/derived-tasks/routed
/data/wellbeing/obs/consultant/outbox/log16-kernel/derived-tasks/running
/data/wellbeing/obs/consultant/outbox/log16-kernel/entity-registry
/data/wellbeing/obs/consultant/outbox/log16-kernel/entity-requests
/data/wellbeing/obs/consultant/outbox/log16-kernel/entity-requests/done
/data/wellbeing/obs/consultant/outbox/log16-kernel/entity-requests/failed
/data/wellbeing/obs/consultant/outbox/log16-kernel/entity-requests/pending
/data/wellbeing/obs/consultant/outbox/log16-kernel/entity-requests/running
/data/wellbeing/obs/consultant/outbox/log16-kernel/entity-responses
/data/wellbeing/obs/consultant/outbox/log16-kernel/entity-responses/approved
/data/wellbeing/obs/consultant/outbox/log16-kernel/entity-responses/failed
/data/wellbeing/obs/consultant/outbox/log16-kernel/entity-responses/needs_review
/data/wellbeing/obs/consultant/outbox/log16-kernel/entity-responses/rejected
/data/wellbeing/obs/consultant/outbox/log16-kernel/entity-responses/revision_requested
/data/wellbeing/obs/consultant/outbox/log16-kernel/gaps
/data/wellbeing/obs/consultant/outbox/log16-kernel/gaps/detected
/data/wellbeing/obs/consultant/outbox/log16-kernel/gaps/resolved
/data/wellbeing/obs/consultant/outbox/log16-kernel/gaps/routed
/data/wellbeing/obs/consultant/outbox/log16-kernel/indexes
/data/wellbeing/obs/consultant/outbox/log16-kernel/pult-runs
/data/wellbeing/obs/consultant/outbox/log16-kernel/pult-runs/answer-20260617-145532
/data/wellbeing/obs/consultant/outbox/log16-kernel/pult-runs/answer-20260617-152231
/data/wellbeing/obs/consultant/outbox/log16-kernel/pult-runs/cleanup-20260617-152003
/data/wellbeing/obs/consultant/outbox/log16-kernel/pult-runs/cleanup-20260617-152816
/data/wellbeing/obs/consultant/outbox/log16-kernel/pult-runs/cleanup-20260617-152904
/data/wellbeing/obs/consultant/outbox/log16-kernel/pult-runs/run-pending-20260617-144438
/data/wellbeing/obs/consultant/outbox/log16-kernel/pult-runs/run-pending-20260617-144457
/data/wellbeing/obs/consultant/outbox/log16-kernel/pult-runs/run-pending-20260617-152007
/data/wellbeing/obs/consultant/outbox/log16-kernel/pult-runs/run-pending-20260617-152335
/data/wellbeing/obs/consultant/outbox/log16-kernel/pult-runs/run-pending-20260617-152812
/data/wellbeing/obs/consultant/outbox/log16-kernel/pult-runs/run-pending-20260617-152847
/data/wellbeing/obs/consultant/outbox/log16-kernel/pult-runs/tasks-20260617-152335
/data/wellbeing/obs/consultant/outbox/log16-kernel/reports
/data/wellbeing/obs/consultant/outbox/log16-kernel/reviewed-docs
/data/wellbeing/obs/consultant/outbox/log16-kernel/reviews
/data/wellbeing/obs/consultant/outbox/log16-kernel/routed-task-dispatch-runs
/data/wellbeing/obs/consultant/outbox/log16-kernel/routed-task-dispatch-runs/routed-dispatch__20260617-141354
/data/wellbeing/obs/consultant/outbox/log16-kernel/routed-task-dispatch-runs/routed-dispatch__20260617-141419
/data/wellbeing/obs/consultant/outbox/log16-kernel/routed-task-dispatch-runs/routed-dispatch__20260617-152335
/data/wellbeing/obs/consultant/outbox/log16-kernel/runner-reports
/data/wellbeing/obs/consultant/outbox/log16-kernel/runner-reports/runner__20260616-174323__participant_pathway
/data/wellbeing/obs/consultant/outbox/log16-kernel/runner-reports/runner__20260617-142951__topic_to_task_system
/data/wellbeing/obs/consultant/outbox/log16-kernel/runner-reports/runner__20260617-143216__participant_communication
/data/wellbeing/obs/consultant/outbox/log16-kernel/runner-reports/runner__20260617-152335__agent_syndicate
/data/wellbeing/obs/consultant/outbox/log16-kernel/schemas
/data/wellbeing/obs/consultant/outbox/log16-kernel/synthesis
/data/wellbeing/obs/consultant/outbox/log16-kernel/synthesis/participant-pathway
/data/wellbeing/obs/consultant/outbox/log16-kernel/task-batches
/data/wellbeing/obs/consultant/outbox/log16-kernel/tasks
/data/wellbeing/obs/consultant/outbox/log16-kernel/tasks/done
/data/wellbeing/obs/consultant/outbox/log16-kernel/tasks/proposed
/data/wellbeing/obs/consultant/outbox/log16-kernel/tasks/routed
/data/wellbeing/obs/consultant/outbox/log16-kernel/themes
/data/wellbeing/obs/consultant/outbox/log16-kernel/themes/captured
/data/wellbeing/obs/consultant/outbox/log16-kernel/themes/in_review
/data/wellbeing/obs/consultant/outbox/log16-kernel/themes/resolved
/data/wellbeing/obs/consultant/outbox/log16-kernel/topic-task-triage-runs
/data/wellbeing/obs/consultant/outbox/log16-kernel/topic-task-triage-runs/triage__20260617-080107
/data/wellbeing/obs/consultant/outbox/log16-kernel/topic-task-triage-runs/triage__20260617-080121
/data/wellbeing/obs/consultant/outbox/log16-kernel/topic-task-triage-runs/triage__20260617-152335
/data/wellbeing/obs/consultant/outbox/log16-kernel/topic-to-task-runs
/data/wellbeing/obs/consultant/outbox/log16-kernel/topic-to-task-runs/topic-to-task-20260616-214608
/data/wellbeing/obs/consultant/outbox/log16-kernel/topic-to-task-runs/topic-to-task-20260617-152335

## Target non-empty warning
WARNING: target runtime is not empty.
Actual migration must use merge/copy policy, not blind overwrite.

## Symlink feasibility
legacy_is_symlink: NO
To create compatibility symlink later, migration must:
1. backup legacy runtime
2. copy legacy -> target
3. rename legacy to backup
4. ln -s target legacy

## Rsync dry-run
.d..t...... ./
>f+++++++++ README.md
cd+++++++++ answers/
cd+++++++++ answers/approved/
cd+++++++++ answers/deprecated/
cd+++++++++ answers/draft/
cd+++++++++ answers/needs_review/
>f+++++++++ answers/needs_review/answer__20260616-151123__participant-pathway.json
>f+++++++++ answers/needs_review/answer__20260616-152426__research_digest.json
>f+++++++++ answers/needs_review/answer__20260616-152835__research_digest.json
>f+++++++++ answers/needs_review/answer__20260616-153802__participant_pathway.json
>f+++++++++ answers/needs_review/answer__20260616-154805__participant_pathway.json
>f+++++++++ answers/needs_review/answer__20260616-161618__participant_pathway.json
>f+++++++++ answers/needs_review/answer__20260616-161717__participant_pathway.json
>f+++++++++ answers/needs_review/answer__20260616-161809__participant_pathway.json
>f+++++++++ answers/needs_review/answer__20260616-163524__participant_pathway.json
>f+++++++++ answers/needs_review/answer__20260616-163526__participant_pathway.json
.d..t...... bin/
>f+++++++++ bin/log16-agent-runner-check.sh
>f+++++++++ bin/log16-agent-runner-generic-check.sh
>f+++++++++ bin/log16-agent-runner.py
>f+++++++++ bin/log16-ask-import-v05-2.sh
>f+++++++++ bin/log16-case-summary.py
>f+++++++++ bin/log16-case-summary.sh
>f+++++++++ bin/log16-create-participant-pathway-requests.py
>f+++++++++ bin/log16-dashboard-check.sh
>f+++++++++ bin/log16-dashboard-open.sh
>f+++++++++ bin/log16-dashboard.py
>f+++++++++ bin/log16-dashboard.sh
>f+++++++++ bin/log16-dispatch-participant-pathway.sh
>f+++++++++ bin/log16-dispatch-questions.py
>f+++++++++ bin/log16-dispatch-questions.sh
>f+++++++++ bin/log16-dispatch-routed-tasks.py
>f+++++++++ bin/log16-dispatch-routed-tasks.sh
>f+++++++++ bin/log16-extend-entity-registry-v01.py
>f+++++++++ bin/log16-gui-check.sh
>f+++++++++ bin/log16-gui.py
>f+++++++++ bin/log16-gui.sh
>f+++++++++ bin/log16-import-latest-v05-2.sh
>f+++++++++ bin/log16-import-v05-run.py
>f+++++++++ bin/log16-import-v05-run.sh
>f+++++++++ bin/log16-last-report.sh
>f+++++++++ bin/log16-new-id.sh
>f+++++++++ bin/log16-participant-pathway-case.sh
>f+++++++++ bin/log16-pult
>f+++++++++ bin/log16-pult-check.sh
>f+++++++++ bin/log16-pult.py
>f+++++++++ bin/log16-routed-task-dispatch-check.sh
>f+++++++++ bin/log16-runner-participant-communication.sh
>f+++++++++ bin/log16-runner-participant-pathway.sh
>f+++++++++ bin/log16-runner-topic-to-task-system.sh
>f+++++++++ bin/log16-smoke-test.sh
>f+++++++++ bin/log16-status.sh
>f+++++++++ bin/log16-synthesize-participant-pathway.py
>f+++++++++ bin/log16-synthesize-participant-pathway.sh
>f+++++++++ bin/log16-topic-task-triage-check.sh
>f+++++++++ bin/log16-topic-task-triage.py
>f+++++++++ bin/log16-topic-task-triage.sh
>f+++++++++ bin/log16-topic-to-task-check.sh
>f+++++++++ bin/log16-topic-to-task-core.py
>f+++++++++ bin/log16-topic-to-task-demo.sh
>f+++++++++ bin/log16-topic-to-task.sh
>f+++++++++ bin/log16-webui-check.sh
>f+++++++++ bin/log16-webui-open.sh
>f+++++++++ bin/log16-webui.py
>f+++++++++ bin/log16-webui.sh
cd+++++++++ bin/__pycache__/
>f+++++++++ bin/__pycache__/log16-agent-runner.cpython-312.pyc
>f+++++++++ bin/__pycache__/log16-case-summary.cpython-312.pyc
>f+++++++++ bin/__pycache__/log16-create-participant-pathway-requests.cpython-312.pyc
>f+++++++++ bin/__pycache__/log16-dashboard.cpython-312.pyc
>f+++++++++ bin/__pycache__/log16-dispatch-questions.cpython-312.pyc
>f+++++++++ bin/__pycache__/log16-dispatch-routed-tasks.cpython-312.pyc
>f+++++++++ bin/__pycache__/log16-extend-entity-registry-v01.cpython-312.pyc
>f+++++++++ bin/__pycache__/log16-gui.cpython-312.pyc
>f+++++++++ bin/__pycache__/log16-import-v05-run.cpython-312.pyc
>f+++++++++ bin/__pycache__/log16-pult.cpython-312.pyc
>f+++++++++ bin/__pycache__/log16-synthesize-participant-pathway.cpython-312.pyc
>f+++++++++ bin/__pycache__/log16-topic-task-triage.cpython-312.pyc
>f+++++++++ bin/__pycache__/log16-topic-to-task-core.cpython-312.pyc
>f+++++++++ bin/__pycache__/log16-webui.cpython-312.pyc
.d..t...... dashboard-runs/
cd+++++++++ dashboard-runs/action-cleanup-20260617-152003/
>f+++++++++ dashboard-runs/action-cleanup-20260617-152003/cleanup.log
cd+++++++++ dashboard-runs/action-cleanup-20260617-152816/
>f+++++++++ dashboard-runs/action-cleanup-20260617-152816/cleanup.log
cd+++++++++ dashboard-runs/action-cleanup-20260617-152904/
>f+++++++++ dashboard-runs/action-cleanup-20260617-152904/cleanup.log
cd+++++++++ dashboard-runs/action-run-pending-20260617-152007/
>f+++++++++ dashboard-runs/action-run-pending-20260617-152007/run-pending.log
cd+++++++++ dashboard-runs/action-run-pending-20260617-152812/
>f+++++++++ dashboard-runs/action-run-pending-20260617-152812/run-pending.log
cd+++++++++ dashboard-runs/action-run-pending-20260617-152847/
>f+++++++++ dashboard-runs/action-run-pending-20260617-152847/run-pending.log
cd+++++++++ dashboard-runs/ask-20260617-152231/
>f+++++++++ dashboard-runs/ask-20260617-152231/ask.log
>f+++++++++ dashboard-runs/ask-20260617-152231/dashboard-ask-result.md
>f+++++++++ dashboard-runs/ask-20260617-152231/input.txt
cd+++++++++ dashboard-runs/tasks-20260617-152335/
>f+++++++++ dashboard-runs/tasks-20260617-152335/dashboard-tasks-result.md
>f+++++++++ dashboard-runs/tasks-20260617-152335/input.txt
>f+++++++++ dashboard-runs/tasks-20260617-152335/tasks.log
cd+++++++++ derived-tasks/
cd+++++++++ derived-tasks/archived/
cd+++++++++ derived-tasks/dispatched/
>f+++++++++ derived-tasks/dispatched/task__20260616-214608__participant_communication__подготовить-starter-tasks-catalog.json
>f+++++++++ derived-tasks/dispatched/task__20260616-214608__participant_communication__проверить-participant-pathway-canon-working-v01.json
>f+++++++++ derived-tasks/dispatched/task__20260616-214608__topic_to_task_system__описать-evidence-lookup-для-theme_case.json
>f+++++++++ derived-tasks/dispatched/task__20260616-214608__topic_to_task_system__проверить-качество-создаваемых-задач.json
>f+++++++++ derived-tasks/dispatched/task__20260616-214608__topic_to_task_system__согласовать-routing-policy-для-новых-задач.json
>f+++++++++ derived-tasks/dispatched/task__20260617-152335__agent_syndicate__описать-adapter-roadmap-для-разных-ии.json
cd+++++++++ derived-tasks/done/
>f+++++++++ derived-tasks/done/task__20260616-214608__topic_to_task_system__установить-минимальный-topic-to-task-core.json
cd+++++++++ derived-tasks/needs_review/
cd+++++++++ derived-tasks/proposed/
cd+++++++++ derived-tasks/rejected/
cd+++++++++ derived-tasks/routed/
cd+++++++++ derived-tasks/running/
cd+++++++++ entity-registry/
>f+++++++++ entity-registry/entity-registry.json
cd+++++++++ entity-requests/
cd+++++++++ entity-requests/done/
>f+++++++++ entity-requests/done/request__20260616-174322__consultant__participant_pathway.json
>f+++++++++ entity-requests/done/request__20260616-174322__koordinator__participant_pathway.json
>f+++++++++ entity-requests/done/request__20260616-174322__shkola__participant_pathway.json
>f+++++++++ entity-requests/done/request__20260616-174322__vhodnoy-nastavnik__participant_pathway.json
>f+++++++++ entity-requests/done/request__20260617-141419__archivarius__описать-evidence-lookup-для-theme_case.json
>f+++++++++ entity-requests/done/request__20260617-141419__consultant__проверить-качество-создаваемых-задач.json
>f+++++++++ entity-requests/done/request__20260617-141419__koordinator__согласовать-routing-policy-для-новых-задач.json
>f+++++++++ entity-requests/done/request__20260617-141419__shkola__проверить-participant-pathway-canon-working-v01.json
>f+++++++++ entity-requests/done/request__20260617-141419__vhodnoy-nastavnik__подготовить-starter-tasks-catalog.json
>f+++++++++ entity-requests/done/request__20260617-152335__koder__описать-adapter-roadmap-для-разных-ии.json
cd+++++++++ entity-requests/failed/
cd+++++++++ entity-requests/pending/
cd+++++++++ entity-requests/running/
cd+++++++++ entity-responses/
cd+++++++++ entity-responses/approved/
cd+++++++++ entity-responses/failed/
cd+++++++++ entity-responses/needs_review/
>f+++++++++ entity-responses/needs_review/response__20260616-174400__consultant__participant_pathway.json
>f+++++++++ entity-responses/needs_review/response__20260616-174428__koordinator__participant_pathway.json
>f+++++++++ entity-responses/needs_review/response__20260616-174458__shkola__participant_pathway.json
>f+++++++++ entity-responses/needs_review/response__20260616-174524__vhodnoy-nastavnik__participant_pathway.json
>f+++++++++ entity-responses/needs_review/response__20260617-143036__archivarius__topic_to_task_system.json
>f+++++++++ entity-responses/needs_review/response__20260617-143110__consultant__topic_to_task_system.json
>f+++++++++ entity-responses/needs_review/response__20260617-143141__koordinator__topic_to_task_system.json
>f+++++++++ entity-responses/needs_review/response__20260617-143250__shkola__participant_communication.json
>f+++++++++ entity-responses/needs_review/response__20260617-143321__vhodnoy-nastavnik__participant_communication.json
>f+++++++++ entity-responses/needs_review/response__20260617-152416__koder__agent_syndicate.json
cd+++++++++ entity-responses/rejected/
cd+++++++++ entity-responses/revision_requested/
cd+++++++++ gaps/
cd+++++++++ gaps/detected/
>f+++++++++ gaps/detected/gap__20260616-151123__participant-pathway-canon-missing.json
>f+++++++++ gaps/detected/gap__20260616-152426__research_digest.json
>f+++++++++ gaps/detected/gap__20260616-152835__research_digest.json
>f+++++++++ gaps/detected/gap__20260616-153802__participant_pathway.json
>f+++++++++ gaps/detected/gap__20260616-161618__participant_pathway.json
>f+++++++++ gaps/detected/gap__20260616-161717__participant_pathway.json
>f+++++++++ gaps/detected/gap__20260616-161809__participant_pathway.json
>f+++++++++ gaps/detected/gap__20260616-163524__participant_pathway.json
>f+++++++++ gaps/detected/gap__20260616-163526__participant_pathway.json
cd+++++++++ gaps/resolved/
cd+++++++++ gaps/routed/
cd+++++++++ indexes/
>f+++++++++ indexes/approved-answers-index.jsonl
>f+++++++++ indexes/gaps-index.jsonl
>f+++++++++ indexes/questions-index.jsonl
>f+++++++++ indexes/reviews-index.jsonl
>f+++++++++ indexes/tasks-index.jsonl
cd+++++++++ pult-runs/
cd+++++++++ pult-runs/answer-20260617-145532/
>f+++++++++ pult-runs/answer-20260617-145532/direct-answer.md
cd+++++++++ pult-runs/answer-20260617-152231/
>f+++++++++ pult-runs/answer-20260617-152231/direct-answer.md
cd+++++++++ pult-runs/cleanup-20260617-152003/
>f+++++++++ pult-runs/cleanup-20260617-152003/cleanup-summary.md
cd+++++++++ pult-runs/cleanup-20260617-152816/
>f+++++++++ pult-runs/cleanup-20260617-152816/cleanup-summary.md
cd+++++++++ pult-runs/cleanup-20260617-152904/
>f+++++++++ pult-runs/cleanup-20260617-152904/cleanup-summary.md
cd+++++++++ pult-runs/run-pending-20260617-144438/
>f+++++++++ pult-runs/run-pending-20260617-144438/pult-run-pending-summary.md
cd+++++++++ pult-runs/run-pending-20260617-144457/
>f+++++++++ pult-runs/run-pending-20260617-144457/pult-run-pending-summary.md
cd+++++++++ pult-runs/run-pending-20260617-152007/
>f+++++++++ pult-runs/run-pending-20260617-152007/pult-run-pending-summary.md
cd+++++++++ pult-runs/run-pending-20260617-152335/
>f+++++++++ pult-runs/run-pending-20260617-152335/pult-run-pending-summary.md
>f+++++++++ pult-runs/run-pending-20260617-152335/runner-agent_syndicate.log
cd+++++++++ pult-runs/run-pending-20260617-152812/
>f+++++++++ pult-runs/run-pending-20260617-152812/pult-run-pending-summary.md
cd+++++++++ pult-runs/run-pending-20260617-152847/
>f+++++++++ pult-runs/run-pending-20260617-152847/pult-run-pending-summary.md
cd+++++++++ pult-runs/tasks-20260617-152335/
>f+++++++++ pult-runs/tasks-20260617-152335/01-topic-to-task.log
>f+++++++++ pult-runs/tasks-20260617-152335/02-triage-apply.log
>f+++++++++ pult-runs/tasks-20260617-152335/03-dispatch-create.log
>f+++++++++ pult-runs/tasks-20260617-152335/04-cleanup-after-dispatch.txt
>f+++++++++ pult-runs/tasks-20260617-152335/05-run-pending.log
>f+++++++++ pult-runs/tasks-20260617-152335/input-event.txt
>f+++++++++ pult-runs/tasks-20260617-152335/pult-tasks-summary.md
.d..t...... reports/
>f+++++++++ reports/import__20260616-152426__research_digest.md
>f+++++++++ reports/import__20260616-152835__research_digest.md
>f+++++++++ reports/import__20260616-153802__participant_pathway.md
>f+++++++++ reports/import__20260616-154805__participant_pathway.md
>f+++++++++ reports/import__20260616-161618__participant_pathway.md
>f+++++++++ reports/import__20260616-161717__participant_pathway.md
>f+++++++++ reports/import__20260616-161809__participant_pathway.md
>f+++++++++ reports/import__20260616-163524__participant_pathway.md
>f+++++++++ reports/import__20260616-163526__participant_pathway.md
>f+++++++++ reports/seed__20260616-151123__participant-pathway.md
.d..t...... reviewed-docs/
.d..t...... reviews/
>f+++++++++ reviews/review__20260616-151123__participant-pathway.json
>f+++++++++ reviews/review__20260616-152426__research_digest.json
>f+++++++++ reviews/review__20260616-152835__research_digest.json
>f+++++++++ reviews/review__20260616-153802__participant_pathway.json
>f+++++++++ reviews/review__20260616-154805__participant_pathway.json
>f+++++++++ reviews/review__20260616-161618__participant_pathway.json
>f+++++++++ reviews/review__20260616-161717__participant_pathway.json
>f+++++++++ reviews/review__20260616-161809__participant_pathway.json
>f+++++++++ reviews/review__20260616-163524__participant_pathway.json
>f+++++++++ reviews/review__20260616-163526__participant_pathway.json
cd+++++++++ routed-task-dispatch-runs/
cd+++++++++ routed-task-dispatch-runs/routed-dispatch__20260617-141354/
>f+++++++++ routed-task-dispatch-runs/routed-dispatch__20260617-141354/manifest.json
>f+++++++++ routed-task-dispatch-runs/routed-dispatch__20260617-141354/routed-dispatch-summary.md
cd+++++++++ routed-task-dispatch-runs/routed-dispatch__20260617-141419/
>f+++++++++ routed-task-dispatch-runs/routed-dispatch__20260617-141419/manifest.json
>f+++++++++ routed-task-dispatch-runs/routed-dispatch__20260617-141419/routed-dispatch-summary.md
cd+++++++++ routed-task-dispatch-runs/routed-dispatch__20260617-152335/
>f+++++++++ routed-task-dispatch-runs/routed-dispatch__20260617-152335/manifest.json
>f+++++++++ routed-task-dispatch-runs/routed-dispatch__20260617-152335/routed-dispatch-summary.md
.d..t...... runner-reports/
cd+++++++++ runner-reports/runner__20260616-174323__participant_pathway/
>f+++++++++ runner-reports/runner__20260616-174323__participant_pathway/manifest.json
>f+++++++++ runner-reports/runner__20260616-174323__participant_pathway/runner-summary.md
cd+++++++++ runner-reports/runner__20260616-174323__participant_pathway/prompts/
>f+++++++++ runner-reports/runner__20260616-174323__participant_pathway/prompts/request__20260616-174322__consultant__participant_pathway.prompt.md
>f+++++++++ runner-reports/runner__20260616-174323__participant_pathway/prompts/request__20260616-174322__koordinator__participant_pathway.prompt.md
>f+++++++++ runner-reports/runner__20260616-174323__participant_pathway/prompts/request__20260616-174322__shkola__participant_pathway.prompt.md
>f+++++++++ runner-reports/runner__20260616-174323__participant_pathway/prompts/request__20260616-174322__vhodnoy-nastavnik__participant_pathway.prompt.md
cd+++++++++ runner-reports/runner__20260616-174323__participant_pathway/raw/
>f+++++++++ runner-reports/runner__20260616-174323__participant_pathway/raw/response__20260616-174400__consultant__participant_pathway.txt
>f+++++++++ runner-reports/runner__20260616-174323__participant_pathway/raw/response__20260616-174428__koordinator__participant_pathway.txt
>f+++++++++ runner-reports/runner__20260616-174323__participant_pathway/raw/response__20260616-174458__shkola__participant_pathway.txt
>f+++++++++ runner-reports/runner__20260616-174323__participant_pathway/raw/response__20260616-174524__vhodnoy-nastavnik__participant_pathway.txt
cd+++++++++ runner-reports/runner__20260617-142951__topic_to_task_system/
>f+++++++++ runner-reports/runner__20260617-142951__topic_to_task_system/manifest.json
>f+++++++++ runner-reports/runner__20260617-142951__topic_to_task_system/runner-summary.md
cd+++++++++ runner-reports/runner__20260617-142951__topic_to_task_system/prompts/
>f+++++++++ runner-reports/runner__20260617-142951__topic_to_task_system/prompts/request__20260617-141419__archivarius__описать-evidence-lookup-для-theme_case.prompt.md
>f+++++++++ runner-reports/runner__20260617-142951__topic_to_task_system/prompts/request__20260617-141419__consultant__проверить-качество-создаваемых-задач.prompt.md
>f+++++++++ runner-reports/runner__20260617-142951__topic_to_task_system/prompts/request__20260617-141419__koordinator__согласовать-routing-policy-для-новых-задач.prompt.md
cd+++++++++ runner-reports/runner__20260617-142951__topic_to_task_system/raw/
>f+++++++++ runner-reports/runner__20260617-142951__topic_to_task_system/raw/response__20260617-143036__archivarius__topic_to_task_system.txt
>f+++++++++ runner-reports/runner__20260617-142951__topic_to_task_system/raw/response__20260617-143110__consultant__topic_to_task_system.txt
>f+++++++++ runner-reports/runner__20260617-142951__topic_to_task_system/raw/response__20260617-143141__koordinator__topic_to_task_system.txt
cd+++++++++ runner-reports/runner__20260617-143216__participant_communication/
>f+++++++++ runner-reports/runner__20260617-143216__participant_communication/manifest.json
>f+++++++++ runner-reports/runner__20260617-143216__participant_communication/runner-summary.md
cd+++++++++ runner-reports/runner__20260617-143216__participant_communication/prompts/
>f+++++++++ runner-reports/runner__20260617-143216__participant_communication/prompts/request__20260617-141419__shkola__проверить-participant-pathway-canon-working-v01.prompt.md
>f+++++++++ runner-reports/runner__20260617-143216__participant_communication/prompts/request__20260617-141419__vhodnoy-nastavnik__подготовить-starter-tasks-catalog.prompt.md
cd+++++++++ runner-reports/runner__20260617-143216__participant_communication/raw/
>f+++++++++ runner-reports/runner__20260617-143216__participant_communication/raw/response__20260617-143250__shkola__participant_communication.txt
>f+++++++++ runner-reports/runner__20260617-143216__participant_communication/raw/response__20260617-143321__vhodnoy-nastavnik__participant_communication.txt
cd+++++++++ runner-reports/runner__20260617-152335__agent_syndicate/
>f+++++++++ runner-reports/runner__20260617-152335__agent_syndicate/manifest.json
>f+++++++++ runner-reports/runner__20260617-152335__agent_syndicate/runner-summary.md
cd+++++++++ runner-reports/runner__20260617-152335__agent_syndicate/prompts/
>f+++++++++ runner-reports/runner__20260617-152335__agent_syndicate/prompts/request__20260617-152335__koder__описать-adapter-roadmap-для-разных-ии.prompt.md
cd+++++++++ runner-reports/runner__20260617-152335__agent_syndicate/raw/
>f+++++++++ runner-reports/runner__20260617-152335__agent_syndicate/raw/response__20260617-152416__koder__agent_syndicate.txt
cd+++++++++ schemas/
>f+++++++++ schemas/answer-card.schema.json
>f+++++++++ schemas/approved-answer-card.schema.json
>f+++++++++ schemas/derived-task-card.schema.json
>f+++++++++ schemas/entity-request-card.schema.json
>f+++++++++ schemas/entity-response-card.schema.json
>f+++++++++ schemas/gap-card.schema.json
>f+++++++++ schemas/review-card.schema.json
>f+++++++++ schemas/task-batch.schema.json
>f+++++++++ schemas/task-card.schema.json
>f+++++++++ schemas/theme-card.schema.json
cd+++++++++ synthesis/
cd+++++++++ synthesis/participant-pathway/
cd+++++++++ synthesis/participant-pathway/synthesis-20260616-183246/
>f+++++++++ synthesis/participant-pathway/synthesis-20260616-183246/manifest.json
>f+++++++++ synthesis/participant-pathway/synthesis-20260616-183246/operator-decision-questions.md
>f+++++++++ synthesis/participant-pathway/synthesis-20260616-183246/participant-pathway-canon-draft.md
>f+++++++++ synthesis/participant-pathway/synthesis-20260616-183246/synthesis-report.md
cd+++++++++ task-batches/
>f+++++++++ task-batches/batch__20260616-214608__participant_communication.json
>f+++++++++ task-batches/batch__20260616-214608__topic_to_task_system.json
>f+++++++++ task-batches/batch__20260617-152335__agent_syndicate.json
.d..t...... tasks/
.d..t...... tasks/done/
