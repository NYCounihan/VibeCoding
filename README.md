# VibeCoding

Vibe coding with Schematic Ventures. A series of episodes building toward an AI agent that drafts email on a user's behalf.

**Thesis:** AI email is a context problem, not a writing problem.

## Episodes

- **[Episode 1 — The Context Problem](Episodes/Episode_1/episode-01-context-problem.md)** — Six architectural principles for email agents (P1–P6). Read first.
- **[Episode 2 — Naive Prototype](Episodes/Episode_2/episode-02-naive-prototype.md)** — Autonomous build plan for a minimal drafter. Two prompts, two API calls per reply. Reads 25 sample threads to extract a context document, then drafts replies to inbound emails typed at the console.

## Running Episode 2

Episode 2's markdown file is an autonomous build plan. Drop it into a coding agent and it will create `.env`, `main.py`, `requirements.txt`, set up a virtual environment, and hand back a run command. The plan asks for your Anthropic API key during setup.

After setup:

```bash
# Linux / macOS / WSL
./venv/bin/python Episodes/Episode_2/main.py

# Windows
venv\Scripts\python.exe Episodes\Episode_2\main.py
```

First run consolidates `samples.md` into `context.md` (one API call). Subsequent runs reuse `context.md`. Pass `--rebuild` to regenerate.

## Layout

```
.
├── CLAUDE.md             working-style rules for coding agents
├── Episodes/
│   ├── Episode_1/        principles
│   └── Episode_2/        naive prototype (plan + generated code)
└── LICENSE
```

## Working style

`CLAUDE.md` at the repo root is the working-style document for any coding agent operating here. Solo developer, fast-moving, no production ceremony, root-cause debugging, simplicity first.

## License

MIT. See [LICENSE](LICENSE).
