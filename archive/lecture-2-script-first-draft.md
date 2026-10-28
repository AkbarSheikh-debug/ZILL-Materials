# Harness Engineering Series — Lecture 2: The Loop (Building Zill, Part 1)

**Speaking script.** Lecture 1 covered prompt, context, harness, loop and graph engineering. This lecture opens the harness and builds its first component.
Read the normal text aloud, word for word. Lines in `[brackets]` are cues for you and are not spoken.
Diagrams: `diagram-01.png` … `diagram-17.png` (1920×1080), in two styles — `diagrams/` (hand-drawn) and `diagrams-pro/` (clean). Same numbers in both.

Rough length: 25–30 minutes of speaking, plus the live build.

---

# PART A — Opening the harness

## 1. Welcome to Lecture 2 — which loop are we talking about?

Welcome back to the Harness Engineering series. This is **Lecture 2**.

Let me quickly recall where we are. In Lecture 1, we built the vocabulary. We learned five words: prompt engineering, context engineering, harness engineering, loop engineering and graph engineering. We saw how they fit inside each other.

That was the map. In this lecture, we start walking.

We are going to open the harness up and look at what is inside it. Component by component. And as we understand each component, we are going to build it ourselves, from scratch. This lecture is the first of those builds.

In this lecture we look at the very first component inside the harness. It is called **the loop**.

And here I have to be careful, because the word "loop" came up in Lecture 1 as well, and these are two different things.

In Lecture 1, when I said loop engineering, I was talking about the big, outer loops. The loops we design around an agent, where a whole piece of work goes round and round.

The loop in this lecture is not that one. This loop is small. It lives inside the harness itself. It is what runs every single time you send one message to a coding agent. Think. Act. Observe. Think. Act. Observe. Its proper name is the **ReAct loop**. Some people simply call it the agent loop.

So for the rest of this lecture, whenever I say "the loop", I mean this small one. The loop inside the harness.

One more small note. I will say "agentic harness" and "harness" interchangeably. They mean the same thing. So from now on I will just say harness.

---

## 2. The five elements of a harness

`[SHOW diagram-01 — the pyramid]`

Before we go into the loop, let me formally introduce the five elements of a harness. Every serious harness in the world, small or big, is made of these same five things.

You can stack them like a pyramid.

At the bottom, we have **the loop**.
On top of that, we have **tools**.
Then we have **context and memory**.
Then **durability**.
And at the very top, **orchestration**.

Each layer answers one question.

The loop answers: how does a thought become an action?
Tools answer: what is the agent allowed to touch?
Context and memory answer: what does the model actually get to see?
Durability answers: what survives if something crashes?
And orchestration answers: how do many agents work together?

We will go through all five, one layer at a time, and we will build each one. At the end, we will assemble them into one complete harness of our own. And our harness has a name. We are calling it **Zill**.

Today, we take only the bottom layer. The loop.

And I want you to understand why we start here. Think of any element. Gold. Silver. Lead. If you keep breaking it down, at the end you reach one single atom. You cannot go smaller and still call it gold.

A harness is exactly the same. If you keep breaking a harness down, the smallest piece you reach is the loop. It is the atom of the harness. You can also call it the heartbeat. If the heart stops, nothing else matters. Without the loop, there is no harness.

So the smallest atomic unit of a harness is the loop. That is today.

---

## 3. My philosophy — small harness, detailed skills

`[SHOW diagram-02 — small harness + skill files = real products]`

Now, before we go into the loop, I want to share the philosophy behind Zill. You may follow a different philosophy later, and that is completely fine.

If you open any popular open-source harness today, you will notice one thing. They are big. Even the ones that people call "minimal" are still tens of thousands of lines of code, or more.

And there is a good reason for that. They are production systems. They support many model providers, many platforms, many edge cases. That is a lot of code.

But here is my bet.

Your harness can be very small. Very minimal. Around one thousand lines of Python. And you can still build serious things with it.

Then you will ask me: if the harness is so small, where does the quality come from?

It comes from the **skill files**.

The human contribution moves. It moves out of the engine, and into the instructions. The harness stays small and simple. The skill files become very detailed. You write down exactly how you want the frontend done, how you want the design system followed, how you want the testing done.

