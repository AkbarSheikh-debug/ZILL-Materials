# Lecture 2 — The loop (building Zill, part 1)

> **The question:** what is the smallest thing that turns a language model into an agent?
>
> **The answer:** a loop of about ten lines, wrapped around a function that has no memory.

Lecture 1 gave the vocabulary: prompt, context, harness, loop and graph engineering. This lecture opens the harness and builds its first component. It also names the project: the harness we build across this series is called **Zill**.

## Which "loop" is this?

Lecture 1 mentioned loop engineering. That is the *bigger* loop, which sits outside the agent and decides when to run it again. This lecture is about a much smaller loop that lives *inside* the harness: the model thinks, takes an action, looks at the result, then thinks again. It is called the **ReAct loop** (reasoning and acting) or simply the **agent loop**. In this series "loop" means that inner loop, and "agentic harness" and "harness" are used interchangeably.

---

## 1. The five elements of a harness

Every agentic harness is built from the same five layers, and each layer answers one question. Stack them like a pyramid with the loop at the bottom:

| Layer | The question it answers |
|-------|-------------------------|
| **Orchestration** | How do multiple agents work together? |
| **Durability** | If something crashes in between, what survives? |
| **Context and memory** | What does the model actually get to see? |
| **Tools** | What is the agent allowed to touch? |
| **Loop** | How does a thought become an action? |

![The five elements of a harness. Each layer answers one question; the series buil](../assets/lecture-2/hand-drawn/diagram-01.png)
***The five elements of a harness.** Each layer answers one question; the series builds one layer per lecture.*

Why start with the loop? Break any element down far enough, whether gold, silver or lead, and you reach a single atom. Break a harness down far enough and you reach the loop. It is the atom, the heartbeat. Without it there is no harness.

## 2. The design bet: a small harness and detailed skills

Production harnesses are huge, tens of thousands of lines, because they support many providers, many platforms and many edge cases. Zill bets differently: **keep the engine tiny (around a thousand lines of Python) and put the human knowledge into detailed skill files.** How the front end should be built, which design system to follow, how testing works: all of that is written once in skills. Small harness, very detailed skills.

![Small harness, detailed skills. The bet behind Zill: keep the engine tiny and pu](../assets/lecture-2/hand-drawn/diagram-02.png)
***Small harness, detailed skills.** The bet behind Zill: keep the engine tiny and put your knowledge into skill files.*

## 3. Why build your own at all?

Two reasons:

1. **It removes the magic.** Daily use of a coding agent makes it feel magical, and magic breeds dependence. The "magic" is about ten lines of code. After seeing that, you stop looking at these tools as a user and start looking at them as an engineer.
2. **Independence.** If you understand the harness, you are not locked into one company, model or price. If a tool becomes expensive, you connect your own harness to another model and carry on.

---

## 4. A model on its own cannot do anything

A language model cannot open a file, run a command, remember yesterday or check its own work. It is a **function**: a list of messages goes in, one message comes out, and then it stops.

Ask a bare model to "delete this file" and it will write *"Okay, I will delete the file."* The file is still there. It is only text.

Picture a genius locked in a windowless room with a gap under the door. You slide a note in, the genius writes a brilliant reply and slides it back. The genius can say "open the test file, the bug is on line twelve", but cannot leave the room to do it. Someone outside has to. **That someone is the harness.**

![The model is a function. Messages in, one message out, then it stops.](../assets/lecture-2/hand-drawn/diagram-03.png)
***The model is a function.** Messages in, one message out, then it stops.*

## 5. What a harness is

The harness is everything around the model, and it does three jobs:

| Job | What it means |
|-----|---------------|
| **Assemble** | Build what the model will see: the note that goes under the door |
| **Execute** | Do what the model asks: open the file, run the command, call the API. The harness is the hands |
| **Repeat** | Take the result back to the model and ask "what next?" |

The model supplies judgment. The harness supplies hands, memory and persistence. The name fits: the harness on a horse does not make the horse strong, it makes its strength usable.

![The harness around the model. Assemble, execute, repeat.](../assets/lecture-2/hand-drawn/diagram-04.png)
***The harness around the model.** Assemble, execute, repeat.*

**Will better models make harnesses unnecessary?** No, the opposite. A stronger model asks for more actions, works on longer tasks and touches more files, so the load on the harness goes up. A crashed laptop, a full context window and a dangerous command are not model problems, and no better model fixes them.

