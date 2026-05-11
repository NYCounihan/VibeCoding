# Architectural Principles for Email Agents

Reference document for anyone building an AI agent that drafts email on behalf of a user.

The thesis of this document is one sentence: **AI email is a context problem, not a writing problem.** Everything below is a consequence of that.

Each principle is independent. Read them in any order.

---

## P1 — The model is not the system

Writing quality is bounded by the context delivered to the model, not by the model's eloquence. Improvements to an email agent come from improving the system *around* the model — what context exists, how it is selected, how it flows into the prompt — not from rewording the prompt.

**Failure mode it prevents:** the team rewrites the same drafter prompt seven times trying to fix problems caused upstream of the prompt.

**How to apply:** when a draft is wrong, list what the model did not know that a competent human would have known. Each gap is a system change, not a prompt change.

---

## P2 — Tone is relational, not global

Users do not have one voice. They write differently to peers, to formal contacts, to family, to senior contacts, to junior contacts, to strangers. A single "USER's tone" instruction collapses all of those into a bland average that sounds wrong everywhere.

**Failure mode it prevents:** drafts that are technically correct but sound off — too formal to a friend, too casual to a vendor.

**How to apply:** cluster the user's contacts into a small number of categories visible in their actual past correspondence. Maintain one tone profile per category. Classify the inbound sender into a category before drafting.

---

## P3 — Two pools of facts: global and local

The agent needs two distinct pools of facts:

- **Global facts** — true across most of the user's emails: positioning, default scheduling habits, recurring places, conventions, language used to describe the user's work.
- **Local facts** — true only of one company, one project, one contact, or one thread: prior commitments, in-progress conversations, ongoing terms, names, specifics.

Both are required. A draft that misses global facts sounds generic. A draft that misses local facts sounds amnesiac.

**How to apply:** build extraction and retrieval separately for each pool. Refresh global facts infrequently. Refresh local facts per thread or per contact.

---

## P4 — Global and local facts must stay separate

Global and local facts must not be merged into a single context blob.

- A local fact can override a global default. The user prefers Wednesday mornings *in general*, but already agreed to Thursday at 8 *with this contact*. The local arrangement wins.
- A local fact must not leak across threads. A price discussed with one contact must not surface in a reply to another.
- The model must know not only what is *true*, but what is *allowed* to be used in this particular message.

**Failure modes it prevents:** (a) a global default overriding the right local arrangement; (b) private local facts surfacing in the wrong reply.

**How to apply:** pass global and local context as separately named blocks into the prompt. Tag each local fact with its scope (contact, company, thread). Filter local facts to the current relationship before they reach the drafter.

---

## P5 — Decompose the work; do not overload one prompt

A single prompt asked to do all of the following at once will produce mediocre output even when every input is correct:

- Understand the sender
- Classify the email
- Retrieve relevant context
- Apply the right tone
- Respect privacy and scope boundaries
- Write the final response

These have different optimal prompts, different evaluation criteria, and different failure modes. Asking one model call to balance them implicitly produces an output that does each acceptably and none of them well.

**How to apply:** decompose into separate model calls, one job each. The structured output of each becomes the input of the next.

---

## P6 — Plan, validate, execute

The minimum useful decomposition is three stages:

1. **Plan** — what should this email accomplish? Classify the sender, decide the action, outline the response intent. Do not draft yet.
2. **Validate** — do we have the facts, tone profile, and scoping rules needed? Is anything missing? Is anything in the plan out of scope for what is allowed?
3. **Execute** — write the draft, following the plan and using only the validated facts.

**Why it matters:** plan and execute have different optima. A model trying to plan and draft simultaneously will sometimes write a perfectly readable email that answers the wrong question. Splitting the steps surfaces that mistake at the plan stage where it is cheap to fix.

**How to apply:** make each stage a separate prompt with structured output. Persist each intermediate output so it can be inspected later when a draft turns out wrong. The persisted plan, validated context, and draft together are usually enough to diagnose any specific failure.

---

## Reading guide

If you take only one thing from this document: **before improving the model, improve what the model knows.** Tone, local facts, global facts, scope rules, and the plan-validate-execute split are six different ways to give the model more of what it needs, separated cleanly enough that the system can be debugged when it fails.

Code, agents, memory systems, and infrastructure are the *implementation* of these principles. They are not the principles themselves. Pick implementations that preserve the separations above, not ones that re-merge them in the name of simplicity.

---

# Taxonomies — starter categories

The principles above tell you to classify, decompose, and scope. They do not say *into what*. This section provides starter taxonomies for each classification a builder will have to make. They are generalized for any business user — narrow or replace them to fit the user you are building for.

Treat these as starting points, not exhaustive lists. Most systems will use a subset of each.

---

## 1. Relationship categories (used by P2 — tone profiles)