Small engine. Detailed instructions. That is the bet behind Zill.

And if this is true, then it means something beautiful. It means every single one of you watching this can build your own harness. Not just use one. Build one.

---

## 4. Why build your own at all?

Now somebody always asks this question, and it is a fair question. "Beyond learning, what is the actual benefit of building my own harness? Claude Code exists. Codex exists. Cursor exists."

I will give you two reasons.

Reason one. When you use these tools every day, it starts to feel like magic. Something mysterious is happening inside. And when something feels like magic, you become dependent on it. Today I want to show you that the magic is about ten lines of code. Once you see it, you cannot unsee it. You stop being a user and you start being an engineer.

Reason two. Independence. If you understand the harness, you are not locked to one company, one model or one price. If a tool becomes too expensive tomorrow, you are not stuck. You take your own harness, you plug in another model, and you continue working.

So we are not building Zill because the world needs one more harness. We are building it because you need to know that you can.

---

# PART B — The loop, in detail

## 5. A model, on its own, cannot do anything

`[SHOW diagram-03 — the model is a function]`

All right. So now let me explain this first element properly. The loop. The heartbeat of the harness.

And to understand why this loop has to exist at all, I have to start with something that sounds uncomfortable.

A language model cannot do anything.

It cannot open a file. It cannot run a command. It cannot remember what you said yesterday. It cannot even check its own work.

So what can it do? Only one thing. A language model is a function. You give it a list of messages. It gives you back one message. And then it stops. That is the entire transaction.

If you ask a bare model, "please delete this file," what happens? Nothing. It writes some text that says "okay, I will delete the file." But the file is still there. Nothing in your computer changed. It is only text, sitting in a variable.

Here is how I want you to picture it.

Imagine a genius locked inside a room. There are no windows. There is no phone. There is only a small slot under the door. You can slide a note in. The genius reads it, writes a brilliant reply, and slides it back out.

The genius can tell you exactly what to do. "Open the test file. I think the problem is on line twelve." But the genius cannot walk out and open the file. Someone outside the room has to do that.

That someone is the harness.

---

## 6. So what is a harness?

`[SHOW diagram-04 — the harness around the model]`

So now we can define it properly.

A harness is everything around the model.

It does three jobs.

Job one: it **assembles** what the model sees. It prepares the note that goes under the door.

Job two: it **executes** what the model asks for. It is the hands. It opens the file, it runs the command, it calls the API.

Job three: it **repeats**. It takes the result, brings it back to the model, and asks, "okay, what next?"

The model gives judgment. The harness gives hands, memory and persistence.

The word "harness" is actually a very good word. Think of a harness on a horse. The harness does not make the horse strong. The horse is already strong. The harness makes that strength usable.

And notice one more thing. People often say, "models are getting better, so soon we will not need all this." It is actually the opposite. A stronger model asks for more actions, works on longer tasks, and touches more files. That puts more load on the harness, not less. A crashed laptop, a full context window, a dangerous command — none of these are fixed by a smarter model. They live outside the model.

---

## 7. The heartbeat: thought, action, observation

`[SHOW diagram-05 — the ReAct triangle]`

Now let us look at how the model and the harness actually talk to each other. This is the heartbeat.

It has three beats.

**Thought.** The model looks at the situation and decides what to do next.

**Action.** The model asks for a tool, and the harness runs it.

**Observation.** The result of that tool comes back, and the model sees it.

And then it goes around again. Thought, action, observation. Thought, action, observation.

This has a name. It is called the **ReAct loop**. And please do not confuse this with React, the web framework. It has nothing to do with it. Here, ReAct means **Reason plus Act**. The name comes from a well-known research paper from 2022. I will put the link in the description.

`[SHOW diagram-06 — one task, six laps]`

Let me make this concrete with an example. Suppose I tell my agent: "There is an issue on my GitHub repository. Please fix it."

Watch what happens.

Lap one. The thought is: "I need to see the issue." The action is: use the GitHub tool to fetch the issue. The observation is: "Okay, I have the issue."

Lap two. The thought is: "Now I need to read the code." The action is the read-file tool. The observation is the content of the file.

Lap three. The thought is: "I found the bug. Let me fix it." The action is the edit tool. The observation is: "File updated."

