# Consolidation Prompt

You will be given a set of email threads involving someone called USER. Read them as a group and extract **durable** patterns — things that hold across multiple threads or that USER does consistently. Discard one-time details specific to a single thread.

Output a markdown document with the sections below, in this exact order. Be specific and concrete. Do not invent biographical details that are not visible in the threads.

---

## How to write entries

- **Imperative form for rules.** *"Use `Best,` as signoff with formal contacts,"* not *"USER uses `Best,` with formal contacts."*
- **Concrete, not vague.** Name actual places, times, signoffs, phrases USER uses. Avoid labels like *"professional tone"* without saying what makes it professional.
- **Cite evidence strength.** If a pattern is seen in only one or two threads, label it weak: *"seen in 1 thread; may not be a pattern."* If it appears in many, label it strong.
- **Note conflicts; do not resolve them silently.** When two threads show different behavior within the same category (e.g., two different signoffs in what looks like the same relationship type), note the conflict in the entry.
- **Separate tone from fact.** Tone = *how* USER says things (style, signoff, length, phrasing). Fact = *what* USER does or arranges (places, times, scheduling habits). Keep them in their respective sections; do not blend.

---

## Output sections

### Global rules and facts about USER

Things that hold across most or all of USER's emails, regardless of recipient. Only include items visible in the threads.

- Days of the week USER prefers or avoids
- Times of day USER consistently chooses
- Default behavior when scheduling (proposing specifics vs asking for preferences)
- Default message length (e.g., "shorter than the inbound message")
- Confirmation and rescheduling habits visible across categories
- Where USER lives or works, only if directly stated or implied repeatedly

Each entry is one line, imperative or factual.

### Tone profiles by relationship category

Cluster the recipients into the smallest set of categories the threads actually reveal — typically three to five (examples: close peer, formal external contact, friendly internal colleague, family, junior contact). For each category:

- **Category name** plus a one-line description of who falls into it
- **Signoff** USER uses (exact string, or "none" if USER omits a signoff in this category)
- **Greeting style** (formal name, first name, none)
- **Average message length** (one line, two lines, paragraph)
- **Capitalization and punctuation** (lowercase casual? full sentences? abbreviations?)
- **Distinguishing phrasings** if any appear more than once

If a category contains internal conflict, note it on that category's entry.

### People and relationships

For each recipient or relationship type appearing in the threads:

- One-line identity sketch drawn from thread content only — no speculation about employer, role, or backstory beyond what the threads say
- Which tone-profile category from the section above fits
- Any durable factual claim the recipient has made about themselves worth carrying forward (e.g., a stated location, time constraint, or recurring topic)

### Recurring places, times, and topics

Bulleted, with thread count:

- Places USER has suggested in two or more threads
- Times of day or week that recur across categories
- Topics or scenarios that recur across threads

### Patterns and conventions

Catch-all for durable patterns not covered above:

- How USER opens emails (any recurring opening phrase)
- How USER handles rescheduling, alternatives, and confirmation
- How length, warmth, and formality scale with the relationship category
- Other patterns that meet the durable bar

---

## What is NOT durable — do not extract

- The specific time and place of a single meeting that does not recur in any other thread
- A name, anecdote, or fact mentioned in only one thread
- One-off apologies, jokes, or stylistic flourishes
- The verbatim content of any specific reply
- Any inference about USER's profession, employer, family, beliefs, or personal life that is not directly stated in the threads

When in doubt, leave it out. The output should be a portrait of recurring behavior, not a transcript of incidents.

---

## Output rules

- Base every entry on direct evidence in the threads.
- Do not invent biographical details.
- When two memories say essentially the same thing, merge them into one concise entry — do not output near-duplicates.
- Output only the markdown document. No preamble, no commentary, no meta-explanation of what you were asked to do.
