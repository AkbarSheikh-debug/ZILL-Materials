# Lecture 1 — The vocabulary: model, harness, loop and graph

> **Lecture 1 of 6 — vocabulary**
> Opens the series. The next lecture builds the first component, the loop.

## Part A. What a harness is

> **The question:** what does a language model need around it before it can do anything at all?

## Start with what a model cannot do

Strip away the product and look at the raw thing you are paying for. A language model is a function. You send it a list of messages; it sends back one message. Then the call ends.

![A model call is a dead end: the conversation goes in, one message comes out, and nothing else happens](../assets/lecture-1/model-call.png)

Try it yourself with any chat API and no tools attached:

```python
reply = call_model([{"role": "user", "content": "Delete the temp folder and tell me when it's done."}])
print(reply["content"])
# "Done! I've deleted the temp folder for you."
```

Now look at your disk. The folder is still there. The model produced a sentence that *describes* an action. Nothing executed it, because nothing could.

Three facts follow from this, and the rest of the guide grows out of them.

| The model has… | Which means | So something else must… |
|----------------|-------------|-------------------------|
| **No memory** | Nothing carries over between calls. The second call does not know the first happened | Re-send the whole conversation, every time |
| **No hands** | It can describe opening a file. It cannot open one | Carry out each action and report the result |
| **No persistence** | It cannot wait for a build, retry after an error, or notice an hour has passed | Keep going, keep time, and recover from failure |

So when a coding agent reads forty files, runs your tests, fixes two bugs and writes a summary, the model did not do those things. It *proposed* them, one at a time. Something else carried out each proposal, reported back, and asked what to do next.

That something else is the harness.

## The definition

> A **harness** is all the code around a model that decides what the model sees, carries out what the model asks for, and decides whether to go around again.

A shorthand you will see everywhere in this field:

```text
agent = model + harness
```

The model supplies judgment. The harness supplies everything judgment needs in order to matter: eyes, hands, memory, patience and limits.

The word is well chosen. A harness on a horse does not make the horse strong; it makes the strength usable. The phrase "harness engineering" became common in 2026, after OpenAI used it as the title of an account of building a large product with coding agents, and Anthropic wrote about "effective harnesses" for long-running work. Both made the same observation: once the model is good enough, the quality of the system is decided by what surrounds it.

That is why two products built on the *same* model can feel so different. One loses the thread after twenty minutes; the other works for six hours. One overwrites your file; the other shows a three-line diff and asks. The weights are identical. The harness is not.

## One request, start to finish

Here is what actually happens when you type *"fix the failing test"* into a coding agent. Every step is harness code except the two marked **model**.

| # | What happens | Who does it | Part of the harness |
|---|--------------|-------------|---------------------|
| 1 | Build the request: system prompt, project instructions, tool list, your message | Harness | Context, memory |
| 2 | Decide the next step: "I should run the tests" | **Model** | |
| 3 | Check the command is allowed; maybe ask you | Harness | Guardrails |
| 4 | Run `pytest`, capture the output, cut it to a sane size | Harness | Tools |
| 5 | Write the call and the result to disk | Harness | Durability |
| 6 | Add the result to the conversation and call the model again | Harness | The loop |
| 7 | Decide the next step: "read `calc.py`" … and so on, for 12 turns | **Model** | |
| 8 | Notice the conversation is getting long; summarise the old part | Harness | Context |
| 9 | The model stops asking for tools. Run the tests once more to confirm | Harness | Evaluation |

Two things stand out. The model's share is small in *volume* and decisive in *direction*: it chooses what happens. And everything that makes those choices safe, affordable and recoverable is ordinary software.

## The nine parts

Every serious harness, from a 300-line script to Claude Code, answers the same nine questions. This guide spends one chapter on each.

![The nine parts of a harness drawn as rings around the model](../assets/lecture-1/harness-anatomy.png)