Lap four. The thought is: "Did my fix actually work?" The action is: run the tests. The observation is: "All tests pass."

Lap five. The thought is: "Let me open a pull request." The action is the GitHub tool again. The observation is: "Pull request created."

Lap six. The thought is: "There is nothing left to do." No tool is called. The model simply gives the final answer, and it comes out of the loop.

Now stop for a second and look at what just happened.

Nobody told it "this task has six steps." I did not write step one, step two, step three. The model chose every step by itself, based on what it had just seen. And the model decided when it was finished.

By the way, this action step is also where many agent mistakes begin. If you give the model five hundred unnecessary tools, it gets confused about which one to pick. Remember that. We will come back to it in Lecture 3, when we build the tools.

So the next time you open Claude Code, or Cursor, or Codex, and you see it saying "reading file… editing… running tests…" — you now know exactly what is happening inside. It is this loop. Thought, action, observation. Again and again.

---

## 8. The model has no memory — the messages array

`[SHOW diagram-07 — the growing array]`

Now I have to break one illusion. And this is probably the most important idea in this lecture.

The model has no memory.

None. Zero.

Every time we call the model, it wakes up completely fresh. It does not remember your last question. It does not remember the file it read ten seconds ago. It does not remember the plan it made.

Then you will say, "But when I chat with it, it clearly remembers the whole conversation!"

No. It does not. Something else is remembering for it.

Think of a brilliant colleague who loses their memory every time they blink. How could you ever work with such a person? There is only one way. You keep a diary. And before every single question, you read the entire diary to them, from page one. Then they answer. Then you write their answer into the diary too.

That diary is called the **messages array**. It is just a list.

Look at the diagram. In call one, the list has the system prompt and the user's question. That goes to the model.

The model replies: "Let me read the test file." The harness runs the tool and gets the file contents. Both of those are **appended** to the list.

In call two, we send everything again. The system prompt, the user's question, the model's reply and the tool result. The whole list.

In call three, the list is longer again. And again we send the whole thing.

So the memory is not inside the model. The memory is the harness, re-sending this list every single time.

This gives us a very simple way to think. **Appending to the list is remembering. Deleting from the list is forgetting.** Almost every advanced feature we build later — memory, compaction, resuming a session — is just a careful edit of this one list.

And here is a practical gift. If you ever want to know what your agent knows at turn forty — every fact, every file, every plan — you do not need any special tool. You just print the list. That list is the agent's entire mind at that moment.

---

## 9. Three roles in the array

`[SHOW diagram-08 — three voices]`

Now let us open the list and look at one entry.

Every message is very small. It has a **role**, which says who is speaking. And it has **content**, which says what was said.

There are only three roles.

First, **system**. These are the standing rules. Who the agent is, which tools exist, how it should behave. It is written once and it sits at the top.

Second, **user**. This is everything that comes in from outside.

Third, **assistant**. This is the model's own voice. Its text, and its requests to run tools.

Now here is the part that surprises everybody.

When a tool runs and gives a result — say, the contents of a file — that result goes back to the model as input from outside. Just like a user message. No human typed it. A program produced it. But from the model's side, it arrives through the same door.

Think of it this way. The model has one mouth and one ear. The mouth is the assistant role. The ear is everything else. And the ear cannot tell the difference between a person and a program. A human typing, a file's contents, a command's output — it is all just input.

Later, when we build our own harness, we will label these messages with the word "tool" so that our own code stays readable. But remember the idea: it is still the outside world speaking to the model.

---

## 10. What a turn is, and the tax you pay

`[SHOW diagram-09 — the bars climbing]`

Let me define one word clearly, because people use it loosely. The word is **turn**.

One turn is one call to the model, plus the tool work it triggers. Call, act, append. That is one turn. One thought-action-observation.

A simple question might take one turn. "Fix the failing test" might take six.

Now think about the cost.

At time zero, before anything happens, the array already contains the system prompt, the list of tools, your skill files, and your project instructions file. Then the user's question is added. And all of that is sent.

In turn two, all of that is sent again, plus what happened in turn one.

In turn forty, we are paying to re-read turns one to thirty-nine.

Look at the bars. The amber part on top is the new work in each turn. It is the same size every time. The grey part underneath is everything being read again. It just keeps growing.

