# skill-up-knowledge-SKILL

Shape learning development for a Solution Engineering environment using a systems approach to training. This skill governs how skill-up paths are analyzed, designed, built, delivered, and evaluated for the estate platform, in enterprise settings, for three audiences at once: corporate stakeholders, working engineers, and people new to engineering.

The method is an SE translation of the Marine Corps Systems Approach to Training (NAVMC 1553.1A): five phases (Analyze, Design, Develop, Implement, Evaluate), two-tier objectives, and the rule that gives the whole system its teeth: an objective states a behavior, a condition, and a standard, or it is not an objective.

## When to use this skill

Any time learning content is created or changed for the platform: a new skill-up path on the skill-up board, onboarding for a new SE, enablement for a new tool or board, or client-facing training as part of a solution. The skill produces paths for the skill-up board's SKILLUP_DATA block; the board renders what this skill designs.

## The five phases, SE translation

**1. Analyze.** Identify what must be performed, by whom, to what standard, before writing a word of content. In this estate the task list is not invented: it comes from the map. Products, connections, skills, and procedures define the work; the gap between what a role must do and what its people can do defines the learning requirement. Output: a task list grounded in estate artifacts, and a target population description per audience (see the three-audience rule). Never analyze from assumption; analyze from the map, the boards, and the skills, and name the gap you found.

**2. Design.** Write the objectives before the content. Two tiers:
- Terminal Learning Objective (TLO): the behavior the learner performs at the end of the path, in operational conditions.
- Enabling Learning Objectives (ELO): the prerequisite knowledge and component skills that build to the terminal behavior.

Every objective, both tiers, carries the three-part anatomy:
- Behavior: an observable action, stated with a verb that can be tested. Prefer verbs like add, produce, run, route, state, identify, apply. Avoid untestable verbs like understand, appreciate, know, be familiar with; if the draft contains one, the objective is not finished.
- Condition: what the learner is given: the running board, a map export, the decision framework, an advisory feed.
- Standard: how well, measurably. In this estate, standards already exist as governance: import-cleanly, preserve-all-fields, source-on-every-entry, no-approval-outside-the-human-path. Reuse the governing rule as the standard wherever one exists; do not write a softer parallel standard beside a hard rule.

**3. Develop.** Build the smallest set of materials that lets the learner reach the standard, choosing method and media by objective, not by habit:
- Reading a board: the board itself is the medium; link it, do not screenshot it.
- Performing a procedure: a worked loop against the real tool (the intake-import-save-export loop, an entry-skill exercise on a sample map).
- Judgment calls: the decision frameworks and worked examples, then a scenario to decide.
Materials live where the work lives: paths on the skill-up board, references as links to the boards, skills, and docs that already exist. Do not duplicate source material into training copies; a training copy of a skill file is a drift twin. Enterprise constraint: no personal study artifacts, no audio tracks, no external creative tooling in the delivered product; those are private study aids and stay local to the individual.

**4. Implement.** Delivery is the platform itself. The skill-up board is the schedule of instruction; the audience selector is the ramp; the boards and tools are the classroom. New-hire onboarding starts at the glossary index, moves through paths in dependency order (estate map before governance before security before agents before deployment), and reaches performance in the live tools under the same conditions the objectives name. Nothing is certified by attendance; reaching the standard is the only completion.

**5. Evaluate.** Two loops, matching the manual's formative and summative split:
- Formative: does the learning work? Each path is checked against its phase: are the objectives testable, do the resources actually teach the ELO they sit under, did learners reach the standard, where did they stall. Stalls are findings against the path, not the learner.
- Summative: did the estate get better? The platform already measures this: audit findings per SE, register discipline, benchmark scores against targets, intake quality. Learning that does not move an estate measure is reviewed for relevance.
Per the write/judge split (ADR-0004), whoever authors a path does not solely evaluate its effectiveness; a second reviewer or the audit function closes the loop.

## The three-audience rule

Every path is written once with three ramps, because the objective and the standard never change by audience; only the on-ramp does:
- New to engineering: assume no prior background; the glossary is the first mile; plain language before terminology, and terminology defined at first use.
- Engineer: assume fluency; point at contracts, schemas, and rules first; the shortest path to the standard.
- Corporate stakeholder: the outcome and governance view; what the standard guarantees and where the boards show it.

A path that only works for one audience is a draft. Acronyms are spelled out at first use in all three ramps.

## Hard rules

- No objective without all three parts. A missing standard is the most common defect; the fix is usually to reuse the governing rule.
- Never invent proficiency. Completion claims, assessment results, and readiness statements come from demonstrated performance against the standard, never from assertion. A path with no way to demonstrate its standard is redesigned, not certified.
- Learning content follows the same-batch rule: when a project changes, its path updates in the same batch, because a path teaching last month's tool is worse than no path.
- Enterprise-clean: no personal study material, no individual's mnemonic tooling, no generated media in the delivered product. The delivered product teaches the platform; how an individual privately studies is their own.
- Grounded like everything else: paths teach what the artifacts actually say. When a path and a skill file disagree, the skill file wins and the path is the defect.

## Output format

A path for the skill-up board is a JSON object in SKILLUP_DATA: id, kicker, name, tlo {text, behavior, condition, standard}, elos [{text, res[[label, href]]}], ramp {new, eng, stake}. Resources link to real files in the repo; a resource that does not exist is a gap to report, not a link to fabricate.
