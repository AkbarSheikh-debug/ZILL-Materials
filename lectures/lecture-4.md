# Lecture 4 — Context and compaction

> **The question:** the model has a fixed-size window and the loop only ever appends to it. What goes into that window, and how do you keep a long task alive when it fills up?

Zill already has `provider.py` and `loop.py` (lecture 2) and `tools.py`, `security.py` and `operations.py` (lecture 3). Today adds **one file, `context.py`**, plus one small hook in the loop. This is arguably the most important lecture of the series, because compaction decides whether an agent can finish big jobs.

![Where we are. Your Zill repo after Lecture 3. Today one new file joins it.](../assets/lecture-4/diagrams/diagram-01.png)
***Where we are.** Your Zill repo after Lecture 3. Today one new file joins it.*

## Context engineering versus context management

Most courses stop at **context engineering**: the elements that go into the context (system prompt, tools, skills, memory files, conversation). That is the easy half.

When you design a harness, the harder half is **context management**: how the harness keeps the context alive and under control, turn after turn, while the agent works. Its most important part is **context compaction**, and it is far more than "summarise the old messages".

![Two different jobs. Context engineering fills the window. Context management kee](../assets/lecture-4/diagrams/diagram-02.png)
***Two different jobs.** Context engineering fills the window. Context management keeps it alive.*

## Context is the fuel

Using the car analogy: the LLM is the engine, the tools are the wheels, and **context is the fuel**. A tank has a fixed size and must be refilled when it runs low. Every model has a fixed context window.