So this is a tax. You pay it on every single turn. In practice, an agent reads far, far more than it writes.

This is why you must build your context wisely. Do not load five hundred tools "just in case." Do not paste a forty-thousand-line log when the last two hundred lines are enough. Everything you leave in the list, you pay for again and again. Your memory is also your invoice.

We will spend one full day on this problem later. For now, just plant the idea.

---

## 11. How a tool call finds its result

`[SHOW diagram-10 — the ticket]`

One small piece of bookkeeping, and then we go to the code.

When the model asks for a tool, it does not just say "read the file." It sends a small structured request. That request has a name — which tool. It has arguments — which file. And it has an **id**.

Think of the token number at a busy restaurant counter. You place your order and they give you token seventeen. When the food is ready, they call "seventeen." That number makes sure you get your food and not somebody else's.

The id is that token. The model says, "here is a job, token A-seventeen." And when our harness sends the result back, it attaches the same token, A-seventeen.

Two rules come from this.

Rule one: every request must get exactly one result. If the model asked for three tools, it must get three results. Not two. If one request is left unanswered, the list is broken and the next call will fail with an error.

Rule two: one turn can carry several requests at once. Modern models often ask for three files in parallel. So our loop must go through every request and answer each one.

Keep rule one in your mind. When we get to durability later in the series, you will see that some of the nastiest bugs come from exactly this — a crash that happens after the request was saved, but before the result was saved.

---

## 12. The loop, derived

`[SHOW diagram-11 — the loop, derived]`

Now we have everything we need. Let us put the whole loop on one picture. And I want you to notice something as we go. We are not going to design this loop. We are going to be forced into it, one step at a time.

Look at the left side first. That stack is our messages array. System, user, and then whatever gets added. It grows on every lap. And remember, this list is the memory.

Now follow the numbers.

**Step one.** We call the model, and we hand it the messages. That is the box that says call model.

**Step two.** The model replies, and we ask exactly one question. Did it ask for a tool?

If the answer is **no**, the model has given us plain text. That is its only way of saying, "I do not need anything else done. Here is my answer." So we follow the red arrow down, we return the answer, and we are out of the loop.

If the answer is **yes**, we cannot return yet. There is work to do.

**Step three.** Our code runs each tool. Look at the words in that box: *our* code. Not the model. The model cannot run anything. It can only ask. The harness does the running.

Now we are holding something the model has never seen — the result of that tool.

**Step four.** So we append that result to the messages. The stack on the left gets one block taller.

**Step five.** And we go back to step one. We call the model again, and this time the model sees the result. It decides again.

That is the whole loop. Call. Check. Run. Append. Repeat.

Now look at the note in the corner, because this is the real lesson. The loop is not designed. It is forced by what the model cannot do. The model cannot act, so we act for it. We then know something the model does not, so we must show it. And the moment we show it, we are back at the start. Each step is forced by the step before it.

One last thing on this picture. Bottom left. Max turns. That is our safety brake. If the model gets stuck and the laps keep going, we stop at a fixed number, ask the model for a short wrap-up, and exit. I will come back to this in a minute.

---

## 13. The loop, in about ten lines

`[SHOW diagram-12 — the code]`

And here it is in code.

Let us read it together, slowly.

We define a function called run loop. It takes the messages, the tools, and a maximum number of turns.

For each turn: we call the model. That is the thought.

We append the reply to the messages. That is remembering.

If the reply has no tool calls, we return the text. We are done.

Otherwise, for every tool call in the reply, we run the tool — that is the action — and we append the result — that is the observation.

And if we ever run out of turns, we ask for a wrap-up and exit safely.

Count the lines. It is about ten.

`[PAUSE — let it sit on screen for two seconds]`

I want you to really take this in. This is the heart of every coding agent you have ever used. Claude Code, Cursor, Codex, all of them. The tools, the permissions, the memory, the sub-agents — all of that is equipment attached to these ten lines.

Most people believe that agency is some deep magic inside the model. It is not. Agency is a loop around the model. A loop that keeps calling a function that has no memory, and keeps feeding it what happened.

Once this lands, the whole subject changes. We are not studying something mystical. We are studying a control loop.

---

## 14. Who decides when it is done?

`[SHOW diagram-13 — workflow vs agent]`