---

## 6. The heartbeat: thought, action, observation

The model and harness talk in a cycle of three steps:

1. **Thought:** the model looks at the situation and decides what to do.
2. **Action:** the model asks for a tool and the harness runs it.
3. **Observation:** the tool's output goes back to the model.

Then it goes around again. This is the **ReAct** loop (from the 2022 paper *ReAct: Synergizing Reasoning and Acting in Language Models*, Yao et al.). It has nothing to do with the React web framework.

![The ReAct triangle. Thought, action, observation, round and round.](../assets/lecture-2/hand-drawn/diagram-05.png)
***The ReAct triangle.** Thought, action, observation, round and round.*

### One task, six laps

Task: "There is an issue in my GitHub repository. Please fix it."

| Lap | Thought | Action | Observation |
|-----|---------|--------|-------------|
| 1 | I need to look at the issue | GitHub tool: fetch the issue | The issue text |
| 2 | Now read the code | read tool | The file contents |
| 3 | Found the bug, fix it | edit tool | File edited |
| 4 | Did the fix work? | run the tests | All tests pass |
| 5 | Open a pull request | GitHub tool | Pull request created |
| 6 | Nothing left to do | *none* | The final answer; the loop ends |

![One task, six laps. Nobody wrote "step 1, 2, 3": at each step the model chose th](../assets/lecture-2/hand-drawn/diagram-06.png)
***One task, six laps.** Nobody wrote "step 1, 2, 3": at each step the model chose the next move from what it had just seen, and it decided when it was done.*

Mistakes often come from the action step. Give the model five hundred tools it does not need and it gets confused about which to pick; lecture 3 returns to this. Next time a coding agent says "reading file… editing… running tests…", this loop is what you are watching.

---

## 7. The model has no memory: the messages array

> If you take one idea from this lecture, take this one: **the model does not remember anything.**

Every call starts completely fresh. It does not recall your previous question, the file it read ten seconds ago or its own plan. Chat feels continuous only because *someone else* does the remembering.

Imagine a brilliant colleague who forgets everything every few seconds. The only way to work with them is to keep a diary and read the *entire* diary aloud before every question, then write their answer into it. That diary is the **messages array**. It is just a list.

- Call 1 sends the system prompt and the user question.
- The model replies "let me read the test file"; the harness runs the tool, and both the request and the result are appended.
- Call 2 sends the whole list again. Call 3 sends it again, longer.

![The growing array. The memory is the list, and the harness resends it on every c](../assets/lecture-2/hand-drawn/diagram-07.png)
***The growing array.** The memory is the list, and the harness resends it on every call.*

Consequences:

- Append something and the agent remembers it. Delete something and it forgets.
- Later features, such as memory, compaction and resuming a session, are all careful editing of this one list.
- To see what the agent knows on turn 40, **print the list**. That is everything it knows.

### Three roles

Each message has a **role** (who is speaking) and **content** (what was said). There are only three roles:

| Role | Meaning |
|------|---------|
| `system` | Standing instructions: who the agent is, its tools, how to behave. Written once, at the top |
| `user` | Anything coming from outside |
| `assistant` | The model's own voice: its text and the tools it asks for |

When a tool returns a file's contents, that result reaches the model through the same door as a user message. The model has one mouth (assistant) and one ear (everything else), and the ear cannot tell a person from a program. Zill's own code tags these messages `tool` for readability, but the idea is unchanged: the outside world is talking to the model.

![Three voices. System, user and assistant; tool results come in through the ear l](../assets/lecture-2/hand-drawn/diagram-08.png)
***Three voices.** System, user and assistant; tool results come in through the ear like any outside input.*

---

## 8. Turns, and the tax you pay

One **turn** is one call to the model plus the tool work that comes out of it: call, act, append. A simple question may take one turn; "fix the failing test" may take six.

The cost is the catch. The array is never empty, even at time zero: system prompt, tool list, skill files and `CLAUDE.md`/`AGENTS.md` memory are already in it. Turn 2 sends all of that again plus turn 1. By turn 40 you are paying to re-read turns 1 to 39. The new work each turn stays about the same size; the re-read part keeps growing.

![The bars climbing. New work per turn stays small; the re-read tax grows every tu](../assets/lecture-2/hand-drawn/diagram-09.png)
***The bars climbing.** New work per turn stays small; the re-read tax grows every turn.*