![Context is the fuel. Lecture 1's picture: the LLM is the engine, tools are the w](../assets/lecture-4/diagrams/diagram-03.png)
***Context is the fuel.** Lecture 1's picture: the LLM is the engine, tools are the wheels, context is the fuel.*

### The tape only grows

The loop takes the messages array and appends the assistant's reply and every tool result. **Nothing is ever removed**, so the array only grows. We call it **the tape**, and the whole tape is sent on every call. Illustrative growth: roughly 3k tokens at turn 1, 9k at turn 5, 24k at turn 10, 51k at turn 20, and by around turn 30 of a real task it crosses the window.

Nobody wrote a bug. "Append everything, forever" is the rule that gives the agent its memory, and the same rule kills it on a long task.

![The tape only grows. Every turn appends. Nothing is ever removed. And all of it ](../assets/lecture-4/diagrams/diagram-04.png)
***The tape only grows.** Every turn appends. Nothing is ever removed. And all of it is re-sent on every call.*

---

# Part 1. What goes into the context

## The nine things in every call

| # | Item | Compacted? |
|---|------|-----------|
| 1 | **System prompt**: how the agent behaves | Never |
| 2 | **Tools**: name, label, description and parameters (the whole contract from lecture 3), every turn | Never |
| 3 | **Skills**: only each skill's *name and short description*, not the file | Never |
| 4-6 | **The messages array**: user messages, assistant messages, tool results | **Yes, the only part ever compacted** |
| 7 | **Memory**: `AGENTS.md` / `CLAUDE.md` files (long-term). The messages array is the short-term memory | Never |
| 8 | *(optional)* Self-saved memory fragments: Hermes and OpenClaw decide what mattered and write small notes to disk | Never |
| 9 | Current working directory and today's date | Never |

Everything about compaction concerns just the messages array.

![Nine things ride into every call. Everything the model sees on one turn. Only on](../assets/lecture-4/diagrams/diagram-05.png)
***Nine things ride into every call.** Everything the model sees on one turn. Only one group of them is ever compacted.*

### Three voices in the context

| Role | Meaning |
|------|---------|
| **System prompt** | The standing guideline written by the harness. Fixed: everyone who starts a Pi session gets the same text |
| **User message** | What you ask in *this* session ("migrate this code base to Rust") |
| **Assistant message** | The model's thinking, answer and tool calls. Grows every turn |

![Three voices in the context. System prompt, user message, assistant message: who](../assets/lecture-4/diagrams/diagram-06.png)
***Three voices in the context.** System prompt, user message, assistant message: who writes them, and when do they change?*

## How a real harness assembles the prompt: Pi

"System prompt" in Pi means *everything assembled and sent before the conversation*, built from five pieces and **rebuilt on every call**:

1. **Base template**: "You are an expert coding assistant operating inside pi…" plus the available-tools list. (This merges items 1 and 2 of the nine.)
2. **`appendSystemPrompt`**: any extra text glued on at the end.
3. **Project context**: every `AGENTS.md` / `CLAUDE.md` found (the memory).
4. **Available skills**: name, description and location only. This block appears **only if the read tool is present**, because the model needs `read` to open a skill.
5. **Date and working directory**, stamped last.

A `customPrompt` replaces the base template entirely, so the model's identity is not hard-coded anywhere.

![Pi builds its prompt from five pieces. buildSystemPrompt() stacks them in order.](../assets/lecture-4/diagrams/diagram-07.png)
***Pi builds its prompt from five pieces.** buildSystemPrompt() stacks them in order. The prompt is composed, not hard-coded.*

Rebuilding every time means the assembled prompt moves while the template stays constant: Monday in repo `app` with one `AGENTS.md` and three skills; Tuesday changes only the date (*date injection*); a day with the read tool switched off simply loses the skills block.

![Same template, three prompts. The template is constant. The assembly is not: dat](../assets/lecture-4/diagrams/diagram-08.png)
***Same template, three prompts.** The template is constant. The assembly is not: date, context and skills all move.*

### The `AGENTS.md` walk-up

People usually have a personal `AGENTS.md` for how they like to work, and a `CLAUDE.md` inside each project. Pi gathers both:

1. First the **global** file from Pi's own folder in your home directory.
2. Then it **walks up** from the working directory: `src/` (nothing), the repo (finds `CLAUDE.md`), its parent (nothing), and so on to the top.
3. In every folder it checks four names in order: `AGENTS.md`, `AGENTS.MD`, `CLAUDE.md`, `CLAUDE.MD`.

Final order: **global first, furthest ancestor next, the closest file last.** The closest file is the most specific, so it gets the final word if two files disagree. Files are de-duplicated by path.

![The AGENTS.md walk-up. Pi loads the global file first, then walks UP from the wo](../assets/lecture-4/diagrams/diagram-09.png)
***The AGENTS.md walk-up.** Pi loads the global file first, then walks UP from the working folder to the root.*

**Why walk again on every rebuild?** Because you can edit these files mid-session. On turn 4 the agent uses npm; you add "use pnpm, never npm" to `CLAUDE.md`; on turn 5 the prompt is rebuilt, the walk finds your edit and the agent switches. There is no limit on how many markdown files Pi collects, so too many files will confuse the model. And these files are Pi's *only* memory: it relies on you to update them, which is a design choice.

![Walk again on every rebuild. Why redo the walk each time? So an edit made mid-se](../assets/lecture-4/diagrams/diagram-10.png)
***Walk again on every rebuild.** Why redo the walk each time? So an edit made mid-session is seen on the very next turn.*

## Skills

A skill is one markdown file, `SKILL.md`. At the top is **frontmatter** with a `name` (for example `processing-pdfs`) and a `description`. Below is the **body**: the real instructions, possibly hundreds of lines.

When context is built, **only the name and description go in, every turn, for every skill.** The body loads only when the model picks that skill. Think of a movie trailer: the name and description are the trailer; the body is the film. This is **progressive disclosure**, so you must write the name and description very well, because they are all the model has to choose with.

![A skill file is a trailer. Only the top of the file sits in the context. The bod](../assets/lecture-4/diagrams/diagram-11.png)
***A skill file is a trailer.** Only the top of the file sits in the context. The body loads when the skill is picked.*

It is really three levels, and a skill is paid for in three instalments:

| Level | What | Loaded |
|-------|------|--------|
| 1 | Name and description | At startup, for every skill |
| 2 | Body of `SKILL.md` | Only when the skill is triggered |
| 3 | Bundled files (references, examples, scripts) | Only if that specific thing is needed |

A bundled file costs nothing until opened, and most of the time the model stops at the first instalment.

![Three levels of loading. A skill is paid for in three instalments, and most requ](../assets/lecture-4/diagrams/diagram-12.png)
***Three levels of loading.** A skill is paid for in three instalments, and most requests stop at the first.*

### Tool or skill?

A **tool** is *how* to do one action (read a file, run bash, grep); its full contract is in context every turn. A **skill** is *what to do and when*: a procedure like a recipe, with only its name and description in context until picked. A recipe can call for many hands, but a hand never tells you the recipe.

![Tool or skill?. A tool is HOW. A skill is WHAT to do and WHEN to do it.](../assets/lecture-4/diagrams/diagram-13.png)
***Tool or skill?.** A tool is HOW. A skill is WHAT to do and WHEN to do it.*

### A real skill

The course author's writing agent kept producing text that read as AI-written (double dashes everywhere, words like "delve"). The fix: give the agent a few chapters of the author's own book and have it produce `writing-style.md`, a skill with a name, a description and a list of rules (no double dashes, never "delve", short paragraphs, real numbers, one analogy first…). Now every run loads that skill, so the style never has to be re-explained for a blog post, landing page or book. The philosophy: **a very small harness core, with the real power in skill files.** (Hermes takes the opposite approach and ships with a lot built in.)

![A real skill: my writing style. Write the rules once. Reuse them for every book,](../assets/lecture-4/diagrams/diagram-14.png)
***A real skill: my writing style.** Write the rules once. Reuse them for every book, post and page.*

### How to write a good skill

These rules distil Anthropic's guide on authoring skills.

**1. Say less.** The model already knows what a PDF is and what React and Rust are. A good skill states what is needed in about 50 tokens; the verbose one burns 150 explaining basics. The window is shared with the system prompt, the conversation and every other skill, so writing a skill is a budgeting exercise: for every paragraph ask whether it earns its tokens.

![Say less. Assume the model already knows what a PDF is and how libraries work.](../assets/lecture-4/diagrams/diagram-15.png)
***Say less.** Assume the model already knows what a PDF is and how libraries work.*

**2. Two required fields.**

| Field | Rules |
|-------|-------|
| `name` | At most 64 characters; lowercase letters, numbers and hyphens only; must not contain "claude" or "anthropic" |
| `description` | At most 1,024 characters; not empty; says what the skill does **and when to use it** |

No XML tags in either, and both are validated, so a break stops the skill loading properly.

![The two required fields. Every skill has exactly two fields at the top, and both](../assets/lecture-4/diagrams/diagram-16.png)
***The two required fields.** Every skill has exactly two fields at the top, and both of them are checked.*

**3. The description is how a skill gets found.** Good: "Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs." Bad: "I can help you process Excel files" (write in the **third person**, never "I" or "you"), and "Helps with documents" (far too vague; with 100 skills the model cannot pick on that).

![The description is how a skill gets found. The model picks between skills on thi](../assets/lecture-4/diagrams/diagram-17.png)
***The description is how a skill gets found.** The model picks between skills on this one sentence alone.*

**4. Name skills after the activity**: processing PDFs, analysing spreadsheets, managing databases, writing documentation. Never `helper`, `utils`, `documents` or `tools`.

![Name skills after the activity. A name should say what the skill does, not that ](../assets/lecture-4/diagrams/diagram-18.png)
***Name skills after the activity.** A name should say what the skill does, not that it helps.*

**5. Match freedom to fragility.** A narrow bridge with a cliff on both sides (a database migration, something specific to your company) needs exact, low-freedom steps. An open field with many safe paths (a code review) needs high freedom: give the goal ("review for bugs and style") and let the model use judgment. **Over-specifying an open-field task makes the skill worse.**

![How much freedom to give. A narrow bridge needs exact steps. An open field needs](../assets/lecture-4/diagrams/diagram-19.png)
***How much freedom to give.** A narrow bridge needs exact steps. An open field needs only the goal.*

**6. Keep it short and split it.** Keep the `SKILL.md` body under about 500 lines; beyond that, split into separate files in the same folder. In a PDF skill, `SKILL.md` is read first; `FORMS.md`, `reference.md` and `examples.md` only when needed; and a `scripts/` folder is special because scripts are *run, not read*, so they cost no tokens. `SKILL.md` acts as a table of contents.

![One folder, loaded piece by piece. SKILL.md is a table of contents for everythin](../assets/lecture-4/diagrams/diagram-20.png)
***One folder, loaded piece by piece.** SKILL.md is a table of contents for everything beside it.*

**7. Keep references one level deep.** If `SKILL.md` links to `advanced.md` which links to `details.md`, the model may only skim the last file. Link every reference file directly from `SKILL.md` and let nothing link further.

![Keep references one level deep. Every reference file should be linked straight f](../assets/lecture-4/diagrams/diagram-21.png)
***Keep references one level deep.** Every reference file should be linked straight from SKILL.md.*

**8. Use a checklist or a loop.** For multi-step skills give a numbered checklist (analyse the form, create the field mapping, validate it, fill the form, verify the output) and tell the model to tick steps off. Or a feedback loop: make the change, run a validator, fix errors, validate again, and continue only when it passes. The skill then never moves forward without reading its own result.

![Checklist or loop. Two shapes for the body of a skill: a straight list, or a cir](../assets/lecture-4/diagrams/diagram-22.png)
***Checklist or loop.** Two shapes for the body of a skill: a straight list, or a circle that checks itself.*

**9. Write the tests before the skill.** Run the task with no skill; write down exactly what failed; build about three test scenarios from those failures; write the *smallest* skill that fixes them. The author used their writing skill for about 100 articles, ran each through an AI-detection API and set one rule: the skill is not done until the articles pass. **The human defines what "good" means**, not the model.

![Write the tests before the skill. Build the skill against real failures, not ima](../assets/lecture-4/diagrams/diagram-23.png)
***Write the tests before the skill.** Build the skill against real failures, not imagined ones.*

**10. Two sessions, one skill.** Use one session (A) to help write the skill, then open a fresh session (B) that knows nothing about how it was written, give it the skill, let it work on real tasks and have it be highly critical. Improve the skill from what B *actually did*. It is a small competition (the same idea as GANs): the writer is never done until the judge passes it.

![Two Claudes, one skill. One session writes the skill. A fresh session uses it an](../assets/lecture-4/diagrams/diagram-24.png)
***Two Claudes, one skill.** One session writes the skill. A fresh session uses it and reports what went wrong.*

## The last piece: date and folder

"Schedule this email for tomorrow at the same time": which tomorrow? The model was trained months ago and does not know today's date. "Run the tests in this project": which project? The harness must bake the date and working directory into the prompt. Many people forget this.

![The last piece: date and folder. Small, easy to forget, and the agent is lost wi](../assets/lecture-4/diagrams/diagram-25.png)
***The last piece: date and folder.** Small, easy to forget, and the agent is lost without it.*

**Part 1 in four lines:** nine things ride into every call but only the messages array is compacted; Pi rebuilds its prompt from five pieces each call; skills load progressively in three levels; and a good skill is short, well-named, tested before it is written, and checked by a second session.

---

# Part 2. Compaction: Pi versus Hermes

## Five levels of understanding compaction

"Use another LLM to summarise the past" is only level one, and in an interview it signals you have never looked inside a harness.

| Level | Question |
|-------|----------|
| 1 | Summarise the past with a model (what everyone says) |
| 2 | **When** do you start? Not at the full window; some time before. But when exactly? |
| 3 | **How much** do you keep? Past versus new: how many recent messages, and how do you decide? |
| 4 | **Where is the boundary?** The array is user, assistant, tool call, tool result, user… What if the cut lands between a tool call and its result? |
| 5 | **What if compaction itself fails?** |

Production harnesses answer all five.

!["Just summarize it" is level one. Every harness compacts. The depth is in the qu](../assets/lecture-4/diagrams/diagram-26.png)
***"Just summarize it" is level one.** Every harness compacts. The depth is in the questions that come after.*

## Where the tokens really go

In a typical context bar the system prompt is a sliver, your messages are a thin line, the model's replies a small part, and **the huge block is tool results**. You type "why is my build red?" (about 10 tokens); the agent runs a command and a 5,000-token log comes back, and that log stays on the tape and is resent every turn.

> **The context does not get full because of what we say. It gets full because of what the agent sees.** If you control tool results, you control most of your budget.

![Where the tokens actually go. A small question can trigger a giant answer, and t](../assets/lecture-4/diagrams/diagram-27.png)
***Where the tokens actually go.** A small question can trigger a giant answer, and that answer stays on the tape.*

---

## Pi's compaction

### When

Picture the whole window as a bar, with a blue arrow showing how much we carry. At the end is a red striped area Pi never lets you enter: **`reserveTokens`**, 16,384 tokens by default. The moment the arrow touches it, Pi compacts. The reason: compaction happens on the same turn the model must still answer, and if the window is already full there is no room to write the answer.

![When Pi compacts. Compaction fires when usage climbs to within 16,384 tokens of ](../assets/lecture-4/diagrams/diagram-28.png)
***When Pi compacts.** Compaction fires when usage climbs to within 16,384 tokens of the ceiling.*

### Counting tokens

The provider's reply includes a **usage block** with exact counts. Pi sums:

- **`usageTokens`**: exact, from the last reply that has a usage block.
- **`trailingTokens`**: an estimate for anything added after it (a tool result, a new user message).

![Where Pi gets the token number. Exact up to the last assistant reply. Estimated ](../assets/lecture-4/diagrams/diagram-29.png)
***Where Pi gets the token number.** Exact up to the last assistant reply. Estimated only for what came after it.*

It is not trivial: Pi walks backwards from the newest message looking for the last reply with a proper usage block. In the example (messages 21 to 28), message 28 is a user message (no usage block), message 27 is a reply from a call that broke halfway (no usage block either), and message 24 has the exact figure of 178,900 tokens. Everything after it is estimated (about 600 + 15 + 30 + 1,223…), giving roughly 180,700.

![Walking back to the last usage block. The newest entry is #28. #27 was aborted, ](../assets/lecture-4/diagrams/diagram-30.png)
***Walking back to the last usage block.** The newest entry is #28. #27 was aborted, so it has no usage. The walk stops at #24.*

How Pi estimates: normal text is **characters ÷ 4**; a tool call is the tool name plus its arguments; **every image counts as 4,800 characters**. Estimates are kept slightly **high on purpose**: compacting a bit early is harmless, compacting too late makes the whole call fail.

![How Pi estimates what it has no usage for. A rough chars-divided-by-four rule, o](../assets/lecture-4/diagrams/diagram-31.png)
***How Pi estimates what it has no usage for.** A rough chars-divided-by-four rule, only ever used for the newest messages.*

### What to keep

Pi walks backwards from the newest message, adding up tokens until it has about **20,000 tokens** (`keepRecentTokens`). That is the **cut**. Everything to its right is recent work and is kept word for word; everything to its left is summarised.

![Walking backwards to find the cut. Pi keeps about 20,000 tokens of the most rece](../assets/lecture-4/diagrams/diagram-32.png)
***Walking backwards to find the cut.** Pi keeps about 20,000 tokens of the most recent conversation, word for word.*

### Where it may cut

Everything before the cut becomes a summary, so if the fresh context started with a tool *result* whose call was summarised away, you would have a coat without a ticket, and the API rejects the whole thing. So Pi may cut at a **user message**, an **assistant message**, a bash execution, a custom entry or a branch summary, but **never at a tool result**, which must stay glued to the call that asked for it.

![Pi is not allowed to cut just anywhere. A tool result must stay attached to the ](../assets/lecture-4/diagrams/diagram-33.png)
***Pi is not allowed to cut just anywhere.** A tool result must stay attached to the tool call that asked for it.*

Pi asks two questions about each message: *can I cut here?* and *does a new turn start here?*

| Message | Can cut? | Turn starts? |
|---------|---------|--------------|
| User | Yes | Yes |
| Assistant | Yes | **No** |
| Tool result | No | No |

The assistant row is why a cut can land **in the middle of a turn**: the recent work is kept but the question that started the turn is on the old side.

![Two questions about the same message. Every turn start is a legal cut. Not every](../assets/lecture-4/diagrams/diagram-34.png)
***Two questions about the same message.** Every turn start is a legal cut. Not every legal cut starts a turn.*

### A split turn: two summaries, joined

In that case Pi makes **two summaries**: the normal one for old history (up to 80% of the reserve) and a small extra one for just the start of the turn, meaning what the user was asking (up to 50% of the reserve). They are joined into a single stored message. Two model calls, one summary, and the model never forgets what question it was answering.

![A split turn: two summaries, joined. If the cut lands inside a turn, Pi also sum](../assets/lecture-4/diagrams/diagram-35.png)
***A split turn: two summaries, joined.** If the cut lands inside a turn, Pi also summarizes the start of that turn.*

### What the summary contains

Always the same shape: **Goal; Constraints and preferences; Progress (done / in progress / blocked); Key decisions; Next steps; Critical context.** For every decision Pi also records *why*, because the next model needs the reason. The list of files read and changed is added **by code, not by the model**, so it is always correct. A fixed shape means the next model knows where to look.

![What Pi's summary always contains. A fixed shape, so the next model always knows](../assets/lecture-4/diagrams/diagram-36.png)
***What Pi's summary always contains.** A fixed shape, so the next model always knows where to look.*

### End to end

1. An hour of session entries.
2. `prepareCompaction`: take the exact number from the last reply, estimate the rest, check whether we touched the reserve.
3. `findCutPoint`: walk back collecting about 20,000 tokens; if standing on a tool result, move.
4. Summarise everything before the cut (one call, or two if the cut is mid-turn).
5. A fresh short context: summary on top, the recent 20,000 tokens untouched, and work continues.

Pi's idea in one line: **decide where to cut safely, then summarise everything before it. One clean cut, one summary, one big drop.** It all lives in one file, `compaction.ts`.

![Pi compaction, end to end. Pi decides WHERE to cut first, then summarizes everyt](../assets/lecture-4/diagrams/diagram-37.png)
***Pi compaction, end to end.** Pi decides WHERE to cut first, then summarizes everything before the cut.*

---

## Hermes's compaction

Hermes goes deeper and does almost everything differently.

### When: a percentage

Hermes takes the full window, removes the space needed for the reply (the **effective window**) and starts compacting at **50%**. Pi waits until almost full; Hermes starts at half.

![When Hermes compacts. Hermes measures its percentage against the room actually l](../assets/lecture-4/diagrams/diagram-38.png)
***When Hermes compacts.** Hermes measures its percentage against the room actually left for input.*

Three corrections handle tricky cases:

| Rule | Why |
|------|-----|
| **Floor of 64,000 tokens**: never compact below it | A small model would otherwise compact while half the window is still empty |
| Window below 512,000: raise the trigger from 50% to **75%** | |
| Window smaller than the floor (say 32,000): use **85%** | A 64k floor on a 32k window makes no sense |

This is the real work of building a harness: not the big idea but the small cases that keep it from breaking.

![Three corrections to the trigger. The rules stop a small model from compacting t](../assets/lecture-4/diagrams/diagram-39.png)
***Three corrections to the trigger.** The rules stop a small model from compacting too early, or never at all.*

### What to keep: head, middle, tail

Hermes keeps the **start** of the conversation exactly (system prompt and the first three messages) and the **end** (most recent messages). Only the **middle** is summarised. Your first messages are usually the clearest statement of your real goal; the middle is wandering. Pi keeps only the end; Hermes keeps both.

![Head, middle, tail. The beginning and the end are protected. Only the middle is ](../assets/lecture-4/diagrams/diagram-40.png)
***Head, middle, tail.** The beginning and the end are protected. Only the middle is summarized.*

### Step one is free

Before summarising anything, Hermes **shrinks old tool results** (remember picture 27): a giant test log becomes one line like "Ran `npm test`, exit …". If the agent read the same file five times, only the latest copy stays; old images are dropped. This is plain code and uses **no model**, so most of the space is freed before any model call.

![Step one is free. Old tool results become one line each, before any model is cal](../assets/lecture-4/diagrams/diagram-41.png)
***Step one is free.** Old tool results become one line each, before any model is called.*

### What its summary contains

Eleven sections: Historical task snapshot, Goal, Constraints and preferences, Completed actions, Active state, Blocked, Key decisions, Resolved questions, Relevant files, Critical context, and Pruned skills. It remembers not only what you decided but where the work is *right now*. And: **never write an API key into the summary; write `REDACTED`.**

![What Hermes's summary always contains. Eleven fixed sections, including the exac](../assets/lecture-4/diagrams/diagram-42.png)
***What Hermes's summary always contains.** Eleven fixed sections, including the exact state of the working directory.*

### End to end

Shrink old tool results (free) → keep the start (free) → keep the end (free) → summarise the middle (the only step that costs money) → next time, build on the previous summary instead of starting from scratch. **Four cheap steps around one expensive one.**

![Hermes compaction, end to end. Four cheap steps surround one expensive one.](../assets/lecture-4/diagrams/diagram-43.png)
***Hermes compaction, end to end.** Four cheap steps surround one expensive one.*

### Micro-compaction

Pi waits until full, then drops everything at once. **Micro-compaction** works bit by bit: after *every* turn Hermes folds that one exchange (your message, the reply, the tool result) into a **running summary**, with a bookmark that moves forward one step each turn. When the window finally fills there is nothing big to do, because the summary is already ready. In Hermes it is **off by default**.

![Micro-compaction. After every turn, Hermes folds ONE more exchange into a rollin](../assets/lecture-4/diagrams/diagram-44.png)
***Micro-compaction.** After every turn, Hermes folds ONE more exchange into a rolling summary.*

Drawn as context size over time, Pi is the teeth of a saw (up, up, up, sudden drop) while micro-compaction stays almost flat with many tiny steps. Same total work, spread differently, but it costs cache (see below).

![Two rhythms. The same total work, spread differently across the session.](../assets/lecture-4/diagrams/diagram-45.png)
***Two rhythms.** The same total work, spread differently across the session.*

### When compaction itself fails

Hermes has four guards:

| Guard | Behaviour |
|-------|-----------|
| **Floor** | The system prompt and tool definitions can never be summarised; if they alone nearly fill the window, Hermes knows |
| **Two strikes** | If one compaction is still too big it tries again; after two tries without help it stops. No endless retries |
| **Cooldown** | If the summary model says "too many requests", wait ten minutes and try again |
| **Fallback** | Summary model unavailable → try a backup model → the main model → and if nothing works (say the API bill is unpaid) make a basic summary with plain code, no model at all |

> **Compaction is allowed to fail. It is never allowed to get stuck in a loop.**

![When compaction itself fails. Four independent guards, for four different failur](../assets/lecture-4/diagrams/diagram-46.png)
***When compaction itself fails.** Four independent guards, for four different failures.*

---

## Pi versus Hermes

**When:** Pi keeps a fixed reserve (16,384 tokens); Hermes uses a percentage (50, 75 or 85 depending on the model).

![Pi vs Hermes: WHEN. Pi reserves a constant. Hermes reserves a proportion.](../assets/lecture-4/diagrams/diagram-47.png)
***Pi vs Hermes: WHEN.** Pi reserves a constant. Hermes reserves a proportion.*

**Where to cut:** Pi finds a safe place first, never on a tool result, then cuts there. Hermes cuts by size first, then nudges the cut until it is safe.

![Pi vs Hermes: WHERE. Pi picks a safe boundary. Hermes repairs the boundary it to](../assets/lecture-4/diagrams/diagram-48.png)
***Pi vs Hermes: WHERE.** Pi picks a safe boundary. Hermes repairs the boundary it took.*

**Summary shape:** Pi has six sections plus a file list; Hermes has eleven. Both keep key decisions; Hermes also keeps exactly where the work stands. Every harness has its own shape; Claude Code has one too.

![Two shapes of summary. Both keep the decisions. Hermes also keeps the working st](../assets/lecture-4/diagrams/diagram-49.png)
***Two shapes of summary.** Both keep the decisions. Hermes also keeps the working state.*

| | Pi | Hermes |
|---|---|---|
| When | Almost full (fixed reserve) | At half (percentage) |
| Keeps | The last ~20,000 tokens | The start *and* the end |
| Summary | 6 sections | 11 sections |
| Free step | None | Shrinks old tool results first |
| Failure | Tries again | Floor, two strikes, cooldown, fallback |

Same problem, two completely different answers. Users never see compaction happen; it just has to work, and Hermes thought about every way it could break.

![Pi vs Hermes: the scorecard. Same problem, two very different designs.](../assets/lecture-4/diagrams/diagram-50.png)
***Pi vs Hermes: the scorecard.** Same problem, two very different designs.*

---

# Part 3. DeepSeek Harness, and the cache

## Compaction as a plugin

In Pi and Hermes compaction is built into the main code. DeepSeek Harness keeps its main loop small and leaves a **socket** that compaction plugs into from outside: one package does the compaction, an optional one shrinks big tool results first (the same idea as Hermes), and another handles the rest. Do not like how it summarises? Swap the plugin and never touch the loop.

![DeepSeek Harness: compaction is a plugin. DeepSeek's open-source harness keeps t](../assets/lecture-4/diagrams/diagram-51.png)
***DeepSeek Harness: compaction is a plugin.** DeepSeek's open-source harness keeps the loop tiny. Compaction plugs in from outside.*

### The log never forgets

The **session log** is append-only: everything that happens is added and nothing is removed, and even the compaction is written into the log (start, summary, end). What the model sees is *built from* the log: old messages are hidden behind one summary and recent ones stay as they are. The model sees a short version but you still have everything; the exact old text is always in the log.

![The log never forgets. An append-only session log. Compaction changes only what ](../assets/lecture-4/diagrams/diagram-52.png)
***The log never forgets.** An append-only session log. Compaction changes only what the model SEES.*

### When it compacts

It has **two limits, and whichever is hit first triggers**: 80% of the window, or the window minus the reply space minus an extra 65,000. After compacting it keeps the newest **16%** exactly.

| Model | 80% rule | Other rule | Winner |
|-------|---------|-----------|--------|
| 200,000-token | 160,000 | ≈102,000 | The fixed-space rule |
| 1,000,000-token | 800,000 | ≈900,000 | The percentage rule |

Small models are governed by fixed space, big ones by percentage: both ideas combined.

![When DeepSeek Harness compacts. Two limits, and whichever bites first wins. Then](../assets/lecture-4/diagrams/diagram-53.png)
***When DeepSeek Harness compacts.** Two limits, and whichever bites first wins. Then the newest 16% is kept word for word.*

### End to end

It starts one of two ways: the normal check before every call, or after the API already said "too long". Then: if the shrinking plugin is installed, shrink tool results (free); check whether it fits now and **stop if so (saving a whole model call)**; if not, make one summary call, **re-sending the same system prompt and tools to keep the cache warm**; if the API still said "too long", shrink harder and try once more; if the summary fails entirely, write a warning and carry on, never crash.

![DeepSeek Harness compaction, end to end. Two triggers share one pipeline: pressu](../assets/lecture-4/diagrams/diagram-54.png)
***DeepSeek Harness compaction, end to end.** Two triggers share one pipeline: pressure BEFORE the call, overflow AFTER a failed one.*

### Its summary

Eight sections: Primary request and intent, Key technical concepts, Files and code, Errors and fixes, Pending jobs, Current work, Next step, Critical context. The model is told it is a *checkpoint, just continue, don't talk about it*, so it does not stop to say "thanks for the summary". Only the summary text is kept (no reasoning, no tool calls), and it is honest about limits: it cannot shrink the system prompt, the tools or one giant tool call. So Pi has six sections, Hermes eleven, DeepSeek eight.

![DeepSeek's summary shape. Eight fixed sections, then wrapped so the model treats](../assets/lecture-4/diagrams/diagram-55.png)
***DeepSeek's summary shape.** Eight fixed sections, then wrapped so the model treats it as a checkpoint.*

### Three harnesses side by side

Three harnesses, the same five questions, three different answers. There is no one right answer, only trade-offs; pick what matters for your product.

![Three harnesses, side by side. The same five questions. Three different answers.](../assets/lecture-4/diagrams/diagram-56.png)
***Three harnesses, side by side.** The same five questions. Three different answers.*

### Context management inside the model

Management is also trained into the model. In the DeepSeek V3.2 paper, while tool results keep coming in the model **keeps all its thinking** and reasons across many tool calls; the moment the user sends a *new message* the old thinking is thrown away (tool calls and results stay). For its search agents, when the context fills they tried something simple: discard all old tool history and keep only the original question, which worked surprisingly well.

![Inside the DeepSeek model. DeepSeek-V3.2's rule for its own thinking during tool](../assets/lecture-4/diagrams/diagram-57.png)
***Inside the DeepSeek model.** DeepSeek-V3.2's rule for its own thinking during tool use.*

## Prompt caching

Every turn the loop resends everything (system prompt, tools, old messages) just to add one message. Call 1: everything is new. Call 2: the starting part is the same. Call 3: that shared part is longer. The *model* remembers nothing, but the **provider** can save the work it already did for the same starting part. That is the **cache**, and a mark called **`cache_control`** tells it "cache up to here".

Why it saves money: inference has two steps, **prefill** (heavy work computing key and value vectors for every input token) and **decode**. With a cache hit you skip prefill for the shared part, so you **pay less** and the answer **starts faster** (**time to first token, TTFT**). **TTL** (time to live) is how long the provider keeps the cache, perhaps five minutes or an hour; Pi supports the one-hour option.

![Prompt caching. Every turn re-sends the same beginning. The provider can keep th](../assets/lecture-4/diagrams/diagram-58.png)
***Prompt caching.** Every turn re-sends the same beginning. The provider can keep the work it already did.*

### Every fold breaks the cache once

Before compaction the system prompt, tools and long history are cached and only the new message is fresh. After compaction the system prompt and tools are still cached (they did not change), but the **summary is brand new and the recent messages moved**, so they must be computed again. **Every compaction loses the cache once.** Two rules follow:

1. **Keep the system prompt and tools identical and at the very start**, so they stay cached however often you compact. (That is why DeepSeek resends them.)
2. Compacting every turn, as micro-compaction does, **loses the cache every turn**. That is the price of the flat line.

![Every fold breaks the cache once. Compaction rewrites history, so everything aft](../assets/lecture-4/diagrams/diagram-59.png)
***Every fold breaks the cache once.** Compaction rewrites history, so everything after the fixed prefix must be computed again.*

---

# Part 4. Compaction in Zill

Pi and Hermes spend thousands of lines on this, much of it to support many models. Zill keeps the main idea.

## Zill's fold: one fold, two halves

When the tape gets too big:

- **Keep the last six messages exactly** (`KEEP_RECENT = 6`).
- Send **everything older to the model once** and ask for one summary.
- The new tape is **one summary plus the last six messages**.
- Count tokens with Pi's trick: **characters ÷ 4**.
- It borrows three ideas from today: (1) from Hermes, **always copy the original request word for word into the summary**, so your real goal survives any number of compactions; (2) also from Hermes, **cut big tool results short** before they go to the summariser; (3) like Pi and Hermes, a summary with **the same sections every time** (goal, progress, decisions, files, errors, next steps).
- If the summariser breaks, it degrades to a plain-code fallback summary instead of crashing, and it never mutates the original list.

![Zill's fold: one fold, two halves. The simplest compaction that works. Old half ](../assets/lecture-4/diagrams/diagram-60.png)
***Zill's fold: one fold, two halves.** The simplest compaction that works. Old half becomes one summary; the last 6 stay exact.*

### The seam

A simple version has the same problem as Pi: the cut can fall between `write four.txt` (the call) and `Wrote four.txt` (the result). After compaction the first kept message is that result, but its call was summarised: an **orphan**, a coat without a ticket, and the API rejects it. The fix is one line: **if the kept part starts with a tool result, drop it.** We do not invent a fake call to match, which would lie to the agent; dropping is safe because the summary already says what happened.

![The seam. Where the summary meets the kept slice. A cut can leave an orphan tool](../assets/lecture-4/diagrams/diagram-61.png)
***The seam.** Where the summary meets the kept slice. A cut can leave an orphan tool result there.*

## What we build

![What we build today. One new file, one tiny socket in the loop, a test file and ](../assets/lecture-4/diagrams/diagram-63.png)
***What we build today.** One new file, one tiny socket in the loop, a test file and a demo.*

- **`context.py`** (new file): a function to count tokens, one to turn old messages into plain text, the compaction itself, the orphan fix, and the hook plumbing.
- **A small loop change:** a hook, **`before_turn`**. Before each model call the loop hands the messages to this function and uses whatever comes back. That is how compaction plugs in.
- **Tests with a fake model** (no internet) and a **demo with a tiny 1,500-token budget**, too small on purpose so you can watch compaction happen.

The prompt is [here](../prompts/lecture-4-build-prompt.md). Three things to notice in it:

1. It says *today we add one file and one hook, nothing else*: small changes mean you can read and check every line.
2. It sets hard rules: **never change the original list**, and **if it is still too big after compacting, return it anyway and never loop** (straight from Hermes: compaction can fail but must never get stuck). It also caps the summary at **250 words**, because the summary rides along with every later call and a huge one wastes the space you wanted to save.
3. It defines **done**: tests pass; the demo compacts and prints PASS; with a big budget it does not compact and still passes; and the agent must say honestly what it could not check.

### Running the demo

![The sawtooth. Without compaction the tape hits the ceiling. With it, the tape sa](../assets/lecture-4/diagrams/diagram-62.png)
***The sawtooth.** Without compaction the tape hits the ceiling. With it, the tape saws safely under budget.*

`python demos/context_demo.py` shows the token count growing (a few hundred, 900, 1,300, 1,600…), then **"Compacted."** and a drop. It keeps going (`four.txt`, `five.txt`, the manifest) and ends with **PASS**: the task does not notice its history was squeezed. This is the sawtooth: up, drop, up, drop. The printed summary is a handover note: the original request word for word, the files made so far, the decisions and what is still left to do.

`python demos/context_demo.py 100000` uses a big budget: it never compacts and still passes. Compaction does not change what the agent does; it lets the agent keep working long after it would have run out of space.

## The three questions (and homework)

![Three decisions you must make. Designing your own harness? Compaction comes down](../assets/lecture-4/diagrams/diagram-64.png)
***Three decisions you must make.** Designing your own harness? Compaction comes down to these.*

If you build your own harness, compaction comes down to three questions, plus one for real users:

1. **When** do I compact? A fixed reserve (Pi), a percentage (Hermes), or both (DeepSeek)?
2. **How** do I compact? What exactly do I keep, where do I cut, what can I shrink for free?
3. **What does my summary look like?** What must always be in it?
4. *For real users:* **what happens when compaction itself fails?**

**Homework**

1. Run the demo with a small budget and read the summary Zill writes. Find one important thing it forgot, then change the summary instruction so it does not forget it again.
2. Change `KEEP_RECENT` from 6 to 2, then 12, and change the budget. Watch how often it compacts and whether the task still passes.
3. Codex does compaction its own way and it is public. Read it and ask the same questions: when, how, what, and what if it fails.

## Summary

- Nine things go into every call, but **only the messages array is compacted**.
- Context fills up because of **what the agent sees** (tool results), not what we say.
- Skills use **progressive disclosure**: trailer first, film only if picked.
- Compaction is five questions: *how, when, how much to keep, where to cut, what if it fails*.
- Pi uses a fixed reserve and a safe cut; Hermes uses a percentage, keeps head and tail, shrinks tool results for free and guards against failure; DeepSeek makes it a plugin over an append-only log.
- **Every compaction breaks the cache once**, so keep the system prompt and tools stable.
- Zill's version: keep the last six messages, summarise the rest, copy the original request, drop an orphaned tool result.
