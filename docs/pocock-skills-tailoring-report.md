# Tailoring the Matt Pocock Skill Set to Solution Engineering in Microsoft 365

**Source repository:** `https://github.com/mattpocock/skills` (read in full: `README.md`, `CLAUDE.md`, `CONTEXT.md`, `.agents/adr/*`, `.agents/invocation.md`, `.agents/writing-docs.md`, and every `SKILL.md` and reference file under `skills/`).

**Scope note:** the repository has no root `AGENTS.md`. Its agent-facing conventions live in `CLAUDE.md` and in `.agents/`, and this report treats those as the equivalent material.

**Reading rule used throughout:** every skill is split into its **mechanism** (the thing that makes it effective) and its **surface** (the TypeScript, npm, GitHub, and web-application details it happens to be written in). Mechanisms are carried across unchanged. Only surfaces are translated. Where a proposed translation risks weakening a mechanism, it is flagged explicitly.

---

## 1. Executive summary

### What this skill system is

It is a set of 37 small, composable agent skills organized into five buckets under `skills/`. Twenty-five of them are "promoted" (the `engineering/` and `productivity/` buckets, which ship in the Claude Code plugin); the rest sit in `misc/`, `in-progress/`, and `deprecated/`. `CLAUDE.md` states the rule directly: "the Claude Code plugin ships exactly the promoted set."

The system deliberately refuses to own your process. The README is explicit about this: "Approaches like GSD, BMAD, and Spec-Kit try to help by owning the process. But while doing so, they take away your control and make bugs in the process hard to resolve." What it ships instead is a set of independent disciplines you assemble yourself, plus one router skill (`ask-matt`) that tells you which one fits the situation you are in.

The skills split on exactly one axis, documented in `.agents/invocation.md`: **user-invoked** skills are "reachable only by the human typing its name" and exist to orchestrate; **model-invoked** skills are "reachable by model or user" and hold reusable discipline. A user-invoked skill may call model-invoked skills but "can never reach another user-invoked one." This matters for adoption because it tells you which skills you must remember to fire and which the agent will reach for on its own.

### Why the mechanisms transfer

The README frames the whole set around four failure modes. Read them without the TypeScript framing and every one of them is a Solution Engineering failure mode, usually a worse one:

1. **"The agent didn't do what I want."** The README calls this "the most common failure mode in software development": misalignment. In Solution Engineering the gap is wider than in application development, because the person specifying the work is a business process owner who does not know what the platform can do, and the person building it does not know the business process. The fix, a forced interview before any build, is more valuable here than it is in a codebase you own end to end.

2. **"The agent is way too verbose."** The README's answer is a shared language document, quoting Eric Evans: "With a ubiquitous language, conversations among developers and expressions of the code are all derived from the same domain model." Microsoft 365 work is drowning in overloaded vocabulary before you add any business jargon: site, site collection, hub, list, library, flow, workflow, process, agent, bot, Copilot, owner, approver, requester. A controlled vocabulary is not a nicety here; it is the difference between a SharePoint column named `Owner` meaning three different things in three solutions.

3. **"The code doesn't work."** The README's answer is feedback loops: "Without feedback on how the code it produces actually runs, the agent will be flying blind." This is where the transfer is hardest and most valuable, because Microsoft 365 work has genuinely fewer loops than a TypeScript application. Section 4 of this report is dedicated to that gap.

4. **"We built a ball of mud."** The README's answer is design discipline: deep modules behind small interfaces. A tenant with 200 uncatalogued flows, each with hardcoded site URLs and personal-account connections, is the same failure with a different file extension.

The disciplines in this repository are, at their core, forced alignment before execution, controlled vocabulary, a written decision record, small proving runs before large commitments, objective pass criteria before progression, and review that separates "does it meet standard" from "does it meet the requirement." None of those are properties of TypeScript. All of them are properties of well-run technical work.

### The three highest-leverage skills to adopt first

These three are chosen on one criterion beyond value: they work on day one with no source-control repository, no issue tracker, and no configuration. That matters, because a large share of Microsoft 365 solution work today has none of those things.

**1. `grill-with-docs`** (`skills/engineering/grill-with-docs/SKILL.md`, which is a two-line wrapper: "Call the Skill tool twice, for 'grilling' and 'domain-modeling'").

This is the single highest-return skill for your work. It attacks failure modes 1 and 2 at the same time, and it produces the `CONTEXT.md` glossary and the decision records as a byproduct of doing work you were going to do anyway. Adopt this before anything else. The README calls the two skills it wraps "my most popular skills" and says to "use them *every* time you want to make a change."

**2. `diagnosing-bugs`** (`skills/engineering/diagnosing-bugs/SKILL.md`).

Its Phase 1 rule is the thing Microsoft 365 troubleshooting most lacks: "If you catch yourself reading code to build a theory before this command exists, **stop: jumping straight to a hypothesis is the exact failure this skill prevents.** No red-capable command, no Phase 2." The normal failure pattern in this space is opening flow run history, reading the red step, forming a theory, changing something, and rerunning by hand. That is hypothesizing without a loop. The skill's refusal to allow it is worth more here than in a codebase where a test suite already exists.

**3. `wizard`** (`skills/engineering/wizard/SKILL.md`).

This is the most platform-specific win available. Microsoft 365 delivery is full of steps only a person with the right role can take: granting admin consent for Graph permissions, creating a connection reference under a service account, assigning a premium connector license, publishing an agent to a specific audience, approving a data loss prevention policy exception. The skill's own description names exactly this class of work: "provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover." It converts a procedure you re-explain every time into a staged, confirmation-gated runbook that captures values and writes them where they belong. The only translation needed is the scripting language.

The immediate next two, once a repository exists, are `to-tickets` (for the tracer-bullet mechanism) and `code-review` (for the two-axis separation). Both are covered in full below.

---

## 2. Mechanism inventory

These are the recurring disciplines across the repository. For each: what the mechanism actually is, and the operational-discipline analogue that will make it stick for you. The analogues are memory hooks and framing. They are not substitutes, and adopting the analogue without the mechanism gets you nothing.

### 2.1 Grilling: forced alignment before execution

**The mechanism.** `skills/productivity/grilling/SKILL.md` defines an interview run in rounds over a **design tree**. The key structural idea is the **frontier**: "every decision whose prerequisites are already settled: the questions you can ask *now* without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round."

Three rules make it work, and all three are load-bearing:

- **Recommended answers are attached to every question.** This converts an open interrogation into a review of proposals, which is far faster and surfaces disagreement rather than inviting invention.
- **Facts are the agent's job, decisions are yours.** "Finding *facts* is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it; don't ask the user for anything you could look up yourself."
- **Completion is objective.** "The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding."

**The analogue.** This is an **alignment readback** before execution: the person who will do the work restates the requirement back to the person who set it, in enough structured detail that a misunderstanding surfaces before any effort is spent, and the work does not start until the readback is confirmed. The frontier discipline is what stops the readback from being a flat checklist: you cannot confirm a downstream decision before the upstream one is settled, so the questions arrive in dependency order.

**Do not weaken it by:** answering your own questions to speed the session up, or acting on a partially resolved frontier. `wayfinder` names this failure explicitly for its human-in-the-loop tickets: "a grilling agent that answers its own questions has broken this."

### 2.2 `CONTEXT.md`: controlled vocabulary as a working artifact

**The mechanism.** `skills/engineering/domain-modeling/SKILL.md` and `CONTEXT-FORMAT.md` define a glossary that is opinionated and exclusive. Each term gets a one or two sentence definition and an explicit `_Avoid_` list of the words it displaces. The rules are strict:

- "**Be opinionated.** When multiple words exist for the same concept, pick the best one and list the others under `_Avoid_`."
- "`CONTEXT.md` should be totally devoid of implementation details. Do not treat `CONTEXT.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else."
- "**Only include terms specific to this project's context.** General programming concepts ... don't belong even if the project uses them extensively."

The active discipline is what gives it teeth: challenge terms against the glossary in the moment ("Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"), sharpen fuzzy language ("You're saying 'account': do you mean the Customer or the User?"), and "update `CONTEXT.md` right there. Don't batch these up."

The repository's own `CONTEXT.md` demonstrates the payoff, including a **Flagged ambiguities** section that records resolutions: "'backlog' was previously used to mean both the *tool* hosting issues and the *body of work* inside it. Resolved: the tool is the **Issue tracker**."

**The analogue.** This is a **controlled vocabulary and reporting standard**: one agreed term per concept, published, with the displaced synonyms named so people stop reaching for them. The `_Avoid_` list is the part most glossaries omit and the part that does the work, because it is what lets you correct drift without arguing about it.

**Do not weaken it by:** letting it become a design document. The moment implementation detail enters, it stops being cheap to read every session and people stop reading it.

### 2.3 Architecture decision records: a decision log attached to the execution plan

**The mechanism.** `skills/engineering/domain-modeling/ADR-FORMAT.md` keeps the format almost aggressively small: "An ADR can be a single paragraph. The value is in recording *that* a decision was made and *why*, not in filling out sections." Status, considered options, and consequences are all optional.

The discipline is entirely in the gate. A record is written only when all three of these hold:

> 1. **Hard to reverse**: the cost of changing your mind later is meaningful
> 2. **Surprising without context**: a future reader will look at the code and wonder "why on earth did they do it this way?"
> 3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

And the reasoning behind the gate: "If a decision is easy to reverse, skip it: you'll just reverse it. If it's not surprising, nobody will wonder why. If there was no real alternative, there's nothing to record beyond 'we did the obvious thing.'"

**The analogue.** This is a **decision log attached to the execution plan**: a short, dated record of the choices that constrain everything downstream, kept so that the next person to touch the work does not silently undo a deliberate decision, and so that a decision does not get relitigated every quarter by whoever arrives next. The three-part gate is what stops it becoming a change log nobody reads.

**Do not weaken it by:** writing one per change. A decision log with 80 entries has the same practical value as no decision log.

### 2.4 Tracer bullets: small proving runs that de-risk the larger effort

**The mechanism.** `skills/engineering/to-tickets/SKILL.md` defines a slice rule that is short and unambiguous:

> - Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests): vertical, NOT a horizontal slice of one layer
> - A completed slice is demoable or verifiable on its own
> - Each slice is sized to fit in a single fresh context window

`tdd` names the opposing failure mode: "**Horizontal slicing**: writing all tests first, then all implementation. Bulk tests verify *imagined* behavior."

Two supporting pieces matter as much as the slice rule. First, **blocking edges**: every ticket declares which tickets must complete before it can start, and work proceeds on the **frontier**, "any ticket whose blockers are all done." Second, the **exception**, which is unusually well thought out: wide mechanical refactors do not fit the tracer-bullet shape at all, so the skill sequences them as expand, migrate in batches, contract, "keeping CI green batch to batch because the old form still exists."

**The analogue.** This is a **small proving run that de-risks the larger effort**: before committing the full build, you push one narrow but genuinely complete path all the way through, so that every integration point, permission, and assumption is tested against reality rather than against a design document. The thing being proved is not the feature. It is the path.

**Do not weaken it by:** slicing by layer because layers are easier to estimate. "Build all the SharePoint lists, then build all the flows, then build the agent" is horizontal slicing and it defers every integration risk to the end.

### 2.5 Red-green loops: gated progression with objective pass criteria

**The mechanism.** `skills/engineering/tdd/SKILL.md` states the loop rules plainly:

> - **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
> - **One slice at a time.** One seam, one test, one minimal implementation per cycle.
> - **Refactoring is not part of the loop.** It belongs to the review stage (see the `code-review` skill), not the red → green implementation cycle.

The **seam** discipline is what keeps the tests worth having: "**Test only at pre-agreed seams.** Before writing any test, write down the seams under test and confirm them with the user. No test is written at an unconfirmed seam. You can't test everything, so agreeing the seams up front is how testing effort lands on the critical paths and complex logic instead of every edge case."

And the anti-patterns are precise. **Tautological** tests are the one most often reinvented by accident: "the assertion recomputes the expected value the way the code does ... so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth."

**The analogue.** This is **gated progression with objective pass criteria**: you do not advance to the next stage until the current one has demonstrably passed a check that was defined before the work started and that can genuinely fail. The "red before green" rule is the operational heart of it. A check that has never been observed to fail is not a check; it is a formality.

**Do not weaken it by:** writing the check after the build and confirming it passes. That is the single most common way this discipline is hollowed out, and it produces a check that cannot fail.

### 2.6 Phase-gated diagnosis

**The mechanism.** `skills/engineering/diagnosing-bugs/SKILL.md` runs six phases with hard gates between them. Phase 1 builds a feedback loop and nothing proceeds without it:

> **This is the skill.** Everything else is mechanical. If you have a **tight** pass/fail signal for the bug (one that goes red on *this* bug), you will find the cause; bisection, hypothesis-testing, and instrumentation all just consume it. If you don't have one, no amount of staring at code will save you.

The completion criterion for Phase 1 is objective and observed, not asserted: "you can name **one command** ... that you have **already run at least once** (show the invocation and its output, redacted)", and it must be red-capable, deterministic, fast, and runnable unattended.

Phase 3 forbids single-hypothesis anchoring: "Generate **3–5 ranked hypotheses** before testing any of them. Single-hypothesis generation anchors on the first plausible idea." Each must be falsifiable, in the form "If \<X\> is the cause, then \<changing Y\> will make the bug disappear." And: "If you cannot state the prediction, the hypothesis is a vibe: discard or sharpen it."

Phase 6 has a literal completion checklist, including "All `[DEBUG-...]` instrumentation removed" and "The hypothesis that turned out correct is stated in the commit / PR message, so the next debugger learns."

**The analogue.** This is **gated troubleshooting with a mandatory verification step first**, closed by a **structured retrospective**: you establish a repeatable way to observe the fault before you theorize about it, you generate competing explanations rather than committing to the first one, you change one variable at a time, and you close by recording which explanation was correct so the next person does not repeat the diagnosis.

**Do not weaken it by:** treating Phase 1 as optional when the fault "looks obvious." The skill's own instruction is "Skip phases only when explicitly justified," and the phase most often skipped is the one that carries all the value.

### 2.7 Two-axis review: standards separated from specification