Now let me show you why this small loop is so powerful. And it comes down to one question. Who decides when the work is done?

There are two ways to make a model do multi-step work.

Look at the left side. This is a **workflow**. Plan, step one, step two, step three, done. Who wrote those steps? You did. The plan is fixed, and it was written ahead of time. *You* decided there would be three steps.

That is perfectly fine when you can predict the shape of the task. But it breaks the moment the task is unpredictable. What if two steps were enough? What if this particular bug needed five? A workflow cannot branch. It makes no decisions along the way. It just walks the path you drew.

Now look at the right side. This is an **agent**. There are no numbered steps here. There is only a loop, going round and round. And look at what is sitting in the middle — a steering wheel. Because in an agent, the model is in the driver's seat.

On every lap, the model chooses: act again, or stop. The number of laps is not written anywhere. It depends on the task. A small fix may take two laps. A messy one may take fifteen.

And that red arrow in the middle is the big idea. It is called **inversion of control**. The exit condition has moved. It has moved out of your code, and into the model.

In a workflow, you decide when it is done. In an agent, the model decides when it is done. That is the whole difference between the two. And that is exactly why an agent can handle open-ended work that you could never script in advance.

Now, handing the steering wheel to a model should make you a little nervous. And it should. Sometimes a model gets stuck. It politely reads the same file again and again, and never says "I am done."

So we keep one brake. **Max turns.** It is a simple counter. If the loop reaches that number, we stop it, no matter what. And we do not just crash. We make one final call, with no tools, and we say: "You are out of turns. Summarise where things stand." So the human reads a status report, not an error.

One rule to remember: never end a run without a report.

And one more. If a tool fails in the middle of a lap, we do not crash the loop. We put the error text into the result and hand it back to the model. Very often the model reads the error and fixes the problem by itself.

---

## 15. A skill is not a tool

`[SHOW diagram-14 — skill vs tool]`

One last piece of theory. Let me clear one very common confusion. People mix up skills and tools all the time.

A **tool** is a piece of code. It is a function the harness can run. It does one concrete thing. Read a file. Run a command. It has a name and it has arguments.

A **skill** is a document. It is written in plain language. It explains how to do a job, step by step. "This is how we build a frontend in this project. Use this design system. Follow this order."

Think of a kitchen. The tool is the knife. The skill is the recipe. The recipe may tell you which knife to use, but the recipe is not a knife.

So a skill can mention tools. But a skill is not a tool.

And now a small question for you. Suppose you have a frontend template, and you want your agent to always follow it. Where does it go in the messages array?

`[PAUSE]`

It goes in a skill file. And the skill file goes into the array, as part of what the model sees. That is how the whole system stays modular. You do not change the harness. You change the instructions.

---

# PART C — Now we build it

## 16. The three pieces of a bare harness

`[SHOW diagram-15 — three pieces of a bare harness]`

So. You now understand the loop at a fundamental level. Before we build it, let me put everything from today on one single picture. Because the simplest possible harness — a bare harness — has only three pieces.

**Piece one, at the top: the model client.** Its whole job is one line. Send the messages, get a reply. It is the only piece that talks to the model company.

**Piece two, bottom left: the message array.** System, user, assistant, tool, and so on. Every new message is appended here, and it keeps the history across turns. And look at the red note. This list *is* the agent's state. There is no other state hiding anywhere.

**Piece three, bottom right: the tools.** Each tool is just a name, a description of its arguments, and a function. For example, a read-file tool is a few lines of ordinary Python.

And in the middle, connecting all three, is the loop. Send. Tool? Run. Append. Repeat.

Read the box at the bottom with me. Client, plus message array, plus tools, spun in a loop, equals an agent.

That is it. That is all an agent is. And that is exactly what we are going to build today.

---

## 17. The provider — one doorway to the model

`[SHOW diagram-16 — provider.py]`

Let us take piece number one first, the model client. Something has to actually send our list to a model. In Zill, that is one file. We call it the **provider**.

The provider does four jobs.

One, it **authenticates**. It holds the API key.

Two, it **translates**. We keep our own simple message format inside Zill. The provider converts it into whatever shape the model company expects, and converts the answer back.

Three, it **retries**. Networks fail. Rate limits happen. The provider waits a little and tries again.