So an agent reads far more than it writes. That is why context must be built carefully: five hundred "just in case" tools only confuse the model, and pasting a 40,000-line log when the last 200 lines would do means paying for it on every later turn. (Lecture 4 is entirely about this.)

## 9. How a tool call finds its result

A tool request is a small structured object: the tool **name**, its **arguments** (which file) and an **id**. The id works like the token at a restaurant counter: "order A-17" goes in, and the result comes back stamped A-17, so it reaches the right request.

![The ticket. Every request carries an id, and its result carries the same id.](../assets/lecture-2/hand-drawn/diagram-10.png)
***The ticket.** Every request carries an id, and its result carries the same id.*

Two rules follow:

1. **Every request gets exactly one result.** Three tools requested means three results returned. A request left unanswered breaks the list and the next model call fails.
2. **One turn can contain several requests.** Models often ask for three files at once, so the loop must answer every one.

Rule 1 returns in the durability lecture: some of the worst bugs come from a crash *after* the request was saved but *before* its result was.

---

## 10. The loop, derived

We are not designing the loop; we are forced into it one step at a time:

1. Call the model with the messages.
2. Check the reply: any tool calls? If not, the text is the final answer and we stop.
3. Otherwise run each tool. This is the action.
4. Append each result to the messages, so the model will see what it has not seen yet.
5. Go back to step 1.

**Nobody designed this loop: it is forced by what the model cannot do.** It cannot act, so we act for it. Acting teaches us something the model does not know, so we show it. Showing it puts us back at step 1.

![The loop, derived. Call, check, run, append, repeat, with max turns as the safet](../assets/lecture-2/hand-drawn/diagram-11.png)
***The loop, derived.** Call, check, run, append, repeat, with max turns as the safety brake.*

### The loop in about ten lines

![The code. About ten lines.](../assets/lecture-2/hand-drawn/diagram-12.png)
***The code.** About ten lines.*

```python
def run_loop(messages, tools, max_turns):
    for _ in range(max_turns):
        reply = call_model(messages)            # the thought
        messages.append(reply)                  # remember it
        if not reply.tool_calls:                # no tools asked: we are done
            return reply.text
        for call in reply.tool_calls:
            result = tools[call.name](**call.args)       # the action
            messages.append(tool_result(call.id, result))  # the observation
    # out of turns: ask for a wrap-up with no tools, so there is always a report
```

This is the heartbeat of every coding agent. Tools, permissions, memory and sub-agents are all built around these lines. Agents do not work because of deep magic inside the model; they work because of a loop *around* a function that has no memory.

## 11. Who decides when it is done?

There are two ways to make a model do a multi-step task:

| | **Workflow** | **Agent** |
|---|---|---|
| Shape | Plan, step 1, step 2, step 3, done | A loop with the model at the wheel |
| Who wrote the steps | You, beforehand | Nobody; each lap the model chooses |
| Number of steps | Fixed | Depends on the task: two laps or fifteen |
| Breaks when | The task is unpredictable | It gets stuck and never says "done" |

![Workflow versus agent. The exit condition moves out of your code and into the mo](../assets/lecture-2/hand-drawn/diagram-13.png)
***Workflow versus agent.** The exit condition moves out of your code and into the model: inversion of control.*

The shift is **inversion of control**: in a workflow *you* decide when it is done; in an agent the *model* does. That is why an agent can handle open-ended work you could never script in advance.

Handing over the wheel deserves caution, so the loop keeps two safeguards:

- **Max turns.** A plain counter. At the limit we do not crash: we make one last call *without tools*, tell the model "you have run out of turns, summarise where things are", and return that. **Never end a run without a report.**
- **Errors become results.** If a tool fails, do not crash the loop. Put the error text in the result and give it to the model. Often it reads the error and fixes the problem itself.

## 12. A skill is not a tool

| | Tool | Skill |
|---|---|---|
| Is | Code: a function the harness runs | A document in plain language |
| Does | One specific thing: read a file, run a command | Explains how to do a job, step by step |
| Kitchen analogy | The knife | The recipe |

A skill may mention tools ("use the Figma tool for this"), but it is not one. A skill's text is added to the messages array as part of what the model sees, so you change behaviour by changing instructions and never touch the harness. That is why the system is so modular.