A small set of buckets that a sender can be assigned to. Each maps to one tone profile, one signoff, one length norm, and one set of allowed local facts.

- **Inner circle** — co-founder, business partner, spouse, immediate family, oldest friends. Lowercase casual; no salutation; no signoff; fragments allowed.
- **Direct report** — someone the user manages. Direct, structured, sometimes feedback-laden; usually first-name greeting, brief signoff.
- **Internal peer** — colleagues at the same level. Friendly, concise, full sentences, casual signoff.
- **Internal senior** — manager, executive, board. Concise, polished, deferential without being formal; consistent signoff.
- **External vendor** — paid service providers, contractors, agencies. Polite professional; clear asks; standard signoff.
- **External client / customer** — current paying counterparty. Warm professional; protective of relationship; standard signoff; sometimes longer.
- **External prospect** — potential client/customer not yet contracted. Warmer than vendor, careful with commitments; standard signoff.
- **External partner** — non-monetary collaborator (joint work, alliance). Treated as a peer-of-the-org; relationship-driven.
- **Industry peer** — counterparts at other organizations. Cordial, comparing-notes register; first-name greeting.
- **Mentor** — someone the user is junior to. Concise, respectful of their time; no padding; standard signoff.
- **Mentee** — someone seeking the user's advice. Warm but brief; direct; standard signoff.
- **Personal acquaintance** — friends-of-friends, alumni, social-context contacts. Friendly but light; no business pretext; minimal signoff.
- **Family (extended)** — relatives outside the inner circle. Warm casual; greeting and signoff vary by person.
- **Cold contact / stranger** — first-touch contacts the user has not previously engaged with. Polite, brief, may decline to engage at all.
- **Automated / no-reply** — system messages, calendar notifications. No reply expected.

---

## 2. Sender intent (used by P5 — what is the sender doing?)

What the inbound email is *trying to accomplish*. Independent of relationship.

- **Scheduling** — propose, accept, decline, reschedule, or cancel a meeting.
- **Information request** — asking the user for facts, opinions, or guidance.
- **Information share** — sending an update, FYI, or read-only news.
- **Decision request** — asking the user to approve, sign off, or pick between options.
- **Action request** — asking the user to do something (review, send, fix, complete).
- **Introduction request** — asking to be connected to a third party, or offering an intro.
- **Follow-up** — checking on a prior commitment, conversation, or task.
- **Acknowledgment** — thanks, confirmation, simple receipt.
- **Negotiation** — discussing terms, price, scope, or timing.
- **Sales / pitch** — promotional or inbound pitch from a vendor or prospect.
- **Personal / relational** — non-task email about life, wellbeing, or casual catch-up.
- **Logistics** — practical coordination (address, time, link, attachment).
- **Complaint / pushback** — disagreement, escalation, dissatisfaction.
- **Apology** — sender acknowledging fault or delay.
- **Automated / informational-only** — receipts, notifications, system mail.

---

## 3. Reply category (used by P5 — what kind of reply fits)

What the user's response is going to *do*. Often constrained by sender intent.

- **Accept** — agree to the proposed action without modification.
- **Decline** — refuse politely with or without reason.
- **Propose alternative** — counter with a different time, scope, or approach.
- **Defer** — postpone the decision without rejecting it.
- **Ask clarifying question** — request more information before committing.
- **Provide information** — answer a factual ask.
- **Provide opinion** — share judgment or recommendation.
- **Forward / route** — pass to the right person.
- **Brief acknowledgment** — thanks / got-it / received.
- **No reply** — intentionally do not respond.
- **Schedule logistics** — arrange or finalize a meeting.
- **Negotiate** — counter on terms.
- **Escalate** — flag concern or raise to a higher contact.
- **Apologize** — make amends.
- **Close** — wrap up a thread that has reached its end.

---

## 4. Sensitivity dimensions (used by P4 — what must be protected)

Independent flags that can apply to any email. An email can carry several at once.

- **Privacy** — contains personal/private information; do not forward.
- **Confidentiality** — covered by NDA, employment terms, or regulatory rules.
- **Time-sensitive** — needs response within hours, not days.
- **Reputational** — could damage the user or the counterparty if mishandled.
- **Financial** — involves money, pricing, or contractual commitment.
- **Legal** — implicates contracts, intellectual property, or liability.
- **Emotional** — carries social weight: frustration, grief, joy, conflict.
- **Public-facing** — could be quoted, screenshotted, or leaked.
- **Internal-only** — must not leave the organization.
- **Third-party named** — names a person not on the thread; consider implications before forwarding or quoting.

---

## 5. Scope of local facts (used by P3 + P4 — where does this fact apply)

The boundary outside which a local fact must not appear.