Four, it **normalises**. Whatever comes back, it turns into one clean shape: some text, maybe some tool calls, and a token count.

Why do we put all of this in one file? Because of one benefit. If tomorrow you want to switch from Gemini to Claude, or to OpenRouter, you change this one file. The loop does not notice. Nothing else in the harness notices.

Think of it as the one doorway in the house. Every model company's strange little requirements stay at the doorway. They do not spread through the rooms.

---

## 18. Let us build it

`[SHOW diagram-17 — what we build today]`

Okay. Now we build.

Today we write only two files. `provider.py`, the doorway. And `loop.py`, the heartbeat. Plus one tiny demo with a deliberately silly tool — a dice roller — so we can watch the full cycle safely, without touching any real files.

And we are not going to type this by hand. We are going to write a careful prompt, and give that prompt to a coding agent. You can use Claude Code. You can use Codex. You can use any open-source agent you like. It does not matter.

You need two things ready.

First, an API key for a capable model. A free Gemini key is fine to start. Do not paste your key into the prompt. That is a bad habit. Put it in a small `.env` file, and tell the agent where that file is.

Second — and this is the fun part — a name. I am calling mine Zill. You can follow along with Zill, or you can give yours your own name. Whatever you choose, it is yours.

`[SCREEN: switch to the terminal, open the coding agent]`

Here is the prompt I am giving.

`[SCREEN: paste the prompt below — read it out section by section as it appears]`

```text
You are building the first part of Zill (lecture 2 of the series), a minimal agentic harness in Python.
Standard library only, no third-party packages, Python 3.10+.

Setup
- Create a project folder named zill-harness and run git init.
- Add a .gitignore covering __pycache__/, *.pyc, .env and .DS_Store.
- All harness code lives in a package folder named zill/ (create an empty
  zill/__init__.py). Demos live in demos/.
- Commit after each working milestone.

Style
- Keep it minimal and readable. This is teaching code.
- Every file starts with a docstring saying what concept it teaches.
- Every public function has a short docstring.
- Target sizes: provider.py about 100 lines, loop.py about 65 lines.

API key
- Read the key from the environment variable ZILL_API_KEY. A .env file at
  <PATH TO YOUR .env FILE> contains it; load it from there if the variable is
  not set. Never print the key and never commit it.
- Use the <YOUR PROVIDER> API with the model <YOUR MODEL ID> as DEFAULT_MODEL.

zill/provider.py — the only file that knows which vendor we use
- complete(model, system, messages, tools) sends one request and returns
  {"text": str, "tool_calls": [...], "usage": {"input": int, "output": int}}.
- Internally Zill uses one neutral message format:
    {"role": "user", "text": ...}
    {"role": "assistant", "text": ..., "tool_calls": [...]}
    {"role": "tool", "name": ..., "text": ...}
  Translate to and from the vendor's wire format inside this file only. If the
  vendor requires any extra field to be echoed back with a tool call, store it
  on the tool call and send it back.
- Retry with exponential backoff on HTTP 429, 500, 502, 503 and on timeouts.
  On any other HTTP error raise RuntimeError with the status and the start of
  the error body.

zill/loop.py — the heartbeat
- run_loop(model, system, messages, tools, on_event, max_turns=80) -> str.
  tools is a dict of name -> tool; each tool has .spec (its schema) and .run.
- Each turn: call provider.complete, append the assistant message, fire
  on_event. If there are no tool calls, return the text. Otherwise run every
  tool call in order and append one tool message per call.
- An unknown tool returns the text "ERROR: unknown tool <name>". A tool that
  raises returns "ERROR: <ExceptionType>: <message>". The loop must never
  crash because a tool did.
- When max_turns runs out: append a user message asking the model to wrap up,
  make one final call with no tools, and return that text.

demos/day1_dice.py
- A hand-written roll_dice tool, an on_event that prints every message, and
  the task: "Roll 3 dice and tell me whether the total beats 10".

Verify before finishing
1. The dice demo prints four messages in order: user, assistant tool call,
   tool result, assistant answer.
2. The prompt "Build a landing page for a coffee shop" returns text only, with
   no tool calls.
3. git log shows today's commits.
```

`[While it runs, keep talking:]`