![Skill versus tool. The tool is the knife; the skill is the recipe.](../assets/lecture-2/hand-drawn/diagram-14.png)
***Skill versus tool.** The tool is the knife; the skill is the recipe.*

---

## 13. The bare harness: three pieces

The simplest harness has just three pieces and a loop connecting them:

| Piece | Role |
|-------|------|
| **Model client** | Sends the messages, returns a reply; the only piece that talks to the model company |
| **Message array** | System, user, assistant, tool messages. It *is* the agent's state; nothing is hidden elsewhere |
| **Tools** | Each is a name, a schema describing its arguments, and a function (a read-file tool is two or three lines of Python) |

**client + message array + tools, spun in a loop = an agent.**

![Three pieces of a bare harness. The loop connects the client, the array and the ](../assets/lecture-2/hand-drawn/diagram-15.png)
***Three pieces of a bare harness.** The loop connects the client, the array and the tools.*

## 14. The provider: one doorway to the model

In Zill the model client is one file, `provider.py`. It does four jobs:

1. **Authenticates:** holds the API key.
2. **Translates:** Zill uses one neutral message format internally; the provider converts to and from each vendor's wire format.
3. **Retries:** waits and tries again on rate limits and network failures (HTTP 429, 500, 502, 503, timeouts) with exponential backoff.
4. **Normalises:** whatever comes back becomes one clean shape: text, maybe tool calls, and token counts.

Because all vendor quirks stay in this one file, moving from Gemini to another model or to OpenRouter means changing only `provider.py`. The loop never notices.

![provider.py. One door; every vendor's peculiarities stay at the door.](../assets/lecture-2/hand-drawn/diagram-16.png)
***provider.py.** One door; every vendor's peculiarities stay at the door.*

Zill's neutral message format:

```python
{"role": "user", "text": ...}
{"role": "assistant", "text": ..., "tool_calls": [...]}
{"role": "tool", "name": ..., "text": ...}
```

---

## 15. Build it

Today's build is two files plus a tiny demo:

- [`provider.py`](../code/zill-harness/zill/provider.py): the door.
- [`loop.py`](../code/zill-harness/zill/loop.py): the heartbeat.
- [`demos/day1_dice.py`](../code/zill-harness/demos/day1_dice.py): a silly dice-roller tool, so the full cycle runs without touching real files.

![What we build today. `provider.py`, `loop.py` and the dice demo.](../assets/lecture-2/hand-drawn/diagram-17.png)
***What we build today.** `provider.py`, `loop.py` and the dice demo.*

The code is not typed by hand. You write a careful prompt and give it to a coding agent. Have ready:

- An API key for a good model (a free Gemini key is fine to start). Put it in a `.env` file and tell the prompt where the file is. **Never paste the key into the prompt.**
- A name for your harness. This series uses **Zill**; use your own if you like.

The full prompt is in [prompts/lecture-2-build-prompt.md](../prompts/lecture-2-build-prompt.md). What makes it good:

- It gives **size targets** (provider about 100 lines, loop about 65) so the harness stays minimal.
- It forbids third-party packages.
- It says what **done** looks like: *verify before finishing*.

### What to expect when it runs

- **The dice demo prints four messages in order:** the user request, the model asking for the dice tool, the tool result, the model's final answer. That is one complete heartbeat on your own code.
- **"Build a landing page for a coffee shop" returns only a description.** It cannot create a single file, because it has judgment but no hands. A dice roller is not a toolbox. That gap is what lecture 3 closes.

---

## Homework

1. Print the messages array after every turn and watch it grow. Then comment out the line that appends tool results and see the error. Breaking it yourself shows that the array *is* the state.
2. Print the turn number, input tokens and output tokens after each turn. Run a small, a medium and a hard task and tabulate the numbers. Note how much larger input is than output. Keep the table for lecture 4.
3. Set max turns to 1 for a task that needs a tool and see how the run ends.

## Summary

- A model alone is a function: messages in, one message out. It is a genius locked in a room.
- The **harness** is everything around it: the hands, the memory and the persistence.
- The model has **no memory**. The memory is one list, resent on every call, so append to remember and delete to forget.
- The heartbeat of every agent is a **loop of about ten lines**: thought, action, observation.
- In an agent **the model decides when it is done**; max turns and error-as-result keep that safe.
- A bare harness is **client + message array + tools in a loop**, and today Zill got its heartbeat. Next: hands.