**The mechanism.** `skills/engineering/code-review/SKILL.md` runs two reviews of the same change, in parallel sub-agents, and refuses to merge their findings:

> - **Standards**: does the code conform to this repo's documented coding standards?
> - **Spec**: does the code faithfully implement the originating issue / spec?

The justification is the sharpest paragraph in the repository:

> A change can pass one axis and fail the other:
> - Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
> - Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**
> Reporting them separately stops one axis from masking the other.

The aggregation rule protects the separation: "Do **not** merge or rerank findings ... Don't pick a single winner across axes: that's the reranking the separation exists to prevent."

The Standards axis carries a fixed baseline of twelve Fowler code smells even when a project documents nothing, bound by two rules: "**The repo overrides**" and "**Always a judgement call.**"

**The analogue.** This is **separating conformance review from acceptance review** and refusing to let one stand in for the other. In practice these are usually run by different people for a reason: a solution can be built exactly to standard and still not be what the requester asked for, and it can deliver exactly what was asked for while violating every tenant convention. Running them together lets a reviewer who is satisfied on one axis stop looking at the other.

**Do not weaken it by:** running one review that "covers both." The parallelism is not a performance optimization; the skill says it exists "so they don't pollute each other's context."

### 2.8 Deep modules behind small interfaces

**The mechanism.** `skills/engineering/codebase-design/SKILL.md` supplies a precise vocabulary and insists on it: "Use these terms exactly: don't substitute 'component,' 'service,' 'API,' or 'boundary.' Consistent language is the whole point."

The definitions that carry across cleanly:

- **Interface**: "everything a caller must know to use the module correctly: the type signature, but also invariants, ordering constraints, error modes, required configuration, and performance characteristics."
- **Depth**: "leverage at the interface. The amount of behaviour a caller (or test) can exercise per unit of interface they have to learn."
- **Seam**: "a place where you can alter behaviour without editing in that place."

Four principles, each independently useful:

- "**The deletion test.** Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep."
- "**The interface is the test surface.** Callers and tests cross the same seam. If you want to test *past* the interface, the module is probably the wrong shape."
- "**One adapter means a hypothetical seam. Two adapters means a real one.** Don't introduce a seam unless something actually varies across it."
- "Depth is a property of the interface, not the implementation."

**The analogue.** This is standard **capability packaging**: a reusable component is worth building when it hides real complexity behind a contract small enough that a consumer can learn it in a minute, and it is not worth building when the contract is nearly as complicated as the thing it wraps. The deletion test is the honest version of the build-versus-reuse conversation.

### 2.9 Progressive disclosure and the two loads

**The mechanism.** `skills/productivity/writing-for-agents/SKILL.md` is the repository's own documentation standard, and it is directly applicable to any documentation system. Its central budget model:

> - **Context load** is the cost of always-loaded material on the agent's window ... spending tokens and attention whether or not it fires.
> - **Cognitive load** is the cost on the human: which documents exist and when to reach for each. The human is the index. Not a cost to minimise: it is the price of human agency; spend it where human judgement matters, remove it where it does not.

It defines an **information hierarchy** of in-file steps, in-file reference, and disclosed reference behind a pointer, with a clean test: "inline what every branch needs, and push behind a pointer what only some branches reach."

Two more levers worth carrying: **completion criteria** ("can the agent tell done from not-done? A vague bound ... invites **premature completion**"), and the warning against steering by prohibition: "**Negation** is the failure mode ... steering by prohibition drags the forbidden behaviour into context and makes it *more* available, not less ... Prompt the **positive**."

**The analogue.** This is documentation design for procedures that get executed rather than read: put the ordered actions at the top, push reference material one level down behind a clear pointer, end every step on a condition someone can objectively check, and write instructions as what to do rather than what not to do. That last point is well established in instructional practice and it is the one most often violated in enterprise runbooks.

---

## 3. Per-skill breakdown

Every skill in the repository is covered. The 25 promoted skills (`engineering/` and `productivity/`) get full treatment. The 12 non-promoted skills (`misc/` and `in-progress/`) are covered more briefly in section 3.26, with justification for each.

### Engineering, user-invoked

---

### 3.1 `ask-matt`

**What it does and the mechanism.** A router over the user-reachable skills, existing because "You don't remember every skill, so ask." It maps a main flow (idea to shipped change), two on-ramps, a codebase-health branch, and a set of standalone skills. `SKILL-MECHANICS.md` explains why routers exist at all: user-invoked skills carry no model-facing description, so "that piled-up cognitive load is cured by a **router skill**: one user-invoked skill that names the others."

The mechanism is cognitive-load management, plus one genuinely valuable sub-document: `PHASE-BOUNDARIES.md`, an ordered decision tree for what to do with your working context at the boundary between two phases of work (continue, clear, hand off, delegate to a sub-agent, or compact). Its ordering rule is "Work top to bottom at the boundary. The first **yes** wins," and its first question is deliberately the cheapest: "Continue costs nothing and loses nothing, so rule it out before anything else."

**Verdict: translate surface (low effort, ongoing).** The router's content is a map of Matt's skills, so it goes stale the moment you add your own. `CLAUDE.md` states the maintenance rule: "a new skill it never mentions, or a stale one it still routes to, is a router that lies."

**Solution Engineering translation.** Keep the file, rename it in your own installation, and edit the map as you add skills. Two edits matter immediately: the main flow's step 2 detour ("If a question needs a runnable answer") should name the Microsoft 365 cases (an approval state model, an adaptive card layout, an agent's grounding behavior), and the on-ramps should name your actual intake surfaces rather than GitHub issues.

`PHASE-BOUNDARIES.md` needs no translation at all. Its distinction between primary and secondary sources ("Every move except **Continue** turns a **primary source** into a **secondary source**") applies unchanged to any long working session.

**Operational framing.** A router is an index to a body of procedure, and it is only as useful as it is current. Treat it the way you would treat any procedure index: whoever adds a procedure updates the index in the same change, or the index becomes actively misleading.

---

### 3.2 `grill-with-docs`

**What it does and the mechanism.** Seven lines total, and the whole body is: "Call the Skill tool twice, for 'grilling' and 'domain-modeling'." It runs the interview and the vocabulary work simultaneously, so the glossary and the decision records are produced as a byproduct of a conversation you were going to have.

The mechanism is section 2.1 plus section 2.2, fused. `ask-matt` explains why it is the default over `grill-me`: "it's stateful, retaining what it learns in `CONTEXT.md` and ADRs ... which makes it the better of the two whenever a repo is there to leave it in."

**Verdict: use as-is.** No changes. The skill contains no TypeScript, no npm, and no GitHub surface. It is two skill invocations.

**Solution Engineering translation.** The skill needs none; what needs describing is what a session looks like when the deliverable is a Power Automate flow rather than a web feature. A real session on "automate the equipment request process" would work a frontier something like this:

*Round 1 (nothing upstream is settled, so these are all askable now):*
- Where does a request originate today, and does that surface change? (Recommended: a SharePoint list form, because it gives you a durable item ID to key everything else to.)
- Who is the approver, and is that a fixed person, a role, a manager lookup, or data on the request? (Recommended: a manager lookup via Graph, because it survives staff changes.)
- What is the system of record for the approved request after approval? (Recommended: the same list, with a status column, because a second store creates a reconciliation problem.)
- What must happen if the approver never responds? (Recommended: escalation after five business days, because an approval with no timeout is an approval that silently stalls.)