While this runs, notice what I asked for. I asked for size targets, because we want a minimal harness. I asked for no third-party packages. And at the bottom I asked it to verify its own work. A good prompt always says what "done" means.

`[When the dice demo runs:]`

Look at this. Four messages. The user's request. The model asking for the dice tool. The tool's result. And the model's final answer. That is one full heartbeat, running on our own code.

`[Then run the landing page prompt:]`

And now watch this. I ask it to build a landing page for a coffee shop. And what does it do? It can only describe one. It cannot create a single file.

Why? Because it has judgment, but it has no hands. A dice roller is not a toolbox.

That gap is exactly what we close in the next lecture.

---

## 19. Homework

Before the next lecture, I want you to do three small things.

One. Print the messages array after every turn, and watch it grow. Then do a small experiment. Comment out the line that appends the tool result, run it again, and read the error you get. Nothing teaches "the array is the state" better than breaking it with your own hands.

Two. After every turn, print the turn number, the input tokens and the output tokens. Your provider already returns these numbers. Run three tasks — one tiny, one medium, one that you expect to struggle — and write the numbers in a small table. Look at how much bigger the input number is than the output number.

Three. Set max turns to one, on a task that needs a tool. Watch what the ending looks like.

Keep that table. We will open our lecture on context with it.

---

## 20. Closing

So let us close.

Today you learned that a model, by itself, can do nothing. It is a genius in a locked room.

You learned that a harness is everything around it — the hands, the memory and the persistence.

You learned that the model has no memory, and that the whole memory is one list that we re-send every time.

And you learned that the heartbeat of every agent in the world is a loop of about ten lines. Thought, action, observation.

In Lecture 1, this still felt like a word on a slide. Now it is running on your machine, and you can read every line of it.

That is what I want for you from this series. Not to be someone who only uses these tools. To be someone who can build them.

In this lecture, Zill got a heartbeat. In Lecture 3, we give it hands. See you there.

---

## Notes for you (not spoken)

**Diagram cue list** (same numbers in `diagrams/` and `diagrams-pro/`)

| # | File | Use it in section |
|---|------|-------------------|
| 01 | diagram-01.png | 2 — five elements pyramid |
| 02 | diagram-02.png | 3 — small harness + skills |
| 03 | diagram-03.png | 5 — model is a function |
| 04 | diagram-04.png | 6 — what a harness is |
| 05 | diagram-05.png | 7 — ReAct triangle |
| 06 | diagram-06.png | 7 — six laps example |
| 07 | diagram-07.png | 8 — growing messages array |
| 08 | diagram-08.png | 9 — three roles |
| 09 | diagram-09.png | 10 — the per-turn tax |
| 10 | diagram-10.png | 11 — tool call id / ticket |
| 11 | diagram-11.png | 12 — the loop, derived |
| 12 | diagram-12.png | 13 — loop code |
| 13 | diagram-13.png | 14 — who decides (workflow vs agent) |
| 14 | diagram-14.png | 15 — skill vs tool |
| 15 | diagram-15.png | 16 — three pieces of a bare harness |
| 16 | diagram-16.png | 17 — provider |
| 17 | diagram-17.png | 18 — today's build |

**Things to check before recording**

- Section 1 describes loop engineering as "the big, outer loops we design around an agent". Change that one sentence so it matches exactly how you defined loop engineering in Lecture 1.
- Lecture numbering assumed: Lecture 1 = prompt → graph engineering, Lecture 2 = this (the loop), Lecture 3 = tools. If your series plan differs, search the script for "Lecture 3" and "Lecture 1" and adjust.
- The diagram files and the script file are still named "day1". Rename them if you like; nothing inside depends on the file names.
- Fill the three `<…>` placeholders in the build prompt: the `.env` path, the provider, and the exact model id (model names change often — copy it from your provider's dashboard).
- I kept all numbers about other harnesses vague on purpose ("tens of thousands of lines or more"). If you want to name specific projects and line counts, verify them first.
- The script never claims Zill has already built a product or passed a benchmark. Add such claims only after you have done it.
- The ReAct paper for the description: *ReAct: Synergizing Reasoning and Acting in Language Models* (Yao et al., 2022).
- This lesson follows the structure of the Odysseus bootcamp's Day 1. A credit line in the description is the right thing to do.