| # | Part | The question | Without it |
|---|------|--------------|------------|
| 1 | [The loop](01-the-loop.md) | How does a decision become an action? | The model can only talk |
| 2 | [Tools](02-tools.md) | What can it touch? | It has judgment and no hands |
| 3 | [Guardrails](03-guardrails.md) | What must it never touch? | One bad command and you lose a directory |
| 4 | [Context](04-context.md) | How does a long task fit in a finite window? | The run dies when the window fills |
| 5 | [Memory and skills](05-memory-and-skills.md) | What should outlive a session? | It relearns your project every morning |
| 6 | [Durability](06-durability.md) | What survives a crash? | A closed laptop erases two hours of work |
| 7 | [Delegation](07-delegation.md) | When should one agent hand work to another? | One window drowns in raw material |
| 8 | [Orchestration](08-orchestration.md) | How does work scale past one agent? | You are the scheduler, forever |
| 9 | [Evaluation](09-evaluation.md) | How do you know it works? | You tune by feel and ship regressions |

The order is not arbitrary. Each part only makes sense once the one inside it exists: you cannot gate tool calls before you have tools, and you cannot compact a transcript before a loop has produced one.

### How big is a harness?

The loop itself is tiny. Everything else is where the code goes.

| | A teaching harness | A production harness |
|---|--------------------|----------------------|
| The loop | ~20 lines | A few hundred lines |
| Tools | 6 functions | Dozens, plus external tool servers |
| Guardrails | A deny list and a prompt | Rule engines, OS sandboxes, hooks |
| Context | One summarisation step | Staged pruning, caching strategy, token accounting |
| Durability | Append to a file | Versioned logs, checkpoints, migrations |
| **Total** | **A few hundred lines** | **Tens or hundreds of thousands** |

The [mini harness](../examples/README.md) in this repository implements parts 1 to 7 in one readable file. Reading it alongside the chapters is the fastest way to make the ideas concrete.

## Prompt, context, harness: three crafts, nested

These words get used interchangeably. They are not the same job.

![Prompt engineering inside context engineering inside harness engineering](../assets/lecture-1/three-crafts.png)

| Craft | What you shape | A typical decision | Lifetime of the decision |
|-------|----------------|--------------------|--------------------------|
| **Prompt engineering** | One piece of text | How do I phrase this instruction? | One message |
| **Context engineering** | Everything in the window right now | Which files, which history, which tool output stays? | One turn |
| **Harness engineering** | The machinery that builds that window and acts on the reply | When do we compact? Which calls need approval? What happens after a crash? | The whole run, and across runs |

They nest. A harness *performs* context engineering automatically on every turn, and a prompt is one of the things it places in the context. Learn the outer craft and you get the inner two along the way.

A quick test of whether you have the distinction: *"the agent keeps forgetting our naming convention."* A prompt engineer rewrites the sentence. A context engineer asks whether the sentence is still in the window at turn 60. A harness engineer asks where the convention is stored, when it is loaded, and what happens to it during compaction.

## "Won't better models make this unnecessary?"

It is the most common objection, and it deserves a straight answer: the pressure runs the other way.

A stronger model attempts longer tasks, calls more tools, and holds more files in play. That puts *more* load on the machinery around it. And the failures a harness handles are not failures of intelligence.

![A perfect model surrounded by six problems it cannot solve on its own](../assets/lecture-1/outside-the-model.png)

> **The perfect-model test.** For any problem you hit, ask: *would a perfect model still have this problem?* If yes, it belongs to the harness.

Apply it:

| Problem | Would a perfect model still have it? | Belongs to |
|---------|--------------------------------------|------------|
| It chose a slow algorithm | No | The model |
| The run failed at turn 90 with a context-length error | Yes: the window is finite | Harness (context) |
| It misread an ambiguous requirement | Partly: a better spec fixes it either way | The task spec |
| Two hours of work vanished when the terminal closed | Yes | Harness (durability) |
| It ran `rm -rf` on the wrong directory | Yes: 99.9% right still fails eventually | Harness (guardrails) |
| It did not know your team's deployment rule | Yes: nobody told it | Harness (memory) |
| It said "all tests pass" without running them | Mostly: verification should not be an opinion | Harness (evaluation) |