*Round 2 (unlocked only by round 1's answers, and genuinely not askable before them):*
- If the manager lookup is the approver source, what happens when the requester has no manager set in Entra?
- If status lives on the list item, who is permitted to edit it directly, and does that need to be locked down?
- Does escalation go to the manager's manager, or to a fixed group?

The dependency ordering is the point. You cannot sensibly ask about the escalation target before you have settled where approvers come from, and the frontier rule is what stops the interview from asking anyway and getting an answer that is quietly invalidated ten minutes later.

The vocabulary work runs alongside. The moment the stakeholder says "requester" in one sentence and "submitter" in the next, that is a `CONTEXT.md` entry with an `_Avoid_` line, and it will save you from a SharePoint column named `Submitter` feeding a flow variable named `requesterEmail` feeding an agent instruction that says "the person who raised the request."

**Operational framing.** This is the alignment readback, run before any build effort is committed, with the added property that it leaves a written record of the agreed terms. In work where the requirement comes from someone outside your discipline, the readback is where nearly all recoverable misunderstanding is caught, and it costs a fraction of catching it after delivery.

---

### 3.3 `triage`

**What it does and the mechanism.** Moves incoming work through a small state machine: two category roles (`bug`, `enhancement`) and five state roles (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). "Every triaged issue should carry exactly one category role and one state role. If state roles conflict, flag it and ask the maintainer before doing anything else."

Three mechanisms sit underneath, and each is independently valuable:

- **Verification before specification.** "**Verify the claim.** Before any grilling, check that the claim holds up. For a bug, reproduce it from the reporter's steps ... Report what happened: confirmed (with code path), failed, or insufficient detail (a strong `needs-info` signal). A confirmed verification makes a much stronger agent brief."
- **A durable written brief as the contract.** `AGENT-BRIEF.md`: "The original body and discussion are context: the agent brief is the contract." Its principles are durability over precision ("**Don't** reference file paths: they go stale"), behavioral rather than procedural description, complete acceptance criteria, and explicit scope boundaries.
- **An institutional memory of rejections.** `OUT-OF-SCOPE.md` keeps one file per rejected *concept*, not per request, so that "when a new issue comes in that matches a prior rejection, the skill can surface the previous decision instead of re-litigating it." Critically, it excludes already-built features from that store, because "recording it would poison the dedup checks with false rejections."

**Verdict: translate surface.** Hard dependency on an issue tracker (ADR 0001 classifies it as such: "Without the mapping, output is wrong, not just fuzzy"). The label vocabulary also needs adjusting for a business audience. The state machine itself is unchanged.

**Solution Engineering translation.**

*Intake.* Your requests arrive as Teams messages, emails, and hallway conversations rather than as issues. Triage cannot work on an unbounded intake surface, so the first translation is a single intake point that everything is copied into. Section 5 covers the tracker choice.

*Labels.* Two changes, both surface:
- `wontfix` becomes `not-planned`. `wontfix` reads badly to a business stakeholder who filed the request in good faith, and this label is visible to them.
- `needs-info` becomes `awaiting-requester`, which states who is blocking rather than what is missing.

Keep `needs-triage`, `ready-for-agent`, and `ready-for-human` unchanged. `ready-for-human` earns its place here more than in a code repository: it is the correct state for anything requiring admin consent, a license purchase, a tenant-level setting, or a data loss prevention policy change.

Resist adding `needs-security-review` and `needs-license-review` as *state* roles. They are real and you will want them, but adding them as states breaks the "exactly one state role" invariant that makes conflict detection possible. Add them as free-standing labels outside the state machine and say so in your labels file.

*Verification.* This is the step that most transfers. "Reproduce it from the reporter's steps" in Microsoft 365 means: open the flow's run history and find the failed run the requester is describing, or run the same Graph call under the same account, or send the same prompt to the agent. Three outcomes, exactly as the skill says: confirmed with the specific failing step or response; not reproducible, which is itself a finding worth recording; or insufficient detail, which is a strong `awaiting-requester` signal. "Insufficient detail" is the majority case for verbally reported Microsoft 365 problems, and having a named state for it is worth the whole setup.

*The brief.* The durability rule translates precisely, and gains force. "Don't reference file paths: they go stale" becomes: do not reference a specific flow action name, a step index, or a list view. Those change constantly and are not stable identifiers. Describe the interface instead: the list schema fields involved, the trigger condition, the required output shape, the permission context the operation must run under.

A worked example, in the skill's own template:

> **Category:** defect
> **Summary:** Equipment requests submitted after 17:00 UK time are assigned the following day's due date
>
> **Current behavior:** The due date is calculated from `utcNow()` and formatted without a timezone conversion, so submissions after 17:00 local time cross the UTC date boundary and shift the calculated due date forward by one day.
>
> **Desired behavior:** Due dates are calculated in the requester's local time zone. A request submitted at any hour on a given local date receives a due date computed from that local date.
>
> **Key interfaces:** The list item's `DueDate` field, which stays a date-only value; the flow's date calculation, which must apply an explicit timezone conversion before formatting; no change to the trigger condition or to the approval step.
>
> **Acceptance criteria:**
> - [ ] A request submitted at 23:30 local time receives a due date computed from that day's local date
> - [ ] A request submitted at 09:00 local time is unchanged from current behavior
> - [ ] Both cases are covered by the flow test harness with fixed submission timestamps
>
> **Out of scope:** Time zones other than the requester's own; historical correction of already-submitted requests.

Note what is absent: no action names, no step numbers, no screenshots. It survives the flow being restructured.

*The rejection store.* `.out-of-scope/` transfers with no change and is unusually valuable in this space, because the same requests recur with different wording every few months. "Can we get a Power BI report on this list", "can this feed a dashboard", "can we visualize the request volumes" are one concept and belong in one file. The rule about not recording already-built features matters too: your equivalent of "it already exists" is usually "there is already a flow that does this, here it is," and that goes in the closing note, not the rejection store.

**Operational framing.** This is intake control with a documented state for every request and a written handover specification before any build begins. The rejection store is the part most often missing in practice, and it is what stops a settled scoping decision from being reopened every time someone new asks.

---

### 3.4 `improve-codebase-architecture`

**What it does and the mechanism.** Surveys a codebase for "deepening opportunities: refactors that turn shallow modules into deep ones," presents them as a self-contained HTML report with before-and-after diagrams and a recommendation strength badge, then runs a grilling session on whichever candidate you pick.

Three mechanisms:
- **Scope before scanning.** "**Scope before you scan: YAGNI.** Deepening a module pays off by making future changes to it easier, so put extra weight on the parts of the codebase that have recently changed."
- **The deletion test as the filter.** "would deleting it concentrate complexity, or just move it? A 'yes, concentrates' is the signal you want."
- **Survey, then decide.** "Do NOT propose interfaces yet. After the file is written, ask the user: 'Which of these would you like to explore?'" The survey and the design session are separate acts.

The README is honest about its limits: "It is a survey, not a rescue: on a genuinely old codebase it will find real candidates, but it won't untangle the mud for you."

**Verdict: translate surface (medium priority, Stage 3).** Two surfaces need work: the hot-spot signal, and the artifact being surveyed.

**Solution Engineering translation.**

*The hot-spot signal.* The skill infers hot spots from `git log --oneline`. If your solutions are not in source control, that signal does not exist. The honest substitute is platform telemetry: flow run volume and failure rate from the Power Platform admin center, and the list of flows that have been edited most recently. That is a weaker signal than commit history, because it tells you what runs often rather than what changes often, and change frequency is the property that predicts refactoring payoff. Note the weakness rather than pretending the substitute is equivalent; and if you adopt the repository pattern in section 5, the real signal comes back.

*What gets surveyed.* The candidates in a Microsoft 365 estate are concrete and recognizable:
- The same sequence of five actions copied into eight flows, which is duplication with no single point of change.
- A child flow that receives a payload and immediately calls another child flow with the same payload, which is the "middle man" smell and fails the deletion test.
- A single flow with forty actions that both processes approvals and generates a weekly report, which is a module changed for two unrelated reasons.
- A site column set defined independently in six site collections rather than once at the hub, which is the same logical change requiring six edits.
- A PowerShell tooling repository where every script builds its own Graph authentication rather than calling one shared function.

Apply the deletion test to each: delete the child flow and does complexity concentrate somewhere useful, or does it just reappear in each of the callers?

*The report.* The HTML report with diagrams is worth keeping exactly as specified, and is arguably more valuable in your context than in Matt's. A before-and-after diagram of a flow estate is a genuinely good artifact to put in front of a stakeholder who controls the budget for the consolidation work.

**Operational framing.** This is a periodic condition survey of a deployed estate that produces a prioritized list of candidates rather than a work order. Keeping the survey separate from the decision is what stops it becoming a backlog of unreviewed remediation items.

---

### 3.5 `setup-matt-pocock-skills`

**What it does and the mechanism.** Scaffolds the per-repository configuration the other engineering skills assume: issue tracker, triage labels, and domain document layout. It writes `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, and `docs/agents/domain.md`, plus an `## Agent skills` block in `CLAUDE.md` or `AGENTS.md`.

The mechanism is explicit configuration for the things skills cannot infer. ADR 0001 explains why only some skills reference it: hard-dependency skills (`to-tickets`, `to-spec`, `triage`) "have to publish to a specific issue tracker or apply a specific label string," while soft-dependency skills "only use it to sharpen output ... and degrade gracefully without it." The design note is worth carrying: "The split keeps soft-dependency skills token-light and avoids cargo-culting the setup pointer into places where it isn't load-bearing."

Two other design properties are worth noting because you will reuse them: it is "a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write," and it leads each question with a recommended answer "so the user can accept it in a word."

**Verdict: translate surface.** The issue tracker section needs a fourth option that fits your environment and the label section needs your vocabulary. Section 5 of this report is the full run plan.

**Operational framing.** This is the configuration step that turns a generic procedure set into one that fits a specific environment. Running it once and writing the answers down is what stops every subsequent session from re-deciding where things live.

---

### 3.6 `to-spec`

**What it does and the mechanism.** Turns an already-completed conversation into a specification and publishes it. Its first instruction is a deliberate constraint: "Do NOT interview the user; just synthesize what you already know."

The mechanisms:
- **Separation of interview from synthesis.** Grilling is a different skill and has already run. This one only writes down what was agreed. Merging the two produces a specification that quietly invents the parts nobody discussed.
- **A seam confirmation gate before the specification is written.** "Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible ... The fewer seams across the codebase, the better - the ideal number is one. Check with the user that these seams match their expectations."
- **A template with a durability rule.** "Do NOT include specific file paths or code snippets. They may end up being outdated very quickly."

The template sections are Problem Statement, Solution, User Stories ("A LONG, numbered list ... extremely extensive"), Implementation Decisions, Testing Decisions, Out of Scope, Further Notes.

**Verdict: translate surface.** The template survives almost intact. Two sections need Microsoft 365 content: Implementation Decisions and Testing Decisions.

**Solution Engineering translation.** Take the template as written and populate the two technical sections with the decisions the platform actually forces:

*Implementation Decisions* for a Power Automate and SharePoint deliverable covers: the list and library schema, including which columns are indexed and whether any view will exceed the list view threshold; whether state lives in one list with a status column or in multiple lists; the trigger type and its condition; whether the flow is solution-aware and which connection references it uses; the identity every connection runs under and why; error handling structure (configure-run-after, scopes, a failure notification path); premium connector usage and its licensing implication; and the data loss prevention classification of every connector involved.

*Testing Decisions* is where the seam confirmation lands. The seams in this space are real and nameable:
- The HTTP request trigger of a child flow, with a JSON schema. This is the highest-value seam available in Power Automate and it behaves like a genuine interface: it has a declared shape, it rejects malformed input, and it can be invoked directly with a fixture payload.
- A PowerShell module's exported functions, which is a full-strength seam with a full-strength test framework behind it.
- A custom connector operation.
- An agent's declared tool or action surface.
- A SharePoint list schema, assertable against a committed template with PnP PowerShell.

The skill's "the ideal number is one" preference translates directly and usefully: if a specification proposes testing at four different seams, that is a signal the solution is being built as four shallow pieces rather than one deep one.

*User Stories* need no translation and are worth writing at the length the template demands. The actor list in this space is genuinely wide (requester, approver, delegated approver, process owner, site owner, tenant administrator, auditor) and the exhaustive list is what surfaces the actor nobody thought about.

**Operational framing.** This is the written execution plan, produced from the confirmed alignment readback rather than in place of it. The separation matters: a plan written during the interview will contain invented content, because it is being drafted before the interview has finished settling.

---

### 3.7 `to-tickets`

**What it does and the mechanism.** Breaks a plan, specification, or conversation into tracer-bullet slices with declared blocking edges. Fully described in section 2.4. Two additional pieces:

- **A user confirmation round before publishing.** "Does the granularity feel right? (too coarse / too fine) Are the blocking edges correct: does each ticket only depend on tickets that genuinely gate it? Should any tickets be merged or split further? Iterate until the user approves the breakdown."
- **A prefactoring instruction.** "Look for opportunities to prefactor the code to make the implementation easier. 'Make the change easy, then make the easy change.'"

**Verdict: translate surface.** Hard dependency on the tracker. The slicing rules themselves need no change.

**Solution Engineering translation.** The key question is what a vertical slice is when there is no schema, API, and UI stack. The answer: a slice is complete when it produces an observable outcome for a real actor, end to end, through every layer the final solution will use.

For the equipment request example, a correct first slice is: *a request submitted through the SharePoint form triggers a flow that writes an approval decision back to the item, for one hardcoded approver, with no escalation, no notification formatting, and no reporting.* That slice touches the list schema, the trigger, the connection, the approval action, and the write-back. It is demonstrable to the requester. It proves every integration point.

The incorrect but tempting alternative is: *build the complete list schema with all 22 columns and all views.* That is one layer, it is not demonstrable, and it defers every genuine risk (does the approval connector behave as expected under the service account, does the write-back trip the trigger recursively, does the requester have permission to see the item after submission) to later.

Blocking edges are typically real and easy to identify here: the list schema blocks the flow that reads it, the connection reference blocks anything using that connector, and the agent's knowledge source blocks the agent's grounding tests.

The expand, migrate, contract sequence has a direct and important analogue. Renaming a SharePoint column that eight flows read is exactly the wide refactor case: a single edit breaks every consumer at once. The correct sequence is the one in the skill: add the new column alongside the old and populate both (expand), migrate consumers in batches with each batch its own ticket (migrate), remove the old column once no consumer references it (contract). This is worth writing down as a standing pattern, because the platform's rename behavior makes the naive approach genuinely destructive.

**Operational framing.** This is decomposing a build into small proving runs with declared dependencies, so that each increment is independently demonstrable and the sequence of work is driven by what is actually unblocked rather than by which parts feel easiest to start.

---

### 3.8 `implement`

**What it does and the mechanism.** Fifteen lines. It is an orchestration wrapper: implement the work, "Use /tdd where possible, at pre-agreed seams," run typechecking and tests at stated intervals, "Once done, use /code-review to review the work," and commit.

The mechanism is that it closes the loop before the work is declared done. Review is not a separate later step someone might skip; it is inside the build procedure.

**Verdict: translate surface (thin skill, thin translation).** The three check commands are the surface. Replace them with your environment's equivalents.

**Solution Engineering translation.** Rewrite the middle three lines as: run the Power Platform solution checker and flow checker regularly; run the test harness for the child flow currently under change regularly; run the full harness and any PnP schema assertions once at the end. Then `/code-review`, then commit the unpacked solution.

Note honestly that "Run typechecking regularly" has no full-strength equivalent, which is the subject of section 4. The closest thing is the flow checker plus a JSON schema on every child-flow trigger, and it catches materially less.

**Operational framing.** Review is inside the procedure rather than after it. That is the difference between a check that happens and a check that happens when there is time.

---

### 3.9 `wayfinder`

**What it does and the mechanism.** For work "too big for one agent session." It charts a map of **decision tickets** on the issue tracker and resolves them one at a time. The defining constraint: "Wayfinder is **planning** by default: each ticket resolves a decision, and the map is done when the way is clear, with nothing left to decide before someone goes and does the thing. The pull to just do the work is usually the signal you've reached the edge of the map and it's time to hand off."

Mechanisms worth naming:
- **The map is an index, not a store.** "a decision lives in exactly one place, its ticket, so the map never restates it, only gists it and links."
- **Deliberate incompleteness with a sharpness test.** The `## Not yet specified` section holds work you can see coming but cannot yet phrase precisely. The test is "whether you can state the question precisely now, *not* whether you can answer it now." Ticket it when the question is sharp even if you cannot act on it; leave it unspecified when you cannot phrase it that sharply.
- **Scope separated from sharpness.** Out-of-scope work "never graduates," gets its own section, and closing a mis-scoped ticket is recorded as a scoping act rather than as a decision on the route.
- **One ticket per session.** "**never resolve more than one ticket per session**, with the exception of research tickets."
- **Explicit human-in-the-loop typing.** Every ticket is either worked with a person present or driven by the agent alone, and the human-present ones cannot be resolved by the agent answering its own questions.
- **Refer by name, not identifier.** "A wall of `#42, #43, #44` is illegible; names read at a glance."

**Verdict: translate surface (Stage 3, low frequency, high value when it fits).** `ask-matt` warns it is "the most cognitively demanding flow here ... save it for exactly that, never a well-scoped feature." That warning applies fully to you.

**Solution Engineering translation.** The genuine fits in your work are the multi-month efforts where the shape is not yet known: consolidating a departmental process estate onto a single information architecture, standing up a Copilot agent program with governance and evaluation, migrating a set of legacy workflows onto a supported pattern, or designing a tenant-wide taxonomy.

The ticket types translate cleanly:
- **Research** (agent-driven): "does the Graph API expose delegated access to this resource, and at what permission scope"; "what are the current documented limits on this connector."
- **Prototype** (person present): "what should the approval card look like"; "does this state model survive the delegated-approver case."
- **Grilling** (person present): the default, and most decision tickets are this.
- **Task**: the type that matters most in your environment. The skill defines it as "Manual work that must happen before a *decision* can be made ... Signing up for a service so its API can be judged, provisioning access, moving data so its shape can be seen." That is a constant in Microsoft 365 work: you cannot decide whether to use a premium connector until someone has provisioned a trial license so you can see what it actually returns. Naming this as a first-class ticket type, distinct from a decision, is a real improvement over treating it as a blocker to complain about.

The map lives wherever your tracker lives (section 5). The local markdown form specified in `issue-tracker-local.md` works fine if you do not have a tracker that supports parent and child relationships.

**Operational framing.** This is phased planning under genuine uncertainty: you chart only as far as you can see, you resolve one open question at a time, and you record what you deliberately are not doing separately from what you have not yet worked out. Keeping those two categories apart is what stops a scope boundary from being mistaken for an unresolved question six weeks later.

---

### Engineering, model-invoked

---

### 3.10 `prototype`

**What it does and the mechanism.** "A prototype is **throwaway code that answers a question**. The question decides the shape." Two branches: `LOGIC.md` for "Does this logic / state model feel right?" and `UI.md` for "What should this look like?" The branch choice matters because "The two branches produce very different artifacts, so getting this wrong wastes the whole prototype."

The rules that make it work:
- **Throwaway from day one, and marked as such.**
- **Trivial to run.** "A logic demo is a single HTML file the user double-clicks. Either way, no thinking required to start it."
- **No persistence by default.** "Persistence is the thing the prototype is *checking*, not something it should depend on."
- **Skip the polish.** "No tests, no error handling beyond what makes the prototype *runnable*, no abstractions."
- **Surface the state.** Render the full relevant state after every action.
- **Capture it when done.** Fold the validated decision into the real work, keep the prototype itself as a primary source on a throwaway branch, and record the verdict and the question it settled.

`LOGIC.md` adds the single most transferable instruction in the whole repository for your work: "Because it's one file with nothing to install, you can hand it to a non-developer (a designer, a PM, a domain expert) and let them feel the model for themselves. So it speaks their language, not the code's." And: "Every label is in **domain language**, not code: buttons and state read like the business, not the reducer."

Its interface constraint is what makes the output reusable: "Put the actual logic ... in a single `<script>` block written as a small, pure module that could be lifted out and dropped into the real codebase later. The page around it is throwaway; this module isn't."

**Verdict: use as-is for the logic branch; translate surface for the UI branch.** The logic branch is an exceptionally strong fit for Solution Engineering and needs no adaptation whatsoever. The UI branch's `?variant=` routing and React switcher are web-application surface.

**Solution Engineering translation.**

*Logic branch, unchanged and highly recommended.* An approval process is a state machine, and stakeholders consistently agree to state machines on paper that they reject the moment they can click through them. A single HTML file with buttons labeled "Submit request", "Approve", "Reject", "Delegate", "Recall", and "Escalate", showing the full request state after each click, with guided walkthrough tabs for the awkward cases (approver delegates then the delegate rejects; requester recalls after approval but before fulfilment; approver leaves the organization mid-request) is the cheapest way to find out that the process everyone agreed to has an unhandled state. The instruction to choose scenarios that demonstrate "the happy path, a tricky edge case, an attempt at something that should be illegal" is exactly right for approval design.

The purity constraint pays off concretely: the validated state transition table lifts directly into the flow's condition logic and into the SharePoint choice column's allowed values.

*UI branch, translated.* Three genuine cases in your work:
- **Adaptive cards.** Three structurally different versions of an approval card, rendered side by side in a single HTML file using the adaptive card renderer, or three card payloads posted to a test Teams channel. The skill's "Variants must be **structurally different**: different layout, different information hierarchy, different primary affordance, not just different colours" applies directly, and the anti-pattern it warns about ("Three slightly-tweaked card grids isn't a UI prototype, it's wallpaper") is precisely what usually happens with card design.
- **SharePoint page and view layouts.** Build the variants on a page in a development site and switch between them, which is the closest available analogue to the `?variant=` pattern.
- **Power Apps screens.** Canvas app screens with a variant selector, which maps to the pattern almost exactly.

The sub-shape preference transfers with full force: "A UI prototype is much easier to judge when it's **butting up against the rest of the app**: real header, real sidebar, real data, real density. A throwaway route on its own is a vacuum: every variant looks fine in isolation." An adaptive card judged in the designer looks fine. The same card in a Teams channel among fourteen other messages often does not.

*What a tracer bullet for an agent build looks like.* This is worth stating explicitly because it is the least obvious case. A tracer bullet for a Copilot agent is: one question, one grounding source, one grounded answer with a citation, delivered to one test user, with the answer checked against a known-correct response. Not the full instruction set, not all six knowledge sources, not the tool integrations. That single path proves the grounding actually retrieves from the source you think it does, that the citation renders, that the permission trimming behaves as expected for a user who should not see everything, and that the publishing and audience assignment work. Every one of those is a real risk and every one of them is invisible until an end-to-end path runs.

**Operational framing.** This is a low-cost walkthrough with the process owner present, run before the build is committed, using a disposable artifact that is deliberately cheap enough to discard. Its purpose is to surface the objection that would otherwise arrive at handover, when changing the design costs a rebuild rather than a conversation.

---

### 3.11 `diagnosing-bugs`

**What it does and the mechanism.** Fully described in section 2.6. The `Redact` section is worth noting separately as a genuine requirement in your environment: "**Redact every secret first**: write `<REDACTED>` in its place. Build loops against env vars, so the credential stays in the environment rather than in what you show. Captured artifacts carry auth headers: quote only the lines that carry the signal."

**Verdict: translate surface.** The phases, gates, and completion criteria are unchanged. Only the ranked list of ten ways to build a feedback loop is TypeScript-and-web-shaped and needs replacing.

**Solution Engineering translation.**

*The ranked list, rewritten for Microsoft 365, in roughly descending order of tightness:*

1. **A test harness invocation against a child flow.** Post a captured failing payload to the child flow's HTTP request trigger and assert on the output. Deterministic, fast, unattended, and genuinely red-capable.
2. **A Pester test against the PowerShell or Graph wrapper.** Full-strength, no compromise.
3. **A direct Graph call with a captured request.** `Invoke-MgGraphRequest` or Graph Explorer with the exact resource, query, and permission context from the failure. This isolates whether the fault is in the call or in the flow around it, which is the single most common ambiguity in this space.
4. **A resubmitted flow run.** Power Automate lets you resubmit a specific historical run with its original trigger payload. This is the closest thing to a replay harness the platform gives you, and it is the workhorse. Its weakness is that it reruns the current flow definition against old input, so it confirms the fix but does not isolate the failing step.
5. **A PnP PowerShell schema or state assertion.** For information architecture faults: read the actual list schema, view definition, or permission set and compare it to the committed template.
6. **A fixed prompt set against an agent.** For Copilot agent faults: a stored set of prompts with expected retrieval targets, run through the agent's test interface. Weakest of these, and section 4 addresses why.
7. **A differential run.** The same input through the development environment and the production environment, or under a service account and under a personal account, diffing the outputs. This is the fastest way to isolate a permission-context fault, which is a large fraction of Microsoft 365 defects.
8. **A repeat loop for throttling and timing faults.** The skill's non-determinism guidance applies without modification: "The goal is not a clean repro but a **higher reproduction rate** ... A 50%-flake bug is debuggable; 1% is not, so keep raising the rate until it's debuggable." Running the same operation 100 times to establish whether a 429 response is systematic or incidental is exactly the right move.
9. **A guided manual loop.** The skill's last resort, with a template script that drives the human through the steps and captures the output. In your environment the human step is often unavoidable (a person must click an approval in Teams), so this is reached more often than it would be in a code repository. Keep it structured rather than ad hoc.

*What "a failing test for a flow" actually is.* Concretely: a child flow with an HTTP request trigger and a declared JSON schema; a parent harness flow, or a stored HTTP request, that posts a fixture payload; and an assertion built from a Condition action whose false branch runs a Terminate action with status `Failed`. That produces a genuinely binary red or green result in the run history, and it is invocable by an agent without a browser. That is the closest full-strength substitute available, and section 4 covers where it is still weaker than a real test.

*Where the platform is harder than a codebase.* Three sources of non-determinism have no equivalent in Matt's setting and should be named in your version of the skill: connector throttling under a shared capacity, search and directory index lag (a permission or property change is genuinely not visible for a period), and permission-context divergence (the same call succeeding under your account and failing under the flow's service account). All three produce the appearance of intermittency. The skill's discipline handles them correctly if you follow it: raise the reproduction rate, assert on the specific symptom rather than on "it worked", and change one variable at a time.

