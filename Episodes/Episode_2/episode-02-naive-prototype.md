# Episode 2 — Build Plan

This file is an autonomous build plan for a coding agent. When the user drops this file into a coding agent's terminal, your job is to run the five steps below in order, in one pass, without pausing for permission between steps:

1. Verify the source files described in Step 1 are present.
2. Ask the user for the Anthropic API key (Step 2).
3. Create three files (Step 3): `.env`, `main.py`, `requirements.txt`.
4. Set up a Python virtual environment and install dependencies (Step 4).
5. Print the final run command for the user (Step 5).

The only pauses you take are: Step 2 (waiting for the user's API key), and the end (handing off to the user to actually run the script).

This is the artifact for podcast episode 2. The thesis: AI email is a context problem, not a writing problem. The project reads 25 sample email threads, asks an AI to extract the facts and tones visible across them, then uses that extracted context to draft replies to inbound emails the user types into the console.

## Where this plan lives in the repo

```
<repo root>/
├── CLAUDE.md                                    (working-style rules — read first)
├── .gitignore                                   (repo-wide)
└── Episodes/
    └── Episode_2/
        ├── episode-02-naive-prototype.md        (this file)
        ├── samples.md                           (25 threads — input)
        ├── prompts/
        │   ├── consolidate.md
        │   └── respond.md
        ├── main.py                              (you will create)
        ├── requirements.txt                     (you will create)
        └── context.md                           (generated on first run)
```

The repo root is two directories above this file.

---

## Step 1 — Verify source files

You will find these files. Do not modify them — they are the source material.

- **`CLAUDE.md`** at the repo root — reusable working-style rules. Read first.
- **`samples.md`** in this folder — 25 email threads.
- **`prompts/consolidate.md`** in this folder — prompt for context extraction.
- **`prompts/respond.md`** in this folder — prompt for reply drafting.

If any are missing, stop and tell the user before doing anything else.

The repo-root `.gitignore` is also already present and includes `.env`.

---

## Step 2 — Ask the user for the API key

Ask, in one short message:

> *"What's your Anthropic API key? I'll save it to `.env` at the repo root, which is gitignored. The key will appear in this chat transcript — that's the trade-off for setting this up autonomously."*

Wait for the user's reply. Do not guess. Do not use a placeholder.

After printing the key write confirmation in Step 3, do not echo the key back in any later message.

---

## Step 3 — Create three files

Create these files with the literal contents shown below. Use the value the user provided in Step 2 for `<API_KEY>`.

### `.env` at the repo root

```
ANTHROPIC_API_KEY=<API_KEY>
```

### `Episodes/Episode_2/main.py`

```python
import sys
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()
MODEL = "claude-sonnet-4-6"

ROOT = Path(__file__).parent
SAMPLES = ROOT / "samples.md"
CONTEXT = ROOT / "context.md"
CONSOLIDATE_PROMPT = ROOT / "prompts" / "consolidate.md"
RESPOND_PROMPT = ROOT / "prompts" / "respond.md"


def consolidate() -> None:
    instructions = CONSOLIDATE_PROMPT.read_text()
    samples = SAMPLES.read_text()
    full_prompt = f"{instructions}\n\n# Email threads\n\n{samples}"
    response = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        messages=[{"role": "user", "content": full_prompt}],
    )
    CONTEXT.write_text(response.content[0].text)


def respond(inbound: str) -> str:
    instructions = RESPOND_PROMPT.read_text()
    context = CONTEXT.read_text()
    full_prompt = (
        f"{instructions}\n\n"
        f"# Context about USER\n\n{context}\n\n"
        f"# Inbound email\n\n{inbound}"
    )
    response = client.messages.create(
        model=MODEL,
        max_tokens=800,
        messages=[{"role": "user", "content": full_prompt}],
    )
    return response.content[0].text


def read_email_from_stdin() -> str | None:
    print('Paste or type an inbound email. Blank line to submit. Type "quit" to exit.')
    lines: list[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            return None
        stripped = line.strip().lower()
        if stripped == "quit":
            return None
        if line == "" and lines:
            return "\n".join(lines)
        if line == "" and not lines:
            continue
        lines.append(line)


def main() -> None:
    rebuild = "--rebuild" in sys.argv
    if rebuild or not CONTEXT.exists():
        print("Consolidating sample emails into context.md (one-time setup)...")
        consolidate()
        print(f"Wrote {CONTEXT.name}. Open and edit it before drafting if you want to.\n")
    else:
        print(f"Using existing {CONTEXT.name}. Pass --rebuild to regenerate.\n")

    while True:
        inbound = read_email_from_stdin()
        if inbound is None:
            print("Goodbye.")
            return
        if not inbound.strip():
            continue
        print("\n--- DRAFT REPLY ---")
        print(respond(inbound))
        print("--- END ---\n")


if __name__ == "__main__":
    main()
```

### `Episodes/Episode_2/requirements.txt`

```
anthropic>=0.40.0
python-dotenv>=1.0.0
```

---

## Step 4 — Create venv and install dependencies

From the repo root, create a virtual environment and install the dependencies into it using the venv's pip directly (no shell activation required):

**Linux / macOS / WSL:**

```bash
python -m venv venv
./venv/bin/pip install -r Episodes/Episode_2/requirements.txt
```

**Windows (PowerShell or CMD):**

```powershell
python -m venv venv
venv\Scripts\pip.exe install -r Episodes\Episode_2\requirements.txt
```

Detect the platform and pick the correct path. Confirm pip exited 0 before moving on.

Then verify the install with a one-line import smoke test:

```bash
./venv/bin/python -c "import anthropic, dotenv; print('ok')"
```

(or `venv\Scripts\python.exe` on Windows). If this prints `ok`, dependencies are good. If it errors, stop and surface the error.

---

## Step 5 — Print the run command

Print this to the user as your final message:

> *Setup complete. To run the email drafter (single command, no activation needed):*
>
> *Linux / macOS / WSL:*
> ```bash
> ./venv/bin/python Episodes/Episode_2/main.py
> ```
>
> *Windows (PowerShell or CMD):*
> ```powershell
> venv\Scripts\python.exe Episodes\Episode_2\main.py
> ```
>
> *First run consolidates the 25 sample threads into `context.md` (~10–20 seconds, one API call), then prompts you for an email. Subsequent runs reuse `context.md`. Pass `--rebuild` to regenerate.*

Do not run `python main.py` yourself — that triggers a paid API call. Let the user run it.

---

## How the script behaves (reference for code generation)

Architecture in one sentence:

```
SETUP (runs once)                            RUNTIME (every user input)
─────────────────────────                    ─────────────────────────────
samples.md  ─┐                               typed email  ─┐
             ├─► AI ─► context.md ──────────────────────────┼─► AI ─► drafted reply
consolidate.md ─┘                            respond.md   ─┘
```

Runtime behavior:

1. On startup, the script checks for `context.md`.
2. If absent, or if `--rebuild` is passed on the command line, the script reads `samples.md` and `prompts/consolidate.md`, sends them together to the model in a single API call, and writes the model's response to `context.md`.
3. Otherwise, the script prints a one-line note saying the existing `context.md` will be used.
4. The script enters an input loop. It prompts the user to paste or type an inbound email. A blank line submits. Typing `quit` exits.
5. For each submitted email, the script reads `context.md` and `prompts/respond.md`, concatenates them with the inbound email into a single prompt, sends one API call, and prints the result between `--- DRAFT REPLY ---` and `--- END ---` markers.
6. After printing a draft, the script loops back to the input prompt.

Code-generation constraints (the embedded `main.py` already satisfies these — these are here for any reimplementation):

- Use the `anthropic` Python SDK and `python-dotenv`.
- Model: `claude-sonnet-4-6`.
- `load_dotenv()` at module top; the `.env` file lives at the repo root and `load_dotenv()` walks up from cwd to find it.
- The Anthropic client is instantiated once at module scope.
- Use `pathlib.Path` resolved against `__file__` so paths work regardless of cwd.
- Consolidation `max_tokens`: 4000. Reply `max_tokens`: 800.
- `samples.md`, `context.md`, `prompts/consolidate.md`, `prompts/respond.md` are sibling references to `main.py`.

---

## Acceptance criteria

After all five steps complete:

1. `.env` exists at the repo root with `ANTHROPIC_API_KEY=` followed by the value the user provided. Do not echo the value in any subsequent message.
2. `Episodes/Episode_2/main.py` exists with the contents above.
3. `Episodes/Episode_2/requirements.txt` exists with the contents above.
4. `<repo root>/venv/` exists and the import smoke test prints `ok`.
5. `git status` does not show `.env` as a tracked file.
6. The user has been given the final run command.

Stop after step 5. Do not add tests, lint config, README updates, or any folder structure beyond what's specified. Do not create a CI workflow.

---

## What this project is not

Not Gmail. Not multi-turn within a thread. Not an agent loop. Two prompts and at most two API calls per reply. Resist the urge to add anything else.