What changes with a better model is which scaffolding you can *simplify*. Teams regularly delete workarounds after a model upgrade: fewer reminders in the prompt, fewer forced intermediate steps. They never delete the loop, the gate, or the log.

## A common trap: building the harness you imagine

It is tempting to design a grand architecture first: a planner, a memory manager, a state graph, a registry. Most of that turns out to be unnecessary, and some of it actively hurts by hiding what the model sees.

A healthier sequence:

1. Start with the loop and two or three tools. Run it on a real task.
2. Watch it fail. Read the transcript.
3. Add the smallest mechanism that prevents *that* failure.
4. Repeat.

Every chapter in this guide follows that pattern: it opens with the failure, then introduces the mechanism. If you cannot name the failure a component prevents, you probably do not need the component.

## How to read this guide

- **In order, the first time.** Chapters 1 to 6 build a single-agent harness. Chapters 7 and 8 scale it. Chapter 9 tells you whether any of it worked.
- **With the code open.** [`examples/mini_harness.py`](../examples/README.md) implements chapters 1 to 7 in one file. Each chapter ends by pointing at the functions it explains.
- **Against real systems.** The harness teardowns show how Claude Code, Codex, Pi, Hermes and DeepSeek Harness answer the same nine questions with very different trade-offs.
- **With your own failures in mind.** Each chapter ends with "check yourself" questions and one exercise. The exercises are short and worth doing.

## Check yourself

1. A model replies, "Done, I've deleted the temp folder." No harness is attached. What is the state of the temp folder, and why?
2. Classify each as a model problem or a harness problem: (a) the agent chose a slow algorithm; (b) the run failed at turn 90 with a context-length error; (c) a two-hour task was lost when the terminal closed; (d) the agent did not know the staging database must never be migrated by hand.
3. Your teammate says, "Give the model a tool that runs Python and it can do anything, so we don't need the rest." Assume the tool exists and works. What still has to exist for it to be called a *second* time?
4. Two products use the same model. One is far more reliable on long tasks. Name three places the difference could come from.

<details>
<summary>Answers</summary>

1. Untouched. The reply is text; nothing executed it.
2. (a) model. (b) harness: context. (c) harness: durability. (d) harness: memory, since nobody put the rule where the agent could read it.
3. A loop that feeds the tool's result back and calls the model again, and a rule for when to stop. One tool call is not an agent.
4. Any three of: context management, durability, tool design, instructions and memory, verification, guardrails.

</details>

## Try it

Take any chat API. Send the message *"Create a file called hello.txt containing the word hi"* with no tools. Read the reply. Then check your disk. Keep that reply in mind; the next chapter builds exactly what was missing.

**Next:** [1. The loop →](01-the-loop.md)


---

## Part B. Loops and graphs

Most people meet agents as a conversation: you type, it works, you correct it, it works some more. You are the outer loop. This page is about taking yourself out of that position without losing control.

There are three levels, and you should climb them one at a time.

![Three levels: supervised, a loop, a graph; you move from being in the loop, to on it, to designing it](../assets/lecture-1/three-levels.png)

| Level | Who drives | Structure | You are… |
|-------|-----------|-----------|----------|
| **1. Supervised** | You, turn by turn | One agent, one session | In the loop |
| **2. Loop** | A script, repeating one agent | Maker, checker, state file | On the loop |
| **3. Graph** | A script, routing between several agents | Nodes and edges | Designing the loop |

## Level 1: supervised

One agent, one human, one session. Everything in the guide applies, and for a great deal of work this is the right level. Do not leave it until you can describe, precisely, what you keep typing.

**The signal to move up:** you notice your own contribution has become mechanical. "Run the tests." "Fix that." "Now the next one." If you could write your side of the conversation in advance, a script can say it.

**The signal to stay:** you are still making judgment calls each turn. If your corrections are about *what the right thing is*, not *keep going*, the task is not ready to automate. Automating it will produce confident work in the wrong direction.

## Level 2: loop engineering

A loop is an agent run inside a `while`, with a check deciding whether to go around again.

![Maker and checker loop with a state file and four ways out](../assets/lecture-1/maker-checker.png)

It has five parts. Leave any one out and the loop misbehaves in a predictable way.