- **Thread-scoped** — applies only inside this email chain.
- **Contact-scoped** — applies whenever the user emails this person, across threads.
- **Company-scoped** — applies whenever the user engages with anyone at this organization.
- **Project-scoped** — applies whenever the user works on this initiative, regardless of counterparty.
- **Event-scoped** — applies during the run of a specific event, conference, or quarter, then expires.
- **Role-scoped** — applies to anyone in a certain role (e.g., recruiters, customers, lawyers).
- **Time-scoped** — applies until a specific date or condition (e.g., "until contract is signed").
- **One-off** — single-use; not durable; should not be re-applied.

Most local facts should carry at least one scope tag. A fact with no scope is a liability.

---

## 6. Global facts categories (used by P3 — what kinds of facts hold across all emails)

The pool of facts the user wants applied in most outbound emails, regardless of who the recipient is.

- **Identity** — the user's name, role, title, organization, and how the user prefers to be addressed.
- **Positioning** — what the user does, how the user describes their work, what the user is known for.
- **Scheduling preferences** — preferred days, times, meeting durations, default venues, preferred channels (in-person, phone, video).
- **Calendar / availability** — vacation, out-of-office, blocked periods, recurring commitments.
- **Communication conventions** — greetings, signoffs, length norms, when to use which.
- **Operating procedures** — how the user handles introductions, declines, follow-ups, escalations.
- **Scope of engagement** — what the user does and does not take meetings on; categories the user routinely declines.
- **Standard answers** — recurring questions the user receives and the user's preferred responses to each.
- **Contact preferences** — preferred channels, response cadence, expectations on turnaround.
- **Recurring people** — colleagues, partners, family, advisors who show up in many threads and are part of the user's regular cast.
- **Recurring places** — venues the user returns to (coffee shops, restaurants, offices).
- **Recurring topics** — themes the user repeatedly engages with.

---

## 7. Local facts categories (used by P3 — what kinds of facts apply to one relationship or thread)

The pool of facts that only apply within a specific scope. Each should carry a scope tag from section 5.

- **Counterparty identity** — name, role, organization, mutual context, how the user and counterparty know each other.
- **Relationship history** — last interaction, prior topics, current stage of the relationship.
- **Active commitments** — what the user or counterparty has promised in prior emails.
- **Open questions** — outstanding asks waiting for resolution.
- **In-progress scheduling** — dates, times, or places under discussion but not yet confirmed.
- **Documents and artifacts** — files, links, notes shared in the thread or relationship.
- **Decisions already made** — what was agreed in prior turns; should not be re-litigated.
- **Restrictions** — what can or cannot be shared with this counterparty.
- **Stage / status** — where the relationship is in its lifecycle (e.g., early outreach, active engagement, paused, closed).
- **Cadence** — how often the user and counterparty typically engage.

---

## 8. Action categories (used by P6 — what the reply should accomplish)

The verb of the planned reply. Often one primary action per reply; sometimes two (e.g., schedule + inform).

- **Schedule** — book, move, cancel, or confirm a meeting.
- **Inform** — share information, requested or proactive.
- **Decide** — communicate a choice or approval.
- **Defer** — request more time or postpone.
- **Ask** — request information, clarification, or action from the sender.
- **Acknowledge** — confirm receipt without further action.
- **Decline** — refuse a request or invitation.
- **Negotiate** — propose terms different from what was offered.
- **Introduce** — connect the sender to a third party.
- **Forward** — pass to the right recipient.
- **Escalate** — flag a concern to a more senior or appropriate contact.
- **Apologize** — make amends for an error or delay.
- **Close** — wrap up a thread that has reached its end.
- **Reschedule** — change a previously-agreed arrangement.

---

## 9. Validation dimensions (used by P6 — what to check before sending)

What the validation step should confirm. Usually a checklist; can be implemented as code, model, or both.

- **Tone match** — does the draft match the tone profile for the sender's relationship category?
- **Fact correctness** — are facts cited in the draft actually true and current?
- **Fact permission** — is each cited fact allowed to be shared with this recipient (scope check)?
- **Scope drift** — does the draft address only what was asked, or expand into adjacent topics?
- **Completeness** — does the draft address every ask in the inbound?
- **Calendar consistency** — does any scheduling proposal match the user's actual availability?
- **Commitment tracking** — does the draft introduce a new commitment? Is the commitment intended?
- **Recipient accuracy** — are the recipients on the right thread? Any cc/bcc that should not be there?
- **Privacy** — does the draft leak local facts outside their scope?
- **Tone red flags** — defensive phrasing, passive aggression, overpromising, hedging when clarity is needed.

---

## How to use these taxonomies

For each principle, pick the subset of categories that match the user you are building for. A solo founder's taxonomy will differ from an executive's; a salesperson's from an academic's. The goal of these lists is to make the choice explicit rather than implicit — a system that ignores `Sensitivity` is making the choice "all emails have the same sensitivity," and that choice has consequences.

If a category in any of these lists never applies to your user, delete it. If a category is missing, add it. The principles are universal; the categories are configuration.