**Operational framing.** This is gated troubleshooting: establish a repeatable observation of the fault before forming a theory about it, generate competing explanations rather than committing to the first, and close with a written statement of which explanation was correct. The final phase's requirement to record the correct hypothesis is a structured lessons-learned step, and it is the reason the same fault does not consume two days twice.

---

### 3.12 `research`

**What it does and the mechanism.** Twelve lines. Spin up a background agent, investigate against "**primary sources** (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it," write findings to a single Markdown file with each claim cited, and save it where the repository already keeps such notes.

The mechanisms: primary sources only, one cited file as the output, and background execution so you keep working.

**Verdict: use as-is.** No changes. It is source-discipline plus a delegation pattern, with no technology surface at all.

**Solution Engineering translation.** None needed, but the value is worth stating: this is disproportionately useful in Microsoft 365 because the platform changes faster than any model's training data. The primary sources are Microsoft Learn, the Graph API reference and its changelog, the connector reference documentation, the Message Center, and the Microsoft 365 roadmap. Any answer about a current permission scope, a connector limit, a throttling threshold, or licensing has a meaningful chance of being wrong from memory, and this skill is the standing corrective.

Pair it with the `teach` skill's blunter version of the same rule: "Never trust your parametric knowledge."

**Operational framing.** This is source discipline: findings are traceable to the authority that owns them, and the citation is what makes the finding reusable six months later when someone asks whether it is still true.

---

### 3.13 `tdd`

**What it does and the mechanism.** Fully described in section 2.5, with `tests.md` and `mocking.md` as supporting reference. `mocking.md` adds a rule that transfers directly: mock at system boundaries only, and "Don't mock: Your own classes/modules, Internal collaborators, Anything you control."

**Verdict: translate surface, and be honest about the gap.** This is the skill where the surface and the mechanism are hardest to separate, because the mechanism assumes a test runner exists. The mechanism itself (red before green, one slice at a time, pre-agreed seams, expected values from an independent source) is intact and transferable. What varies is how strong a substitute you can build, and it varies by artifact type.

**Solution Engineering translation, by artifact:**

- **PowerShell and Graph tooling.** No translation needed and no weakening. Pester gives you a full red-green loop with mocking at boundaries. Apply the skill verbatim, including the anti-patterns.
- **Child flows with an HTTP request trigger.** A strong substitute, as described in 3.11. The seam is the trigger's JSON schema, and the skill's "The interface is the test surface" holds literally: the schema is the interface and the harness crosses it. Red before green works: write the harness case, watch it fail against the current flow, change the flow, watch it pass.
- **SharePoint information architecture.** A schema assertion script comparing live state to a committed PnP template is deterministic and genuinely red-capable. Weaker than a test only in that it asserts on structure rather than behavior.
- **Copilot agents.** The weakest case, addressed in section 4.
- **Canvas apps.** Test Studio exists and provides a real recorded-assertion loop. Weaker than a code test suite in maintainability, but it is a real loop.

The anti-patterns translate with almost no change and are worth restating in your own words because they are easy to fall into:
- **Implementation-coupled** becomes: a harness that asserts on which actions ran, or on an intermediate variable's value, rather than on the flow's output. It breaks whenever the flow is restructured and tells you nothing about whether the behavior is correct.
- **Tautological** becomes: computing the expected due date in the harness with the same expression the flow uses. It cannot ever disagree with the flow. The expected value must be an independent literal, so the fixture says "submitted 2026-03-04T23:30 local, expect due date 2026-03-11" as a fixed pair.
- **Horizontal slicing** becomes: building every harness case for the whole solution before building any of it.

The seam confirmation gate is the highest-value single instruction to carry, because harness effort in this space is expensive. "You can't test everything, so agreeing the seams up front is how testing effort lands on the critical paths and complex logic instead of every edge case" is more true here than in a TypeScript project, not less.

**Operational framing.** This is gated progression against objective pass criteria defined before the work starts. The "red before green" rule is the part that cannot be compromised: a check that has never been observed to fail has not been shown to be capable of failing, and in a low-feedback environment that is the most common way a validation regime becomes ceremonial.

---

### 3.14 `domain-modeling`

**What it does and the mechanism.** Fully described in section 2.2. The invocation boundary is worth noting because it affects when the skill fires: `.agents/invocation.md` says "Merely *reading* `CONTEXT.md` for vocabulary is a one-line prose pointer, not the `domain-modeling` skill. Only the active build/sharpen discipline ... is `domain-modeling`."

The lazy-creation rule keeps it from becoming a setup chore: "Create files lazily: only when you have something to write. If no `CONTEXT.md` exists, create one when the first term is resolved."

**Verdict: use as-is.** No technology surface. It is a glossary discipline and a decision-record gate.

**Solution Engineering translation.** None needed for the skill. What is worth writing down is what your `CONTEXT.md` should contain, because the platform supplies a large amount of pre-existing ambiguity before your business domain adds any.

Terms that need resolving in almost any Microsoft 365 context, with the `_Avoid_` discipline applied:

> **Request**: A single submitted item of work tracked through the approval process, from submission to closure.
> *Avoid*: ticket, case, submission, item
>
> **Requester**: The person who submitted a Request and to whom its outcome is reported.
> *Avoid*: submitter, originator, end user, customer
>
> **Approver**: The person whose decision determines whether a Request proceeds. Distinct from a Process owner, who sets the rules but does not decide individual Requests.
> *Avoid*: manager, authorizer, reviewer
>
> **Agent**: A published Microsoft 365 Copilot agent with a defined instruction set, grounding sources, and audience.
> *Avoid*: bot, assistant, chatbot, copilot (lowercase, as a generic noun)

The general rule from `CONTEXT-FORMAT.md` applies and prunes hard: "Only include terms specific to this project's context. General programming concepts ... don't belong." So "SharePoint list" does not belong. It is platform vocabulary with a single agreed meaning, and putting it in the glossary just makes the glossary long enough to stop being read.

*What belongs in your decision records.* The three-part gate is easy to apply here because the platform forces a set of genuinely hard-to-reverse choices:
- One list with a status column, or separate lists per state. Reversing this after six months of data is a migration.
- SharePoint list or Dataverse as the store. Carries licensing, capability, and cost consequences.
- Application permissions or delegated permissions on the Graph integration, and which scopes. Reversing requires a new consent cycle.
- Flows owned by a service account with connection references, or by an individual. This is the decision that most often surfaces as an incident when someone leaves.
- The environment strategy: which environments exist, what is deployed where, and what is permitted to be built directly in production.
- Naming and site architecture conventions, including the hub structure.
- Which parts of the process are deliberately not automated, and why. The format file is right that "The explicit no-s are as valuable as the yes-s."

All seven pass all three gates: hard to reverse, surprising without context, and the result of a genuine trade-off. Contrast with "we used a Compose action here for readability", which passes none of them and should not be recorded.

**Operational framing.** This is a controlled vocabulary maintained as work proceeds rather than compiled afterwards, paired with a decision log gated tightly enough that people still read it. Recording terms at the moment they are resolved is what keeps the vocabulary honest; recording them later produces a glossary of what someone thinks was agreed.

---

### 3.15 `codebase-design`

**What it does and the mechanism.** Fully described in section 2.8. `DEEPENING.md` adds a dependency taxonomy that decides how a deepened module is tested: in-process, local-substitutable, remote but owned (ports and adapters), and true external (mock). Plus a testing rule: "replace, don't layer. Old unit tests on shallow modules become waste once tests at the deepened module's interface exist; delete them."

`DESIGN-IT-TWICE.md` adds a parallel exploration pattern: spawn three or more agents, each with a different design constraint ("Minimize the interface", "Maximise flexibility", "Optimise for the most common caller"), then compare on depth, locality, and seam placement, and give an opinionated recommendation rather than a menu.

**Verdict: translate surface.** The vocabulary and principles are technology-neutral. The TypeScript examples in the "Designing for testability" section are surface. The dependency taxonomy needs Microsoft 365 categories.

**Solution Engineering translation.**

*What a module is in your work:* a child flow, a custom connector, a PowerShell module, an Azure Function, an agent's declared tool, a site column set, a content type.

*What an interface is:* everything a consumer must know to use it correctly. For a child flow that is the trigger's JSON schema, plus the invariants the schema cannot express: whether it is idempotent, what it does on partial failure, what identity it runs under, what it returns on the not-found case, and what its expected latency is. The skill's insistence that an interface is more than a signature is exactly right here, because a flow's JSON schema expresses about a third of what a caller needs to know, and the rest has to be written down.

*Depth, concretely:* a child flow taking `{ requestId }` and handling lookup, permission resolution, approval routing, escalation timing, and audit logging is deep. A child flow taking fourteen parameters and performing one Graph call is shallow, and the deletion test says so: delete it and complexity does not concentrate, it just moves back to the single caller.