| Part | What it is | Without it |
|------|-----------|------------|
| A checkable **goal** | A condition a command can test | The loop cannot terminate |
| A **state file** | What each fresh iteration reads first and updates last | Every iteration starts from zero |
| A **maker** | The agent that does one small piece of work | Nothing happens |
| A **checker** | An independent judge | The maker declares success immediately |
| **Stop conditions** | Success, iteration cap, budget cap, no progress | An expensive overnight surprise |

### 1. A goal that can be checked

```markdown
# Goal
All functions in `src/billing/` have type hints and `mypy --strict src/billing` reports zero errors.

# Not in scope
Changing behaviour. Renaming public functions. Files outside `src/billing/`.
```

"Improve the code" cannot terminate. "Zero mypy errors in this directory" can.

| Cannot terminate | Can terminate |
|------------------|---------------|
| "Improve test coverage" | "Line coverage of `src/api/` is at least 85%, measured by `make coverage`" |
| "Clean up the codebase" | "`ruff check .` reports zero errors" |
| "Make it faster" | "`make bench` reports p95 under 200 ms" |
| "Fix the bugs" | "Every test in `tests/regressions/` passes" |

### 2. A state file

Each iteration is a fresh agent with an empty context. The state file is what it reads first and updates last:

```markdown
# Loop state
Iteration: 4 of 15
Remaining: 23 mypy errors (was 61)

## Done
- invoices.py, tax.py: fully typed

## In progress
- ledger.py: the `Entry` union is tricky; see note below

## Notes for the next iteration
- `Decimal | None` is the right type for `discount`; do not default it to 0
- Checker feedback from iteration 3: do not add `# type: ignore`; fix the type
```

The "notes for the next iteration" section is where the loop *learns*. Without it, iteration 7 makes the same mistake iteration 3 was corrected for.

### 3. A maker

The agent that does the work. Its prompt is the same every iteration:

```text
Read GOAL.md and LOOP_STATE.md. Do the next small piece of work toward the goal.
Stay in scope. Run the check yourself before you stop.
Update LOOP_STATE.md with what you did and what you learned. Then stop.
```

Small pieces matter. An iteration that tries to finish everything behaves like the [under-finishing](failure-modes.md) failure.

### 4. A checker

Something independent decides whether the goal is met. In order of preference:

| Checker | Cost | Trust | Use when |
|---------|------|-------|----------|
| **A command** (`mypy` exits 0) | Free, instant | Total | Always, if one exists |
| **A second agent with a rubric** | A model call | Good, if calibrated | No command can judge it |
| **A human**, sampled | Attention | Ground truth | The stakes are high |

If the checker is an agent, give it the artifact and the criteria, not the maker's reasoning, and require specific, actionable feedback:

```text
You are reviewing a change you did not write. Criteria:
(1) no `# type: ignore` comments were added;  (2) no function signature changed its meaning;
(3) every changed file still passes its tests.
Answer PASS or FAIL per criterion, with a file and line as evidence.
If anything fails, say exactly what to change.
```

*Missing it:* the maker declares success on iteration one. A maker reviewing itself is the [premature victory](failure-modes.md) failure with extra steps.

### 5. Stop conditions

```python
for i in range(MAX_ITERATIONS):                 # hard cap
    run_agent(MAKER_PROMPT)
    ok, feedback = check()
    if ok:
        break                                   # goal met
    if spent() > BUDGET:
        break                                   # out of money
    if no_progress_for(3):
        break                                   # stuck: same errors three times running
    append_to_state(feedback)
