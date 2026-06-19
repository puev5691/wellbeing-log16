# wellbeing-log16

## What this is

`wellbeing-log16` is a local lab system for the БЛАГОПОЛУЧИЕ project.

It helps organize a workflow:

    question
    answer
    source/gap
    task
    routing
    review
    reusable answer
    next action

This repository is not a finished public product yet.

It is a local lab and documentation base preparing for a future public entry point.

## Current status

Current confirmed lab milestone:

    v0.3.0-lab

Confirmed locally:

    tests pass
    log16 doctor works
    log16 doctor --json works
    runtime health OK
    qwen3:8b detected through Ollama
    GitHub prepublish checks pass
    public knowledge base skeleton exists
    public FAQ answer cards exist
    answer cards are linked to public docs

## What is ready

    CLI basics
    runtime health checks
    doctor diagnostics
    JSON doctor report
    public knowledge base skeleton
    public FAQ draft layer
    public answer cards
    Windows/WSL onboarding draft

## What is not ready yet

    hosted demo
    public production release
    complete install guide
    verified Windows/WSL test bench
    stable contribution process
    public GitHub publication

## Start reading

Recommended public docs:

    docs/public/README.md
    docs/public/navigation.md
    docs/public/project/what-is-wellbeing.md
    docs/public/project/what-is-log16.md
    docs/public/status/current-stage.md
    docs/public/faq/index.md
    docs/public/participation/how-to-start.md
    docs/public/tasks/open-task-classes.md
    docs/public/knowledge-base/answers/index.md

## Local diagnostics

If the local runtime is installed:

    /data/wellbeing/obs/log16/bin/log16 doctor
    /data/wellbeing/obs/log16/bin/log16 doctor --json

## Public answer cards

Reusable public answer cards are stored in:

    docs/public/knowledge-base/answers/

Check them with:

    scripts/check-public-answer-cards.sh
    scripts/check-public-answer-links.sh

## Publication boundary

Do not publish internal runtime state, private queues, logs, secrets, raw entity outputs or unreviewed internal materials.

See:

    docs/public/publication-boundary.md

## For contributors

Start with:

    docs/public/participation/how-to-start.md
    docs/public/tasks/open-task-classes.md
    docs/public/faq/how-to-help.md

## Notes

This root README is a draft for future GitHub publication.

It should be activated only after operator review.

КТО: КОНСУЛЬТАНТ
ДЛЯ ЧЕГО: public root README draft for wellbeing-log16
СТАТУС: draft