*The dependency taxonomy, translated:*
- **In-process** becomes: expression logic, data transformation, and decision rules with no connector call. Always testable directly.
- **Local-substitutable** becomes: a development environment with test data and separate connection references. This is the closest analogue and it is not local, which is a real weakening covered in section 4.
- **Remote but owned** becomes: your own child flows, Azure Functions, and custom connectors. The port-and-adapter pattern applies directly, and the adapter is the connection reference: the same flow definition points at a development connection in one environment and a production connection in another. That is genuinely two adapters at one seam, which by the skill's own rule ("One adapter means a hypothetical seam. Two adapters means a real one") makes it a real seam worth designing around.
- **True external** becomes: third-party connectors and external APIs. Mock in the harness by pointing the connection reference at a stub endpoint.

*"Accept dependencies, don't create them"* has a direct and important translation: pass the site URL, list name, and target identity into a child flow as parameters rather than hardcoding them inside it. That single practice is what makes a child flow testable in a development environment at all, and it is the most commonly violated design rule in Power Automate.

*Design it twice* transfers well and is cheap: ask for three structurally different designs for a child flow's parameter contract, one minimizing the parameter count, one maximizing reuse across callers, and one optimizing for the most common caller. The comparison usually settles the design in one pass.

**Operational framing.** This is capability packaging with an explicit contract: a reusable component is worth building when it hides enough complexity that a consumer can learn its contract in a minute, and the deletion test is the honest check on whether it does.

---

### 3.16 `code-review`

**What it does and the mechanism.** Fully described in section 2.7.

**Verdict: translate surface.** The two axes and the parallel execution are unchanged. Two surfaces need work: what the diff is, and what the standards baseline contains.

**Solution Engineering translation.**

*What is the diff when there is no traditional repository?* There are more real answers here than people assume, and this is the question that determines whether the skill is usable at all.

1. **Unpacked solutions.** `pac solution unpack` decomposes an exported Power Platform solution into a source tree of JSON and XML, including each flow's definition as JSON. Committed to git, this gives you a genuine, line-level diff of a flow. This is the strongest answer and it is the reason section 5 recommends the repository pattern.
2. **Site templates.** `Get-PnPSiteTemplate` produces an XML representation of a SharePoint site's structure: lists, columns, content types, views, and permissions. Committed and re-extracted, it diffs.
3. **Agent configuration.** An agent's instruction set, grounding source list, starter prompts, and declared actions can be exported or maintained as source and diffed.
4. **PowerShell.** Ordinary source control with a full-strength diff.
5. **When none of the above exists,** the honest substitute is a human-written change record: what changed, where, and why, written before the review. This is materially weaker than a diff because it depends on the author's completeness and cannot reveal an unintended change. Flag it as such rather than treating it as equivalent.

There is a real caveat with option 1 that should be recorded: unpacked flow definitions are machine-generated, so a small semantic change can appear as a large diff (reordered keys, regenerated identifiers, positional metadata). The compensating discipline is to commit a short human-written change summary alongside the export, and to review the summary against the diff rather than reading the diff cold.

*The Standards axis.* The skill says the Standards sub-agent should read "Anything in the repo that documents how code should be written." You will need to write that document, and it does not exist by default. A Solution Engineering standards baseline should cover at minimum: naming conventions for flows, lists, columns, and environment variables; connection references and service-account ownership rather than personal connections; environment variables rather than hardcoded site URLs and identifiers; a required error-handling pattern (a scope with configure-run-after and a failure notification path); indexed columns and delegation-safe query patterns; solution-awareness for anything intended to be deployed; data loss prevention classification compliance; and a rule on premium connector usage requiring explicit licensing sign-off.

*The Fowler smell baseline, translated.* This is worth doing properly because the smells map remarkably well onto flow and solution estates. The skill's two binding rules carry over unchanged ("The repo overrides" and "Always a judgement call"):

- **Mysterious Name**: `Condition 2`, `Apply to each 3`, `Compose 7`. Endemic, and the single cheapest thing to fix.
- **Duplicated Code**: the same action sequence in several flows.
- **Feature Envy**: a flow that reaches deep into another solution's list structure more than its own.
- **Data Clumps**: site URL, list name, and item ID passed together everywhere. They want to be one parameter object on a child flow's schema.
- **Primitive Obsession**: a status held as a free-text string rather than a choice column with a defined set of values.
- **Repeated Switches**: the same Switch on the same status value recurring in five flows. Consolidate into one child flow the five call.
- **Shotgun Surgery**: adding one status value requires editing six flows and three views.
- **Divergent Change**: one flow that handles both approvals and reporting, edited for two unrelated reasons.
- **Speculative Generality**: child flow parameters no caller ever populates.
- **Message Chains**: `body('Get_items')?['value'][0]?['fields']?['Requester']?['Email']`, which breaks silently on any shape change and returns null rather than failing.
- **Middle Man**: a child flow that only forwards its input to another child flow.
- **Refused Bequest**: a content type inheriting from a base type whose columns it overrides or ignores.

*The Spec axis.* Unchanged in mechanism. The sub-agent reads the specification or agent brief and reports what is missing, what was built that was not asked for, and what looks implemented but wrong. The scope-creep finding is worth emphasizing in your context, because Microsoft 365 work invites it: while you are in the flow anyway, it is easy to add three things nobody requested, and each one is a future maintenance obligation nobody agreed to.

**Operational framing.** This is separating conformance review from acceptance review and refusing to let one substitute for the other. In practice they answer different questions and are often best run by different reviewers, and merging them lets a reviewer satisfied on one axis stop examining the other.

---

### 3.17 `resolving-merge-conflicts`

**What it does and the mechanism.** Fourteen lines. Resolve conflicts by tracing each side's intent to its primary source ("Read the commit messages, check the PRs, check original issues/tickets"), preserve both intents where possible, never invent new behavior, run the project's automated checks, and "Always resolve; never `--abort`."

The mechanism is resolution by intent rather than by line selection, plus a completion rule that forbids the escape hatch.

**Verdict: low priority for your work, with one genuine exception.** Justification: most Microsoft 365 solution work today is single-author and does not involve concurrent branch development. The skill is not weakened; it just fires rarely.

The exception, if you adopt the repository pattern from section 5, is real and unpleasant: unpacked solution JSON merges badly, because two people editing different parts of the same flow in the maker interface produce two full regenerated definitions rather than two localized changes. The skill's discipline is exactly right for this case (resolve by intent, traced to what each side was trying to achieve, then verify by importing the merged solution and running the harness), but the practical answer is usually to avoid the situation: serialize flow edits, or split the work into separate solutions.

**Operational framing.** Skipped. Forcing an operational analogue onto a rarely-fired conflict-resolution procedure would be padding.

---

### 3.18 `wizard`

**What it does and the mechanism.** Generates an interactive script that walks a person through a manual procedure "that's tedious to do by hand and tedious to re-explain to an AI every time. It opens each URL, says exactly what to click and copy, captures the values, writes them where they belong ... confirms at every stage, and shows how many stages are left."

The mechanisms:
- **A fixed library, authored stages.** "The delightful UX is already solved by `template.sh` ... **Your job is only to scope the procedure and author its stages.** The library above the `STAGES` marker is identical in every wizard; that consistency is the point: never hand-edit it."
- **Scope before authoring, with an objective completion criterion.** "**Done when:** every stage is named in order, and for each captured value you know (a) where the human gets it, (b) where it's written ... and (c) whether it's secret."
- **Refuse to invent steps.** "Where you don't actually know the current UI or the exact command, say so and ask the user or check the docs: never invent steps that may not exist."
- **Confirmation gates before irreversible actions**, and one focused task per stage so nothing scrolls away.
- **Static verification rather than execution.** "Don't run it end-to-end yourself: it opens browsers and blocks on human input. Trace it statically instead."

**Verdict: translate surface (highly recommended, Stage 2).** The only surface is bash. Everything else is a well-designed procedure-authoring discipline.

**Solution Engineering translation.** Rewrite `template.sh` once as a PowerShell equivalent, keeping the same helper set: a stage function that clears the screen and shows progress, a prompt, a masked prompt for secrets, a URL opener, a confirmation gate, and a value writer. Then author stages against it, and never touch the library again. That one-time investment is what makes every subsequent runbook consistent.

The procedures worth building first, all of which you currently re-explain every time:
- **App registration and consent.** Create the registration, add the Graph permission scopes, obtain admin consent, create the client secret or certificate, record the tenant and application identifiers, and store the secret in Key Vault. Multiple stages, several captured values, one irreversible action (consent), and one secret. This is the archetypal case.
- **Environment provisioning.** Create the environment, assign the database, set the security group, configure the data loss prevention policy assignment, and record the environment identifier.
- **Connection reference setup for a new solution.** Create each connection under the service account, record the connection identifiers, and map them during import.
- **Agent publishing.** Configure the audience, submit for approval where required, verify the grounding sources resolved, and record the published identifier.
- **Solution promotion.** Export from development, import to test, remap connection references and environment variables, run the readiness checks, and promote to production. The confirmation gates matter here, because the import step is not cleanly reversible.

Two of the skill's rules deserve emphasis in your environment specifically. First, the refusal to invent steps: Microsoft admin portal navigation changes frequently, and a runbook containing a plausible-sounding but wrong click path is worse than no runbook. Verify against Microsoft Learn or ask, exactly as instructed. Second, "`confirm` before any irreversible action" is the built-in mechanism for the reversibility gap identified in section 4.7, and it should be applied more aggressively here than the skill's original context requires.

**Operational framing.** This is a runbook that executes itself: a written procedure that walks the operator through each step in order, confirms before anything irreversible, captures required values as it goes, and records where each one was written. The one-time cost of authoring it is repaid the second time the procedure runs, and it removes the failure mode where a step is skipped because the person running it had done it before.

---

### Productivity, user-invoked

---

### 3.19 `grill-me`

**What it does.** Seven lines: "Call the Skill tool with 'grilling'." The stateless entry point to the interview.

**Verdict: use as-is.**

**Solution Engineering translation.** None. Use it when you are not working in a repository: sharpening a proposal, a stakeholder presentation, a process design, or an architecture position before you have anywhere to write the artifacts. `ask-matt` is right that `grill-with-docs` is strictly better whenever a repository exists, "because it runs the same interview and leaves a paper trail."

**Operational framing.** The same alignment readback as 3.2, without the written record. Appropriate when there is nothing yet to write to, and a downgrade otherwise.

---

### 3.20 `handoff`

**What it does and the mechanism.** Writes a portable summary of the current conversation so another agent can continue. Its instructions are all about what to leave out: "Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead," and "Redact any sensitive information, such as API keys, passwords, or personally identifiable information."

The mechanism is pointer-based transfer rather than restatement, which keeps the handoff short enough to be read and stops it from becoming a stale second copy of the specification.

**Verdict: use as-is.**

**Solution Engineering translation.** None needed. The redaction rule matters more in your environment than in Matt's: a working session about a Graph integration routinely contains tenant identifiers, application identifiers, user principal names, and sometimes real business data pulled back from a list during testing. Read the redaction line as a hard requirement, not a suggestion.

`PHASE-BOUNDARIES.md` correctly constrains when to use it: only when something is actually travelling to a new tool, a new directory, or a colleague. "If nothing is travelling, you don't need it."

**Operational framing.** This is a structured handover between shifts on continuing work: what has been established, what is outstanding, and where the detail lives, written by reference rather than by restatement so that it stays current and short enough to be read.

---

### 3.21 `teach`

**What it does and the mechanism.** Turns the current directory into a stateful teaching workspace over multiple sessions, with a defined file structure: a statement of why the topic matters to the learner, a resource list, a reference library, a lesson library, a record of what has been learned, and a preferences file.

The mechanisms are, unusually for a skill file, drawn straight from learning science and stated correctly:

- **Purpose grounding.** Every lesson is tied to the learner's stated reason for wanting the topic, and the skill is blunt about what happens without it: "knowledge acquisition is not grounded in real-world goals. Lessons will feel too abstract. You will have no way of judging what the user should do next."
- **Fluency versus storage strength.** "**Fluency strength**: in-the-moment retrieval ... **Storage strength**: long-term retention. Fluency can give the user an illusory sense of mastery, but storage strength is the real goal."
- **Desirable difficulty, applied selectively.** Retrieval practice, spacing, and interleaving for skills. And the correct asymmetry: "For acquiring knowledge, difficulty is the enemy. It eats working memory you need for understanding," but "For skill acquisition, difficulty is the tool."
- **Working memory limits.** "The lesson should be short, and completable very quickly. Learners' working memory is very small."
- **Appropriate challenge level**, computed from the record of what has been learned so far.
- **Sources over recall.** "Never trust your parametric knowledge."
- **Reference material outlives lessons.** "Lessons will rarely be revisited later - reference documents will be. They should be the compressed essence of the lesson, in a format designed for quick reference."
- **Component reuse.** "Reuse is the default, not the exception ... never inline code a future lesson would duplicate."

**Verdict: use as-is.** No changes. This is the skill in the repository that most closely matches disciplines you already hold, and there is nothing technology-specific in it.

**Solution Engineering translation.** None required. Where it earns its place in your work: standing up a workspace for a domain you need working depth in rather than passing familiarity. Graph API permission models, Power Fx, Dataverse security roles, and Kusto query syntax are all good candidates, because each has a large surface, a real reference need, and a genuine gap between recognizing syntax and being able to produce it.

The reference library is the part that pays back beyond your own learning: a compressed, well-formatted reference on Graph permission scopes or delegation-safe SharePoint query patterns is directly reusable as team enablement material, which is a deliverable in its own right in most Solution Engineering roles.

**Operational framing.** This is a structured capability development plan with recorded progress and an explicit competency target, distinguishing what a learner can recognize from what they can reliably produce. The distinction between fluency and durable retention is precisely the one that separates a training session people enjoyed from one that changed how they work, and this skill has it right.

---

### 3.22 `to-questionnaire`

**What it does and the mechanism.** Turns a decision you cannot make alone into a Markdown questionnaire for the one person who can. The defining mechanism is stated in bold in the file:

> **Grill the send, not the subject.** Interview the user only about the _send_, which they can always answer: who it goes to, and what they need back. The questions in the document then target the **gap** between what the recipient knows and what the user needs.

Two steps, each with an objective completion criterion, then the document. The structure carries its own discipline: most-important-first ordering "since async means you may only get one pass", one idea per question with an answer stub beneath it, and a "why this matters" line only where the question could be misread. The "How to answer" section explicitly legitimizes incomplete responses: "Partial answers and 'I don't know' are useful: flag anything you're unsure of rather than skipping it."

**Verdict: use as-is.** No changes. High value.

**Solution Engineering translation.** None needed, but this is more useful in your role than in Matt's, because a Solutions Engineer is blocked on other people's knowledge constantly and in predictable categories:

- **The business process owner**, on the process rules you cannot infer: who can approve their own request, what happens when the named approver is on leave, whether a rejected request can be resubmitted, what the retention obligation is.
- **The security or compliance reviewer**, on whether an integration pattern is permitted: which Graph scopes are approvable, whether application permissions are allowed at all, what the data loss prevention position is on the connectors you need.
- **The licensing or tenant administrator**, on what is actually available: whether premium connectors are licensed, whether an environment can be provisioned, whether agent publishing to the whole organization requires an approval process.
- **The data owner**, on the shape and quality of the source you are integrating with.

The "grill the send, not the subject" rule is the load-bearing part and the part most easily lost. It works because you genuinely cannot be interviewed about the thing you do not know, and any attempt produces guesses dressed as requirements. Being interviewed about the send is always answerable.

**Operational framing.** This is a structured information request aimed at a specific person's expertise, ordered so that a partial response is still useful. Writing down what you need back before you write the questions is what stops it becoming a general request for comment that returns nothing actionable.

---

### 3.23 `wait-what`

**What it does and the mechanism.** Seven lines, fired the moment a message does not land:

> Wait, I don't understand where you've got to here. Re-pitch that: give me a little bit of context, talk in ASD-STE100 Simplified Technical English, and use the ubiquitous language from `CONTEXT.md`.

Three mechanisms in one sentence: a low-cost interrupt that carries no social penalty, a named plain-language standard rather than a vague request to simplify, and a requirement to re-pitch in the agreed vocabulary.

The choice of ASD-STE100 is not decoration. It is a controlled-language specification with a defined vocabulary and sentence-construction rules, developed for technical documentation that must be unambiguous to readers with varying language backgrounds. Naming it gives the instruction a real target instead of "explain it more simply."

**Verdict: use as-is.** No changes, no translation, no configuration. The lowest-cost adoption in the entire set.

**Solution Engineering translation.** None. Note the secondary use: the re-pitch it produces is often directly reusable as the stakeholder-facing explanation of the same thing, which is a recurring deliverable in your role.

**Operational framing.** This is an immediate clarification request with a defined output standard rather than a general appeal to simplify. Its value is that it is cheap enough to use every time, which is the only way a clarification mechanism actually gets used.

---

### Productivity, model-invoked

---

### 3.24 `grilling`

**What it does and the mechanism.** The interview primitive itself, fully described in section 2.1. `ask-matt` lists what runs it internally: `grill-me`, `grill-with-docs`, `triage`, `wayfinder`, and `improve-codebase-architecture`.

**Verdict: use as-is.** This is the most important single file in the repository and it contains no technology surface whatsoever. Twenty-eight lines, no code, no tooling, no platform assumptions.

**Solution Engineering translation.** None. Reach for it directly when you want the interview with no wrapper, per `ask-matt`.

One adoption note: the "recommended answer attached to every question" rule is what makes the sessions fast enough to run every time. Without it the interview becomes an open-ended requirements gathering exercise and stakeholders disengage. With it, the stakeholder is reviewing proposals rather than generating specifications, which is a much easier task and produces better disagreement.

**Operational framing.** Covered in 2.1. This is the alignment readback, and it is the mechanism the majority of the rest of the set depends on.

---

### 3.25 `writing-for-agents`

**What it does and the mechanism.** Fully described in section 2.9. `SKILL-MECHANICS.md` covers the skill-specific branch: the invocation choice and its cost model, the split-by-invocation rule, and why router skills exist.

**Verdict: use as-is.** Required reading before you write your own skills or your `CLAUDE.md`, and directly applicable to documentation systems work more broadly.

**Solution Engineering translation.** None for the skill. The transferable content, for the internal documentation and runbooks you produce as deliverables:

- The **information hierarchy** and its branching test ("inline what every branch needs, and push behind a pointer what only some branches reach") is a straightforwardly good rule for runbook design. Most enterprise runbooks fail by inlining every exception path into the main sequence until the main sequence is unreadable.
- **Completion criteria** on every step. "A vague bound ('understanding reached') invites **premature completion**." Every step in a deployment runbook should end on a condition the operator can objectively check.
- **Prompt the positive.** "Steering by prohibition drags the forbidden behaviour into context and makes it *more* available, not less." Write "run the flow under the service account" rather than "do not run the flow under your own account." This is well-established instructional practice and it is violated in most operational documentation.
- The **environment as a source of truth**: "a document that restates it is a **cache**: a copy of a lookup, earning its load only when the lookup is expensive." Do not restate a list's column names in a runbook. State the convention and the reason, which are the things that cannot be looked up.
- **No-ops.** "an instruction the model already obeys by default pays load to say nothing." The human equivalent: a runbook step telling a competent operator to do what they would obviously do anyway costs attention and returns nothing.

**Operational framing.** This is documentation design for procedures that are executed rather than read: ordered actions at the top, reference one level down behind a clear pointer, every step ending on an objectively checkable condition, and instructions written as what to do rather than what to avoid.

---

### 3.26 Non-promoted skills

`CLAUDE.md` defines these buckets: `misc/` is "kept around but rarely used, not promoted", and `in-progress/` is "beta: public on purpose, feedback wanted, not shipped in the plugin." They are covered here for completeness, with a verdict and justification for each.

| Skill | Bucket | Verdict | Justification |
| --- | --- | --- | --- |
| `loop-me` | in-progress | **Translate surface. Genuinely high value.** | The closest thing in the repository to your actual job. It runs a grilling session whose only output is workflow specifications, with a vocabulary built for exactly this: **Trigger** (event or schedule, and "Event-triggering is usually the more efficient"), **Checkpoint** ("a human-in-the-loop point where the user is asked to verify or decide"), **Push right** ("defer the checkpoint as far as it will go. Do maximal work before involving the human, so they are asked once, late, with everything prepared"), and **Brief** ("a tight, decision-ready summary ... never the raw output"). Push right and Brief are the two best pieces of approval design advice in the whole set, and they translate to Power Automate approval design with no change at all. Its completion criterion is strong: "A workflow spec is done when an implementer agent could build it without asking a single question." Surface to translate: none of consequence. It is beta, so expect it to change. |
| `retro` | in-progress | **Translate surface. Adopt the concept now, the file later.** | A stub ("design notes only, not functional yet") but the categories are the right ones for a lessons-learned review of an agent-assisted session: navigation, automated checks, coding standards, steering-file size, tool economy, no-op instructions, and information access. Its architectural point is worth carrying regardless: "the review agent should be responsible for imposing coding standards, not the implementation agent," because the implementation agent carries all the context pressure. That maps directly onto how you should split your own review. |
| `writing-fragments` / `writing-beats` / `writing-shape` | in-progress | **Translate surface. Moderate value for documentation deliverables.** | A three-stage writing pipeline: gather raw material without structure, then shape it, with a shared **grounding** discipline (a concept must be established before a later section can rely on it, either as a stated prerequisite or by an earlier section introducing it). That is a clean and correct statement of prerequisite sequencing, and it applies directly to writing training material, adoption guides, and architecture documents for mixed audiences. The lever it names is the real one: "Demand too much up front and you shut out readers who don't have it; ground too much inside and the early beats drown in definitions." |
| `claude-handoff` | in-progress | **Low priority.** | Same mechanism as `handoff`, but it launches a background agent via a specific command line rather than writing a file. The mechanism is not weakened; it is just a delivery variant tied to one harness. Use `handoff` unless you specifically want the background launch. |
| `implement-spec` | in-progress | **Low priority for now.** | Works the tickets as a task graph rather than a list, running implementer agents across the ready frontier concurrently, each in its own git worktree, landing as one pull request. The frontier-concurrency mechanism is genuinely valuable and the "communicate primarily through **context pointers**" instruction is good practice. But the execution model assumes git worktrees and per-branch isolation, and Microsoft 365 artifacts cannot be built concurrently in isolated copies: two agents cannot edit the same solution in the same environment at once. Revisit only if your work becomes predominantly PowerShell and Azure Function development, where the model holds. |
| `setup-ts-deep-modules` | in-progress | **Low priority as written; the rule is worth stealing.** | Wires a dependency analysis tool into a TypeScript repository so that a package's public surface is its root files and everything in subfolders is private. TypeScript-specific and not translatable as a tool. The *rule* has a direct analogue worth adopting by convention: a child flow is reachable only through its declared trigger contract, and a PowerShell module exposes only what it explicitly exports. Its verification step is the model to copy regardless of language: "**Done when:** you have observed a pass, then a fail on the deep import, then a pass again. If step 2 does not fail, the rules are not wired correctly." That is the red-before-green discipline applied to a static check, and it is the correct way to commission any validation rule. |
| `git-guardrails-claude-code` | misc | **Use as-is. Worth adopting early.** | Installs a hook that blocks destructive git commands before they execute. Cheap, platform-neutral, and useful the moment you start keeping unpacked solutions in source control, where an accidental hard reset loses work that cannot be re-exported. |
| `setup-pre-commit` | misc | **Translate surface. Moderate value.** | Husky and lint-staged are the surface. The mechanism is running the cheap checks automatically at commit time rather than relying on memory. Translate to: PSScriptAnalyzer on PowerShell, a JSON validity check on unpacked solution files, and a naming-convention check. The value depends entirely on whether you adopt the repository pattern in section 5. |
| `migrate-to-shoehorn` | misc | **Low priority.** | A one-off migration from TypeScript `as` assertions to a specific TypeScript library. No mechanism to transfer; the entire content is the surface. |
| `scaffold-exercises` | misc | **Low priority.** | Creates exercise directory structures that pass a specific course repository's linter. Entirely specific to Matt's course tooling. The general idea (scaffold a conventional directory structure so it passes an automated check) is one you might reimplement for your own solution repository layout, but there is nothing here to reuse. |

---

## 4. Feedback-loop gap analysis

The README's third failure mode is the one where the transfer is genuinely hardest: "You need the usual tranche of feedback loops: static types, browser access, and automated tests." Microsoft 365 work has weaker versions of all three and lacks two things Matt's setting takes entirely for granted.

Each gap below states the original loop, what the environment actually provides, the closest honest substitute, exactly how the substitute is weaker, and the discipline that compensates. Where a substitute is not weaker, that is stated too.

### 4.1 Static types

**Original loop.** Compile-time verification, instant, total coverage, free at the point of use.

**What the environment provides.** Power Automate has no compile step. A malformed expression fails at runtime, on a real run, potentially after side effects have occurred. There is no equivalent of a type error at authoring time for expression content.

**Closest honest substitute.** Four things stacked, in descending strength:
1. **A JSON schema on every child-flow HTTP request trigger.** This is the strongest and most type-like mechanism available. A declared schema rejects a malformed payload at the boundary and generates typed dynamic content for downstream actions. It is a genuine interface contract that is enforced at runtime.
2. **Parse JSON with an explicit schema** rather than navigating dynamic content with chained null-safe accessors. The parse step becomes the place where a shape violation surfaces, rather than a null propagating silently through four more actions.
3. **The flow checker and the Power Platform solution checker**, which perform static analysis for known defect patterns and give design-time warnings.
4. **PSScriptAnalyzer** for PowerShell, which is a genuine static analysis loop.

**Where it is weaker.** Materially, in three ways. Coverage is partial: expressions inside a string are opaque to every check listed above, so a mistyped column name in an expression is invisible until it runs. The checks are on demand rather than continuous, so nothing tells you at the moment of the mistake. And the schema only guards the boundary, not the interior: everything after the parse is unverified.

**Compensating discipline.** Put a schema on every child-flow trigger without exception, so that every reusable unit has an enforced contract at its seam. Parse JSON explicitly rather than navigating dynamically, which converts the "Message Chains" smell into a single checked step. Keep expressions short, because a long expression is an unverified program in a string literal. And treat the first tracer bullet as the type check: an end-to-end run against real data is the only thing that verifies the expression content, so run it early rather than after everything is built.

### 4.2 Automated tests, for flows

**Original loop.** A test runner, red before green, subsecond feedback, unattended.

**What the environment provides.** No native test framework for flows.

**Closest honest substitute.** The child-flow harness pattern, which is stronger than most people expect:

- Build the logic as a child flow with an HTTP request trigger and a declared JSON schema. That is the seam.
- Build a harness that posts fixture payloads to that trigger. It can be a parent flow with a set of test cases, or a PowerShell script issuing the HTTP calls, which is preferable because it is invocable by an agent without the maker interface.
- Assert with a Condition action whose false branch runs a Terminate action with status `Failed`. That produces a genuinely binary pass or fail in run history.
- Keep fixtures as committed files with independently derived expected values, per the tautology rule in `tdd`.

Red before green works here in full: write the harness case, run it against the current flow, watch it fail, change the flow, watch it pass. That is not an approximation of the mechanism; it is the mechanism.

**Where it is weaker.** Speed, principally. A harness run takes seconds to minutes rather than milliseconds, which changes how often you will run it and therefore how tight the loop is. It consumes real connector calls and counts against throttling limits. It requires a development environment with test data, so setup cost is real. And it only covers logic that has been factored into a child flow with a trigger contract: a monolithic flow triggered by a list item creation cannot be tested this way at all.

**Compensating discipline.** The last weakness is the important one and it is also the fix: the requirement to be testable forces the design toward child flows with declared contracts, which is exactly the deep-module shape `codebase-design` argues for. Design for the harness and you get the architecture as a byproduct. For speed, follow the "tighten the loop" section of `diagnosing-bugs` literally: cache setup, narrow scope, pin time values, and use fixed fixture data rather than querying live sources.