```

Four exits: success, iteration cap, budget cap, and *no progress*. The last one is the one people forget. A loop that makes the same failed attempt fifteen times is burning money to tell you something it could have said on the third.

Measuring progress needs a number: errors remaining, tests passing, features marked done. If the number has not improved for three iterations, stop and hand it to a person, with the state file as the report.

### What loops are good at

| Good fit | Poor fit |
|----------|----------|
| Mechanical, checkable transformations: migrations, lint classes, type annotations | Work where "better" is a matter of taste |
| A natural queue: the next ticket, file, or failing test | A single tightly coupled change |
| Iterating toward a measurable target: coverage, a benchmark | Anything where each step needs a human decision |

## Level 3: graph engineering

When one loop is not enough, several agents with different jobs are connected by code.

![A pipeline of planner, implementer and reviewer with two capped cycles and an escalation path](../assets/lecture-1/agent-graph.png)

### The rules that keep a graph maintainable

**Nodes are agent runs. Edges are code.** A node has a narrow job, its own prompt, its own tools and a fresh context. An edge is an `if` on something mechanical: an exit code, a test result, a field in a JSON file. If you find a model deciding where control goes next, ask whether a test could decide instead.

**Every node has a contract.**

| Field | Example |
|-------|---------|
| Input | `plan.md`, the issue text |
| Output | A branch with commits; `result.json` with `{ "status": "...", "summary": "..." }` |
| Tools | Read, edit, shell. No network |
| Done when | `make check` exits 0 |
| On failure | Write what blocked you to `result.json` and exit non-zero |

**State lives in files.** What passes between nodes is a plan document, a diff, a results file. Never one agent's memory of a conversation. That makes every hand-off inspectable and every node re-runnable.

**Every cycle has a cap.** Each backward edge needs a counter and an escape route to a human. An uncapped cycle between an implementer and a reviewer can run for hours, with each side politely disagreeing.

**Different context is the point.** A reviewer is useful because it has *not* seen the implementer's reasoning. Giving every node the full history defeats the purpose and multiplies the cost.

### The whole thing is a small script

A graph does not require a framework. This is the pipeline in the diagram:

```python
plan = run_node("planner", inputs=[issue], mode="read-only")
if not human_approves(plan):
    stop("plan rejected")

for attempt in range(3):                                  # capped cycle 1
    run_node("implementer", inputs=[plan, feedback], worktree=wt)
    if run("make check", cwd=wt).returncode != 0:         # an edge: an exit code
        feedback = last_test_output(wt)
        continue
    review = run_node("reviewer", inputs=[diff(wt)], mode="read-only")
    if review["status"] == "approved":                    # an edge: a JSON field
        open_pull_request(wt)
        break
    feedback = review["comments"]
else:
    escalate_to_human(wt)                                 # the exit for both cycles
```

Read the control flow: every decision is a return code, a field, or a person. No model chooses the next node.

### Common graph shapes

| Shape | When to use it |
|-------|----------------|
| **Pipeline** (plan → build → test → review) | Stages are distinct and ordered |
| **Fan-out and gather** | Many independent items; see orchestration |
| **Maker-checker cycle** | Quality needs iteration against a rubric |
| **Router** (classify, then send to a specialist) | Inputs fall into a few clearly different kinds |
| **Escalation ladder** (cheap model first, stronger on failure) | Most cases are easy and cost matters |

## Before you add a node

Graphs are seductive. A diagram with eight boxes looks like progress. Each box, though, adds cost, latency, a hand-off where detail is lost, and a new place for things to go wrong. Before adding one, answer:

1. **What specific failure does this node prevent?** Name a real run where it happened.
2. **Could a command do it instead of an agent?** A linter is cheaper than a reviewer.
3. **Could the existing node do it with a better prompt or tool?**
4. **How will I know if this node is helping?** If you cannot measure it with the methods in evaluation, you cannot justify it.

| You are about to add… | First try… |
|-----------------------|-----------|
| A "planner" node | Asking the one agent to write a plan file before coding |
| A "tester" node | Putting the test command in the instructions and a stop hook |
| A "reviewer" node | A linter for the things the reviewer keeps catching |
| A "memory manager" node | A progress file |
| A "supervisor" model | A `for` loop |

A reasonable path for most teams: one good supervised agent; then a maker loop with a mechanical checker; then a reviewer; and only then anything more elaborate.

## Sources and further reading

- Anthropic, [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents): workflows versus agents, and the common composition patterns
- Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Learn Harness Engineering](https://github.com/walkinglabs/learn-harness-engineering): its lectures on loop engineering and graph engineering cover these topics at length, with templates
