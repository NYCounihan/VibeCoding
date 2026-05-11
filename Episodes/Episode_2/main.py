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