### 4.3 Automated tests, for PowerShell and Graph tooling

**Original loop.** As above.

**What the environment provides.** Everything. Pester is a full test framework with mocking, and the `mocking.md` rule ("Mock at **system boundaries** only") applies verbatim: mock the Graph call, never your own functions.

**Where it is weaker.** It is not. State this plainly, because it matters for how you sequence adoption: the parts of your work that are PowerShell get the full-strength loop with no compromise, which makes them the right place to practice the `tdd` discipline properly before attempting the weaker substitutes elsewhere.

**Compensating discipline.** None needed. Apply `tdd` as written.

### 4.4 Automated tests, for Copilot agents

**Original loop.** Deterministic assertions, binary pass or fail.

**What the environment provides.** A test interface, and non-deterministic output.

**Closest honest substitute.** A fixed evaluation prompt set, written before the agent is built, with each prompt paired to an assertion. The assertion design is what determines whether this is worth anything:

- **Assert on retrieval, not wording.** "The response cites document X" is checkable. "The response is helpful" is not.
- **Assert on facts that must appear.** "The response contains the current approval threshold value" is checkable against a known-correct value.
- **Assert on refusals.** "A question outside the grounding scope produces a decline rather than an invented answer" is one of the most important assertions and one of the most often omitted.
- **Assert on permission trimming.** Run the same prompt as a user who should not have access to a source and confirm the source is not surfaced. This is checkable and is a genuine security control.

**Where it is weaker.** Substantially, and it should not be described otherwise. The result is a score rather than a binary verdict, so there is no true red or green. The same prompt can pass and fail across runs. Assertion checking is either manual or itself performed by a model, which introduces its own error. And the loop is slow enough that nobody will run it on every change.

**Compensating discipline.** Four things. Fix the prompt set before building, so it cannot be quietly shaped to what the agent happens to do. Set a numeric threshold in advance and treat it as the gate (for example, all permission-trimming and refusal assertions must pass, and at least 90 percent of retrieval assertions), which restores an objective pass criterion even though the underlying signal is not binary. Require a human sign-off on the evaluation run before publishing, which is honest about the fact that the loop is not fully automatable. And put the agent's declared actions and tool integrations behind child flows or functions that *are* testable, so that the non-deterministic surface is as small as possible. That last point is the important one: the reasoning is untestable, but the things the agent can do should be tested at their own seams.

### 4.5 Browser access and seeing it run

**Original loop.** The agent drives a headless browser, asserts on the DOM, and sees what the user sees.

**What the environment provides.** The agent cannot practically drive SharePoint or the Teams client. Authentication is interactive and conditional-access protected, and browser automation against Microsoft 365 surfaces is fragile enough that it is rarely worth the maintenance.

**Closest honest substitute.** Split the verification. The agent verifies *state* through APIs: PnP PowerShell and Graph read-backs confirm that the list item has the expected status, that the permission was applied, that the file landed in the right library, that the schema matches the template. The person verifies *experience*: the card renders correctly in Teams, the form is usable, the agent's response reads sensibly.

**Where it is weaker.** The agent verifies data, not experience, and a solution can be correct in every data assertion while being unusable. This is a genuine and permanent gap, not one that closes with better tooling.

**Compensating discipline.** Make the split explicit rather than accidental. The agent owns state assertions and runs them automatically. The person owns a written experience checklist, run before deployment, covering the specific things only a person can judge. Treat that checklist as a deliverable of the specification, written during the alignment readback while the acceptance criteria are being agreed, not improvised at the end. This is the one place where the substitute is a human procedure, and it is worth being honest that this is a real cost rather than describing it as equivalent coverage.

### 4.6 A diff as the review surface

**Original loop.** `git diff <fixed-point>...HEAD` produces a complete, precise, mechanically generated record of every change.

**What the environment provides.** By default, nothing. A flow edited in the maker interface leaves no reviewable change record.

**Closest honest substitute.** Put the artifacts in source control, as detailed in 3.16: `pac solution unpack` for Power Platform solutions, `Get-PnPSiteTemplate` for SharePoint structure, exported configuration for agents, and ordinary source for PowerShell. This restores a genuine line-level diff for most of what you build.

**Where it is weaker.** The exports are machine-generated, so the signal-to-noise ratio is poor: a one-condition change can produce a large diff full of regenerated identifiers and positional metadata, and a semantic change can hide inside it. The export is also a point-in-time snapshot rather than a continuous record, so the granularity of the history is however often you remember to export. And where you have not adopted the repository pattern at all, the only substitute is a human-written change record, which is materially weaker because it depends on the author's completeness and cannot reveal an unintended change.

**Compensating discipline.** Export and commit on a fixed trigger (before and after every change set, not on a schedule), so the diff boundaries line up with units of work. Commit a short human-written change summary alongside each export, and have the Spec axis of the review read the summary while the Standards axis reads the export. And accept the noise rather than trying to eliminate it: the reviewer's job on a machine-generated diff is to confirm that every semantic change in the summary appears in the export and that nothing else does.

### 4.7 Reversibility

**Original gap.** This one has no counterpart in Matt's system, because in a code repository nearly everything is reversible with a commit. It needs to be added rather than translated.

**What the environment provides.** Many operations are not reversible. Deleting a SharePoint column loses its data. A mass notification cannot be recalled. A permission change propagates immediately. An approval decision written back to a system of record is a business record. Removing a solution component on import can delete data.

**Closest honest substitute.** Three things, all borrowed from skills already in the set:
1. The **wizard** skill's confirmation gate before any irreversible action, which is already specified: "`confirm` before any irreversible action."
2. A **dry-run parameter** on every flow that has side effects, defaulting to logging the intended action to a list rather than performing it. The `prototype` skill's rule ("No persistence by default. State lives in memory") is the same instinct applied earlier in the lifecycle.
3. A **development environment with test-only data**, so that the first tracer bullet cannot touch anything real.

**Where it is weaker.** These reduce the probability of an irreversible mistake; they do not create an undo. There is no equivalent of reverting a commit for a mass mail send.

**Compensating discipline.** A written pre-deployment readiness checklist per change class, produced during specification rather than at deployment time, stating for each change what the rollback is or explicitly that there is none. A change with no rollback and no stated acceptance of that fact should not be deployed. This is the one discipline in this report with no analogue in the source repository, and it is required because the environment genuinely differs.

### 4.8 Summary

| Loop | Substitute | Strength | Compensating discipline |
| --- | --- | --- | --- |
| Static types | Trigger JSON schemas, explicit parse, solution and flow checkers, PSScriptAnalyzer | Partial. Expressions remain unverified until runtime | Schema on every child-flow trigger; short expressions; run the tracer bullet early |
| Tests, flows | Child-flow harness with Terminate on assertion failure | Good. Genuinely red-capable, but slow and requires the child-flow shape | Design for the harness, which produces the right architecture anyway |
| Tests, PowerShell | Pester | Full strength. No compromise | None needed |
| Tests, agents | Fixed evaluation prompt set with retrieval, refusal, and permission assertions | Weak. Non-deterministic, scored not binary | Fixed prompt set written first; numeric threshold set in advance; human sign-off; push testable behavior behind child flows |
| Browser access | Agent asserts state through APIs; person verifies experience | Partial. Data verified, experience not | Written experience checklist, produced during specification |
| Diff | `pac solution unpack`, PnP site templates, exported agent configuration, in git | Good but noisy. Machine-generated, snapshot-based | Export on change-set boundaries; human-written change summary alongside |
| Reversibility | Confirmation gates, dry-run parameters, development environment | Reduces probability only. No undo exists | Written rollback position per change class, agreed during specification |

---

## 5. Setup plan

This section is a run plan for `/setup-matt-pocock-skills` in your situation. The skill is "a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write," so it will ask; this is what to answer and why.

### 5.1 Prerequisite: decide what a repository is when the work lives in Microsoft 365

The skill assumes a repository, and every engineering skill downstream of it assumes the same. That assumption is the one real obstacle, and the answer is to create the repository deliberately rather than to work around its absence.

**Recommended: one repository per business domain, not per solution.** A domain here is a coherent area of the business you serve: HR, Finance, Facilities, IT Service Management. This is the right granularity because the glossary and the decision records are domain-scoped, and a per-solution repository would fragment both into pieces too small to be useful.

Suggested layout:

```
<domain>-solutions/
├── CLAUDE.md                       (or AGENTS.md; the setup skill writes into one of these)
├── CONTEXT.md                      (the controlled vocabulary for this domain)
├── docs/
│   ├── adr/                        (decision records, numbered from 0001)
│   ├── agents/                     (written by the setup skill)
│   │   ├── issue-tracker.md
│   │   ├── triage-labels.md
│   │   └── domain.md
│   ├── standards/
│   │   └── SOLUTION_STANDARDS.md   (the Standards axis of code-review reads this)
│   ├── runbooks/                   (wizard output that earned a permanent home)
│   └── research/                   (research skill output, cited)
├── src/
│   ├── solutions/<name>/           (pac solution unpack output)
│   ├── sites/<name>/               (PnP site templates)
│   ├── agents/<name>/              (instructions, grounding manifest, evaluation prompt set)
│   └── scripts/                    (PowerShell modules and tooling)
├── tests/
│   ├── harness/                    (flow harness scripts and fixtures)
│   └── pester/                     (PowerShell tests)
└── .scratch/                       (local specifications and tickets, if using the local tracker)
```

**Multi-context.** The skill offers a multi-context layout with a root `CONTEXT-MAP.md` "only when exploration found monorepo signals." Its signals are npm-specific and will not fire. The genuine analogue: adopt multi-context when one repository serves several business domains with genuinely different vocabularies, where "Request" means something different in Facilities than in HR. If each domain has its own repository, you are single-context and should stay there. `CONTEXT-FORMAT.md` is right that this "fits almost every repo."

### 5.2 Section A: issue tracker

The skill offers GitHub, GitLab, local markdown, or "Other", where "Other" means describing the workflow in a paragraph that gets recorded as prose.

The constraint that decides this is not preference. It is whether an agent can read and write the tracker from a command line. `to-tickets`, `to-spec`, and `triage` are all hard dependencies on the tracker per ADR 0001, and a tracker the agent cannot drive makes them unusable.

Assessed against that constraint:

| Option | Agent-drivable | Fit for Microsoft 365 work |
| --- | --- | --- |
| **Azure DevOps Boards** | Yes, via the `az boards` CLI | Strong. Likely already present in a Microsoft environment, supports parent and child relationships and blocking links natively, and is a credible system of record for stakeholders |
| **GitHub Issues** | Yes, via `gh` | Strong technically, and it is what the skills were built against. Weak organizationally if your stakeholders do not have access or your organization does not use it |
| **Local markdown** | Yes, ordinary file operations | Strong for the design record, with no stakeholder visibility at all |
| **Planner or a SharePoint list** | Not practically | Poor. No usable command-line surface, so the hard-dependency skills degrade badly |

**Decision: Azure DevOps Boards, declared as "Other", with a written workflow.** It satisfies the agent-drivability constraint, it has native blocking relationships which `wayfinder` explicitly prefers ("Blocking uses the tracker's **native** dependency relationship: essential because it renders the frontier *visually* in the tracker's own UI"), and it is a system of record your stakeholders can already see.

Fallback if Azure DevOps becomes unavailable: **local markdown** for the design record, with a deliberate, stated synchronization rule to whatever the business tracks work in. Be explicit that this is a two-system arrangement with a manual reconciliation step, rather than pretending the markdown is the system of record.

`docs/agents/issue-tracker.md` must contain the concrete command forms, in the shape the GitHub template uses: how to create an item, read one with its comments, list by label, comment, apply and remove labels, close, and the wayfinding operations (create a parent map item, create a child, add a blocking link, query the frontier, claim, resolve). Without those concrete forms the skills guess, and guessed commands fail silently. Section 5.6 supplies that content, ready to paste.

Three platform differences change the wording of the tracker document, and all three are surface rather than mechanism:

- **Azure Boards has tags, not labels.** The five triage roles map to tag strings, set through the `System.Tags` field. Everywhere a skill says "apply the label", read "apply the tag".
- **Comments are a parameter, not a subcommand.** There is no `comment` verb. A comment is added by `az boards work-item update --discussion "..."`, which means every triage note and resolution comment rides on an update call.
- **Closing is a state change, not a verb.** There is no `close` command. Set `System.State` to the closed state your process template actually uses, which varies: Agile uses `Closed`, Scrum uses `Done`, Basic uses `Done`. Confirm yours once and write the literal string into the tracker document rather than leaving it generic.

### 5.3 Section B: triage labels

The skill's default is the five canonical roles with the label string equal to the role name. Two changes, both surface, both justified in 3.3. Note that on Azure Boards these are **tags**, so the right-hand column is the tag string written into `System.Tags`:

| Canonical role | Your tag | Meaning |
| --- | --- | --- |
| `needs-triage` | `needs-triage` | Awaiting assessment |
| `needs-info` | `awaiting-requester` | Blocked pending information from the person who raised it |
| `ready-for-agent` | `ready-for-agent` | Fully specified, with a written brief, ready to be picked up |
| `ready-for-human` | `ready-for-human` | Requires an action only a person can take: admin consent, licensing, a tenant setting, a policy exception |
| `wontfix` | `not-planned` | Will not be actioned |

Categories: keep the two canonical ones, renaming `bug` to `defect` for a business-facing audience. Resist adding more, because the state machine's conflict detection depends on exactly one category and one state per item.

Add `needs-security-review` and `needs-license-review` as free-standing tags **outside** the state machine, and say so explicitly in `docs/agents/triage-labels.md`. They are real routing signals in your work, but making them state roles breaks the invariant that lets `triage` detect a conflicting state.

One mechanical caution specific to Azure Boards: `System.Tags` is written as a **whole-field replacement**, not as an add or remove operation. Setting it to `ready-for-agent` silently drops every other tag on the item. So "apply a tag" is really read-modify-write: read the current tags, change the one role you mean to change, and write the full set back. Write that instruction into the tracker document, because an agent following the GitHub template's `--add-label` mental model will quietly erase the category tag every time it changes state.

### 5.4 Section C: domain documents

