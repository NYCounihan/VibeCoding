# Working Style

Instructions for coding agents working with this developer. Reusable across any solo-developer project.

## Core philosophy

One primary user. Fast-moving codebase. Updates over continuity. No production ceremony unless asked.

What this means in practice:

- Renaming, restructuring, and deleting code is encouraged. Nothing here serves users other than the developer.
- No backwards compatibility, no migration shims, no deprecation cycles. If something is replaced, delete the old code.
- No defensive coding for cases that cannot occur. No input validation for impossible states, no try/except added for "robustness."
- No future-proofing or abstraction for hypothetical needs. Build for the next session, not the next year.
- No production-grade hygiene (extensive logging, full test coverage, CI gates, performance budgets) unless explicitly requested.

Effort spent making code easier for future readers to maintain is wasted in this project.

## First-use setup (agent: do this before responding)

This file is a portable template. Any value of the form `<VALUE>` is a placeholder to fill in once per machine.

Before responding to the user's first substantive request in any session, scan this file for remaining `<...>` placeholders. If one is found:

1. Ask the user for the value in one short message. Do not guess.
2. Use the Edit tool to replace every occurrence of that placeholder in this file with the literal answer.
3. Then continue with the user's original request.

Current placeholders:

- `<SCREENSHOTS_FOLDER>` — absolute path to the user's screenshots folder. Common examples by OS: Windows under `Pictures\Screenshots` or `OneDrive\Pictures\Screenshots`; macOS `~/Desktop` or `~/Pictures/Screenshots`; Linux `~/Pictures/Screenshots`. Ask, do not guess.

This section can stay after configuration; it documents what was set.

## Discuss-then-code rule

The user runs coding agents in permissionless mode. The cost of speed is one discipline rule: do not code during discussion.

**Discussion turn** — a question, an open-ended exploration, or a review without a named next change. Investigate read-only (Read, grep, ls). Answer, surface trade-offs, wait. Do not write files. Do not run mutating commands.

**Coding turn** — an imperative ("build", "fix", "change", "add", "implement") or explicit confirmation of a proposal ("yes, go"). Now you may write. Do not re-ask permission for each step inside the agreed scope. If scope appears to be growing beyond what was agreed, stop and surface it — that is a scope check, not a permission ask.

When in doubt about which mode the user is in, ask one short clarifying question before touching files.

## Root-cause debugging (strongest technical rule)

When you find a bug, trace it to the first wrong assumption — the original line that introduced the conflict, even if that line is syntactically correct. Fix at the source.

Forbidden:
- Catching the exception further down and continuing
- Patching a caller to compensate for a callee's wrong behavior
- Adding a special-case branch instead of fixing the general case
- Type-coercing or normalizing inputs that should have been correct upstream
- "Just in case" guards added around a symptom whose cause is unknown

If the root-cause fix is larger than the current task warrants, state that explicitly and ask whether to proceed. Do not split the difference with a band-aid.

## Simplicity rule

Prefer fewer concepts, fewer files, fewer branches, and fewer lines — when clarity and performance are not sacrificed.

Before adding code, look for code to remove. Before adding a file, look for a file to merge into. Before adding a branch, ask whether the case is actually reachable.

Spend reasoning effort up front so the diff is smaller. Three thoughtful lines beat ten reactive ones.

## Drift flagging (suggest, do not execute)

Naming, file boundaries, and structure drift over time. When you notice something worth renaming, restructuring, or consolidating, do not act on it inside the current task.

Instead, append one line to your end-of-turn message: *"Drift noticed: [thing]. Want me to address in a separate turn?"* The user decides.

Refactors outside the current task scope require explicit authorization.

## Reviewing other agents' output

When asked to review a plan, commit, or diff from another coding agent, end your review with concise *questions* directed at that agent — not statements of conclusion.

- Good: *"What does this function return when the input list is empty?"*
- Bad: *"This crashes on empty input — add a check."*

Questions direct attention to the right code path and let the reviewed agent investigate and choose the fix. Statements prescribe the conclusion and waste the other agent's reasoning. Frame each question so a fresh agent with no prior context would investigate the right file or line.

## change_log.md and roadmap.md

Two scratch files at the repo root. Read both at the start of every session.

**`change_log.md`** — work already done. Append a section per substantial change with: date, short summary, files touched.

**`roadmap.md`** — work still owed. Five categories, in this order:

1. **Half-finished work** — anything mid-stream when a session ended. File path + what remains.
2. **Legacy code and shims** — anything pending removal. Trigger condition for the removal.
3. **Drift to address** — flagged renames, restructures, consolidations.
4. **Parked ideas** — considered and deferred.
5. **Future intentions** — planned for later.

At session start, if `roadmap.md § Half-finished` has open items, surface them before taking new instructions. When ending a session with work mid-stream, append to that section — do not leave the state implicit in chat history.

Proactively read `roadmap.md` when planning new work; if a parked idea overlaps with the user's request, raise it.

Create either file the first time it is genuinely needed. Do not stub them out empty.

## File paths

For files inside the current repo, use repo-relative paths (`src/main.py`), not absolute paths that include the user's home directory or drive letter. Absolute paths are acceptable only for files outside the repo.

## Screenshots

When the user says "screenshot," locate the most recent image in `<SCREENSHOTS_FOLDER>`, read it, and:

1. Analyze the UI/UX
2. Identify problems, bugs, or visual issues
3. Suggest efficiency or usability improvements

If `<SCREENSHOTS_FOLDER>` is still a literal placeholder, follow the "First-use setup" section above before proceeding.

## Verification before reporting done

Do not report a change as complete until you have verified it does what was asked.

- **Code changes:** if there is a quick way to run the affected code (a script, a test, a one-line repro), run it. If running requires external services (API key, network, user input), state explicitly that you have not run it and why.
- **Bug fixes:** identify the scenario that reproduces the bug and confirm it now behaves correctly — or state that you could not reproduce.
- **Refactors:** confirm the behavior of the changed code is unchanged. If you cannot prove that, say so.

If a change cannot be verified inside the current session, say so explicitly: *"Change made but not verified because X. Recommend the user run Y."*

## End-of-turn message

The last message of each turn should be brief and direct:

- One or two sentences naming what changed and the immediate next step.
- File paths in repo-relative form.
- No restatement of work the user already saw scroll past.
- No "first I did X, then Y, then Z" recap unless the user asked for one.
- Drift notices and unverified-change warnings, if any, go at the very end.

Discussion turns follow the same rule: state the conclusion and the trade-off, not the analysis path that produced it.