Answer **single-context** unless you have genuinely merged several business domains into one repository. `CONTEXT.md` at the repository root, `docs/adr/` beside it.

Take the lazy-creation rule seriously: "Create files lazily: only when you have something to write." Do not seed `CONTEXT.md` with forty terms before the first session. A glossary written speculatively is a glossary of guesses, and it will be wrong in exactly the places that matter. The first term goes in when the first term is actually resolved during a grilling session.

### 5.5 Additional setup the skill does not cover

Four things the skill will not ask about but that your environment needs:

1. **`docs/standards/SOLUTION_STANDARDS.md`.** The Standards axis of `code-review` reads whatever documents how work should be built, and in a fresh repository that is nothing. Write it early, per the contents listed in 3.16. Until it exists, the Standards axis runs on the Fowler baseline alone, which is useful but incomplete.
2. **A PowerShell wizard template.** Translate `template.sh` once, keeping the helper set and the discipline that the library above the stage marker is never hand-edited. Everything you build with `wizard` depends on this existing.
3. **The harness pattern, written down.** Document the child-flow harness convention (schema on the trigger, fixture files, Condition plus Terminate assertion, where fixtures live) as a runbook, so that every subsequent harness looks the same rather than being reinvented.
4. **The export and commit procedure.** Document how solutions, site templates, and agent configuration get exported and committed, and when. Without this the repository drifts out of sync with the tenant within weeks and the diff surface stops being trustworthy.

### 5.6 `docs/agents/issue-tracker.md`, ready to paste

This is the "Other" workflow prose the setup skill records, written in the shape of the repository's own `issue-tracker-github.md` so the skills find what they expect. Paste it as `docs/agents/issue-tracker.md` and fill the three bracketed values on first use.

Verification status, stated so you know what to trust: the link type reference names and their direction, and the relation types accepted by the CLI, were confirmed against Microsoft's published documentation. The three bracketed values below are environment-specific and must be confirmed against your own organization before the document is relied on.

```markdown
# Issue tracker: Azure DevOps Boards

Issues, specs, and wayfinding maps for this repo live as Azure Boards work items.
Use the `az boards` CLI (the `azure-devops` extension) for all operations.

## Fixed values for this project

- Organization: `https://dev.azure.com/[ORG]`
- Project: `[PROJECT]`
- Work item type used for issues, specs, and tickets: `[TYPE]` (commonly `Issue` on
  the Basic process, `User Story` on Agile, `Product Backlog Item` on Scrum)
- Closed state string: `[CLOSED-STATE]` (`Closed` on Agile, `Done` on Scrum and Basic)

Set the defaults once so no command needs to repeat them:

    az devops configure --defaults organization=https://dev.azure.com/[ORG] project=[PROJECT]

## Conventions

- **Create an item**: `az boards work-item create --title "..." --type "[TYPE]"
  --description "..." --fields "System.Tags=needs-triage"`.
  Returns JSON; the new id is `.id`.
- **Read an item**: `az boards work-item show --id <id>`. Comments are not included
  in that payload; fetch them separately with
  `az boards work-item relation list --id <id>` for links, and read the discussion
  through the work item's `_links` or the REST comments endpoint.
- **List by tag**: use a WIQL query (see below). There is no `--label` filter.
- **Comment on an item**: `az boards work-item update --id <id> --discussion "..."`.
  There is no separate comment command; the comment rides on an update.
- **Apply / change a triage tag**: `System.Tags` is a whole-field replacement, so this
  is read-modify-write, never an append:
  1. `az boards work-item show --id <id> --query "fields.\"System.Tags\"" -o tsv`
  2. Change only the one role you mean to change, keeping every other tag.
  3. `az boards work-item update --id <id> --fields "System.Tags=<full semicolon-separated set>"`
  Writing a bare tag string without step 1 silently drops the category tag.
- **Close**: `az boards work-item update --id <id> --state "[CLOSED-STATE]" --discussion "..."`.
  Closing is a state change, not a delete.

## Queries

All listing is WIQL, run with `az boards query --wiql "..."`.

- **Everything needing attention** (untagged, or awaiting triage):

      SELECT [System.Id], [System.Title], [System.Tags], [System.State]
      FROM workitems
      WHERE [System.TeamProject] = '[PROJECT]'
        AND [System.State] <> '[CLOSED-STATE]'
        AND ([System.Tags] CONTAINS 'needs-triage' OR [System.Tags] IS EMPTY)
      ORDER BY [System.CreatedDate] ASC

- **Ready for an agent to pick up**: same shape, with
  `[System.Tags] CONTAINS 'ready-for-agent'`.

Tags are matched with `CONTAINS`, never `=`, because the field holds a
semicolon-separated set.

## When a skill says "publish to the issue tracker"

Create a work item of type `[TYPE]` with the spec or ticket body as its description,
and set `System.Tags` to `ready-for-agent`.

## When a skill says "fetch the relevant ticket"

`az boards work-item show --id <id>`, plus its relations and discussion.

## Wayfinding operations

Used by `wayfinder`. The **map** is a single work item; its tickets are **child**
work items of it.

- **Map**: a work item tagged `wayfinder:map`, holding the Destination / Notes /
  Decisions-so-far / Not-yet-specified body.
- **Child ticket**: create the ticket, then link it to the map:

      az boards work-item relation add --id <ticket-id> --relation-type parent \
        --target-id <map-id>

  Tag each ticket `wayfinder:<type>` (`research`, `prototype`, `grilling`, `task`).
- **Blocking**: use the native dependency link. On Azure Boards, **Predecessor** is
  the item that must complete first, so a ticket is blocked by its predecessors:

      az boards work-item relation add --id <blocked-ticket> \
        --relation-type predecessor --target-id <blocker-ticket>

  The underlying reference names are `System.LinkTypes.Dependency-Reverse`
  (Predecessor) and `System.LinkTypes.Dependency-Forward` (Successor). This link
  renders in the Boards UI and in delivery plans, which is why it is preferred over
  a body convention. Run `az boards work-item relation list-type` once to confirm the
  exact strings your organization accepts.
- **Frontier query**: the map's open children that have no open predecessor and no
  assignee. Query the children, then for each,
  `az boards work-item relation list --id <id>` and drop any with a predecessor whose
  state is not `[CLOSED-STATE]`.
- **Claim**: `az boards work-item update --id <id> --assigned-to "<you>"`, before any
  other work in the session.
- **Resolve**: `az boards work-item update --id <id> --discussion "<answer>"
  --state "[CLOSED-STATE]"`, then append a context pointer (gist plus link) to the
  map's Decisions-so-far.

## Item URLs

Refer to items by title in anything a human reads, per `wayfinder`'s "Refer by name"
rule. The link behind the name is
`https://dev.azure.com/[ORG]/[PROJECT]/_workitems/edit/<id>`.
```

Two things above are worth calling out because they are the places this will break if treated as equivalent to the GitHub template. The tag replacement behaviour is a genuine trap: the GitHub template's `--add-label` is additive and the Azure Boards equivalent is not, so an agent carrying the GitHub mental model across will erase tags it never intended to touch. And the predecessor direction is easy to invert: the blocker is the predecessor, so the relation is added *on the blocked item, pointing at the blocker*, which is the opposite of how people usually say it out loud.

---

## 6. Adoption sequence

Three stages, each with objective entry criteria that must be satisfied before advancing. Criteria are stated as conditions that can be checked rather than as judgements about readiness, and the intent is that a stage is not entered on schedule but on evidence.

The sequencing principle: each stage adds only skills whose prerequisites the previous stage has actually produced. Adopting `to-tickets` before a tracker exists, or `code-review` before a diff surface and a standards document exist, produces the appearance of the discipline without the mechanism.

### Stage 1: Foundation

**Skills adopted:** `grilling`, `grill-me`, `grill-with-docs`, `domain-modeling`, `research`, `wait-what`, `handoff`, `to-questionnaire`, `ask-matt` (for `PHASE-BOUNDARIES.md`), `wizard`, `diagnosing-bugs`.

**Why these.** Every one works with no repository, no tracker, and no source control. Together they cover the two failure modes that cost the most in Solution Engineering (misalignment and vocabulary drift), the diagnostic discipline, and the human-only-procedure problem. They also produce the artifacts the next stage depends on.

**Entry criteria:** none. Start here.

**What you are building.** A `CONTEXT.md` and a decision record set for at least one business domain, and the habit of running the interview before the build rather than after the first draft is rejected.

**Objective criteria to be met before entering Stage 2:**

1. `grill-with-docs` has been run at the start of at least five real pieces of work, before any build effort was committed to those pieces.
2. `CONTEXT.md` contains at least fifteen terms, each with a definition of two sentences or fewer and an `_Avoid_` list, and contains at least one entry under a flagged-ambiguities heading recording a term that was contested and resolved.
3. At least three decision records exist, and each one demonstrably satisfies all three gates from `ADR-FORMAT.md` (hard to reverse, surprising without context, the result of a genuine trade-off). A record that fails any gate is removed rather than counted.
4. You can name at least one specific instance where the interview changed the design before build effort was spent. This is the criterion that distinguishes running the skill from being changed by it.
5. At least one `wizard` runbook exists in PowerShell, has been executed end to end by a person other than its author, and completed without that person needing to ask a clarifying question.
6. `diagnosing-bugs` has been run on at least two real faults, and in both cases a named, repeatable command or harness invocation existed and was observed to fail before any hypothesis was recorded.

Criterion 6 is the one most likely to be failed, and it is the one least worth waiving. It is the specific discipline the skill exists to enforce.

### Stage 2: Integration

**Skills adopted:** `setup-matt-pocock-skills`, `to-spec`, `to-tickets`, `implement`, `tdd`, `codebase-design`, `code-review`, `prototype`, plus `git-guardrails-claude-code` and `setup-pre-commit` as supporting hygiene.

**Why these.** All of them depend on infrastructure Stage 1 did not require: a tracker, a repository, a diff surface, a standards document, and a working test harness. Attempting them earlier produces the ceremony without the feedback.

**Entry criteria (all six Stage 1 criteria met, plus):**

7. A domain repository exists with the layout from section 5.1, and `/setup-matt-pocock-skills` has been run against it, producing `docs/agents/issue-tracker.md` with concrete command forms, `docs/agents/triage-labels.md`, and `docs/agents/domain.md`.
8. At least one Power Platform solution has been unpacked into the repository and committed, and a second export has been committed showing a reviewable diff of a real change.
9. `docs/standards/SOLUTION_STANDARDS.md` exists and covers, at minimum, naming conventions, connection reference and ownership rules, environment variable usage, the required error handling pattern, and delegation-safe query patterns.

**Objective criteria to be met before entering Stage 3:**

10. At least one child flow exists with a declared JSON schema on its trigger, and a harness that invokes it with fixture payloads and asserts via Terminate on failure.
11. That harness has been observed to go red on a real defect and green after the fix. Not a demonstration fault introduced to prove the harness works, but an actual defect found in real work. This is the red-before-green criterion applied to the harness itself, and it is the single most important gate in the sequence.
12. Pester tests exist for at least one PowerShell module, written test-first for at least one function.
13. `code-review` has been run with both axes on at least three change sets, with the Standards axis pointed at the standards document from criterion 9, and the two axes' findings have been kept separate in the report.
14. At least three work items have been decomposed with `to-tickets` into slices meeting the vertical rule, and the first slice in each case was demonstrable to the requester on its own.
15. At least one `prototype` logic demonstration has been put in front of a business stakeholder before the corresponding build started, and its verdict recorded.

Criterion 11 is the gate that most matters. A harness that has never been red has not been shown to be capable of going red, and in an environment with this few feedback loops, a validation regime that cannot fail is the most expensive kind of false assurance.

### Stage 3: Full operation

**Skills adopted:** `triage`, `wayfinder`, `improve-codebase-architecture`, `teach`, `writing-for-agents`, `loop-me`, `retro`, and the authoring of your own skills.

**Why these last.** Each requires something the first two stages produce. `triage` requires an intake volume worth a state machine and a place to put briefs. `wayfinder` requires an effort genuinely too large for one session, and applying it to a well-scoped feature is a documented misuse. `improve-codebase-architecture` requires a survey surface and a standards document, or its findings are unactionable. Writing your own skills requires enough repeated practice that you know which parts of your work are actually repeatable.

**Entry criteria (all fifteen prior criteria met, plus):**

16. Intake volume is high enough that untriaged requests accumulate. If everything is actioned as it arrives, `triage` is overhead and should be deferred.
17. At least one request has arrived that is genuinely too large to plan in a single session, where the shape of the work is not yet visible. `ask-matt` is explicit that `wayfinder` is "slower and denser, so save it for exactly that, never a well-scoped feature."
18. The standards document has been stable for a period, meaning architecture survey findings can be assessed against a settled baseline rather than a moving one.

**Objective criteria for the stage being fully operational:**

19. `triage` has processed at least ten incoming requests through the state machine, at least three have been verified before specification (confirmed, not reproducible, or insufficient detail), and `.out-of-scope/` contains at least one recorded rejection that has since prevented a repeat request from being relitigated.
20. At least one architecture survey has produced a candidate that was actioned, and the deletion test was applied to it explicitly.
21. At least one skill has been written for your own recurring work, following `writing-for-agents`, with every step ending on an objectively checkable completion criterion.
22. A structured retrospective has been run on at least one completed piece of work, using the `retro` categories, and produced at least one change to the standards document, the automated checks, or the steering files.

Criterion 22 is what makes the whole set self-improving rather than static. Without it the disciplines are applied but never tuned to how the work actually goes, and the standards document slowly stops describing the work it governs.

### What full operation looks like

A request arrives and is triaged into a state with a written brief. Work that is well-scoped runs through the interview, produces a specification with confirmed test seams, decomposes into slices whose first increment is demonstrable, and is built with the harness going red before it goes green. Work that is not yet well-scoped is charted as decisions before it is charted as work. Faults are diagnosed against a repeatable observation before a theory is formed. Changes are reviewed on two axes that are not permitted to mask each other. The vocabulary and the decision record are updated as decisions land rather than reconstructed afterwards. Procedures only a person can execute exist as runbooks rather than as knowledge in one head. And the whole arrangement is periodically reviewed against how the work actually went.

None of that depends on TypeScript.
