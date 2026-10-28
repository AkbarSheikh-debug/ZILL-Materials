# Lecture 3 — Tools and security

> **Lecture 3 of 6 — tools and security**
> Phase-by-phase script. Tags such as `[OPEN]`, `[EXPLAIN]`, `[STOP]` mark the speaking rhythm.

**Speaking script — phase-by-phase version.**
Lecture 1 gave the vocabulary. Lecture 2 built the loop. This lecture gives Zill its hands (tools) and its conscience (security).

---

## How this script is organised (read this once, not spoken)

The lecture is cut into **12 phases**. Each phase is cut into small **beats**. A beat is one idea, about one to three minutes.

**Every beat has the same four steps, always in this order:**

| Tag | What you do |
|-----|-------------|
| `[OPEN]` | One or two sentences that tell the viewer what is coming. |
| `[EXPLAIN]` | The explanation. Short paragraphs. **One paragraph = one breath.** |
| `[TAKEAWAY]` | One line that sums up the beat. Say it **slowly**, looking at the camera. |
| `[STOP]` | Stop talking. Breathe for two seconds. Then start the next beat. |

So you always know where you are, and you always know where to stop.

**Other tags (none of these are spoken):**

- `[SCREEN → diagram-07]` — put this picture on screen (folder `diagrams-lecture3/`).
- `[DRAW → draw-02…]` — draw this on the board. Copy it from the picture in the folder `drawings-to-copy/`.
- `[WRITE]` — write these words on the board while you talk.
- `[ASK]` — ask the viewers a question and tell them to pause the video.
- `[OPTIONAL]` … `[END OPTIONAL]` — you can skip this part if the video is getting long.
- `[PHASE CHANGE]` — a big change of topic. Pause for three seconds. Then say the line that follows it.

**Rules for speaking it**

1. Anything inside `[square brackets]` is for you. Do not read it aloud.
2. Each blank line is a small pause.
3. Words in **bold** are the words to stress.
4. If you lose your place, go to the next `[OPEN]` and continue from there. Nothing will be lost.

---

## Map of the lecture (not spoken)

| Phase | What it is about | Time | Pictures | Board drawings |
|-------|------------------|------|----------|----------------|
| 0 | Opening and the plan | 2 min | — | — |
| 1 | Revision of Lecture 2 | 3 min | 01 | — |
| **PART 1** | **What is a tool?** | | | |
| 2 | Tools in simple words | 5 min | 02, 03 | — |
| 3 | The tool contract | 9 min | 04, 05, 06 | draw-01 |
| **PART 2** | **Which tools do we build?** | | | |
| 4 | The six tools | 10 min | 07, 08, 09, 10 | draw-02, draw-09 |
| | *— natural break: you can end video 1 here —* | | | |
| **PART 3** | **How do we keep them safe?** | | | |
| 5 | Why security | 4 min | — | draw-03 |
| 6 | Protection 1: the gate | 8 min | 11, 12, 13 | draw-04 |
| 7 | Protection 2: the jail | 6 min | 14 | draw-05, draw-06 |
| 8 | Protection 3: the backend | 6 min | 15, 20 | draw-07 |
| **PART 4** | **Put it together and build it** | | | |
| 9 | The whole picture | 5 min | 17, 16, 18 | draw-08 |
| 10 | The build | 10 min | 19 | — |
| 11 | Homework and closing | 3 min | — | — |

Total: about 70 minutes with the build. If that is too long, record Phases 0–4 as one video and Phases 5–11 as the next.

---
---

# PHASE 0 — Opening

*Goal of this phase: the viewer knows what today is about, and how the lecture is laid out.*

### Beat 0.1 — Hook: a brain with no hands · about 1 min

`[OPEN]`

Hello everyone, and welcome back to the Harness Engineering series. This is lecture number three.

`[EXPLAIN]`

Let me start with a small story from the last lecture.

In the last lecture, we built the loop. Our harness, Zill, got its heartbeat.

And at the very end, we tried something. We asked Zill: "Build a landing page for a coffee shop."

And what did it do?

It did not build anything. It only **described** a landing page, in words.

Why did that happen?

Because Zill had a brain. But it had **no hands**.

So today, we fix that. And we do it in two steps.

Step one. We give Zill hands. In our world, hands are called **tools**.

Step two. We make sure those hands cannot do damage. That is called **security**.

`[TAKEAWAY]`

So remember just two words for today. **Tools**, and **security**. Hands, and a conscience.

> `[WRITE]`
> **LECTURE 3**
> 1. TOOLS = the hands
> 2. SECURITY = the conscience

`[STOP]`

### Beat 0.2 — The plan for today · about 1 min

`[OPEN]`

Before we begin, let me tell you how this lecture will go. So that you can follow along easily.

`[EXPLAIN]`

There are four parts.

Part one. What is a tool, really?

Part two. Which tools do we build?

Part three. How do we keep them safe?

And part four. We build everything, and we run it.

Every time we move from one part to the next, I will tell you. So you will never be lost.

> `[WRITE]`
> **TODAY — 4 PARTS**
> Part 1 · What is a tool?
> Part 2 · Which tools do we build?
> Part 3 · How do we keep them safe?
> Part 4 · Build it and run it

`[STOP]`

---
---

# PHASE 1 — Revision of Lecture 2

*Goal of this phase: the viewer remembers the loop, and sees the two places where today's work plugs in.*

### Beat 1.1 — Lecture 2 in one minute · about 1.5 min

`[OPEN]`

First, a one-minute revision of the last lecture. Because everything we do today is plugged into it.

`[EXPLAIN]`

In the last lecture, we learned three things.

Number one. A model, by itself, cannot **do** anything. It can only think, and reply with text.

Number two. So we put a **loop** around it. The model thinks. It asks for an action. Our harness runs that action. And the result goes back to the model. Thought, action, observation. Again and again.

Number three. The model has **no memory**. Everything it knows is in one list, called the **messages array**. And we send that whole list to the model on every single turn.

`[ASK]`

Now a quick question for you. Please pause the video and answer it. What all is inside the messages array?

*[wait two seconds]*

Here is the answer. The system prompt. The user's request. The descriptions of the tools. The skill files. Your project instructions. And the whole conversation so far.

Keep "the descriptions of the tools" in your mind. We will need it today.

`[TAKEAWAY]`

So, lecture two in one line: a model that can only think, a loop around it, and one list which is its memory.

`[STOP]`

### Beat 1.2 — The two empty sockets · about 1.5 min

![Diagram 01](../assets/lecture-3/diagrams/diagram-01.png)
*Diagram 01 — Where we left off*

`[OPEN]`

Now let me show you exactly where today's work goes.

`[EXPLAIN]`

Look at this picture. In the middle is our file from last time. `loop.py`.

This loop has two empty places, where we can plug something in. I call them **sockets**. Like the socket on your wall. The socket is already there. You just plug something into it.

**Socket one** is the list of tools. Last time, it had only one toy tool in it. A dice roller.

**Socket two** is a small function called `before_tool`. Before the loop runs any tool, it first asks this function: "May I run this?" Last time, this function simply said yes to everything.

Today, we fill both sockets.

Into socket one, we plug real tools. That is the file `tools.py`.

Into socket two, we plug a real guard. That is the file `security.py`.

And there is one more small file, `operations.py`. It decides on which machine a tool runs. I will explain it properly in part three.

Now look at the box at the bottom of the picture.

The loop does not know the names of the tools. It only knows: "here is a list of tools." That is why we will **not** change `loop.py` today. Not one line.

`[TAKEAWAY]`

So today is not about changing the loop. Today is about **plugging things into it**.

> `[WRITE]`
> Socket 1 → `tools.py` (the hands) + `operations.py` (where they work)
> Socket 2 → `security.py` (the conscience)
> `loop.py` → **no change**

`[STOP]`

---
---

# PHASE 2 — Tools in simple words

*Goal of this phase: the viewer can say what a tool is, and knows there are two kinds.*

`[PHASE CHANGE — pause three seconds]`

Alright. The revision is done.

Now we start **part one of four**. What is a tool?

### Beat 2.1 — A brain in a jar · about 2 min

![Diagram 02](../assets/lecture-3/diagrams/diagram-02.png)
*Diagram 02 — A brain in a jar*

`[OPEN]`

Let me begin with a very simple picture.

`[EXPLAIN]`

Think of the language model as the **engine** of a car. The engine is powerful. But an engine alone does not take you anywhere. You need wheels.

Tools are the **wheels**.

Here is another way to see it. Look at the screen.

Imagine a brain inside a glass jar. This brain can think very well. But it cannot touch anything. It cannot open a file. It cannot send a message.

A tool **breaks that glass**. With a tool, the model can reach outside the jar.

And what is outside the jar? Look at the right side.

Your GitHub repository. Your terminal. Your Google Drive. Slack. Or any API, like Zoom, or Jira, or Notion.

Now remember our loop. Thought, action, observation.

Which of these three is a tool?

It is the **action**. The middle word.

`[TAKEAWAY]`

So here is the simple definition. A tool is anything that lets the model **touch the world outside**.

> `[WRITE]`
> MODEL = the engine · TOOLS = the wheels
> **Tool = anything that lets the model touch the outside world**
> Thought → **ACTION** → Observation

`[STOP]`

### Beat 2.2 — Two kinds of tools · about 3 min

![Diagram 03](../assets/lecture-3/diagrams/diagram-03.png)
*Diagram 03 — Two kinds of tools*

`[OPEN]`

Now, tools come in two kinds. And most people do not know this.

`[EXPLAIN]`

Kind one is **pre-built** tools. These come inside the harness. You install the harness, and they are already there.

Kind two is **external** tools. These are added later, by you, or by your project.

Let us take the pre-built ones first. Look at the left box. Almost every coding harness comes with these seven.

**Read.** It reads a file.

**Write.** It creates a new file.

**Edit.** It changes a part of a file.

**Bash.** It runs a command in the terminal.

**Grep.** It searches for text inside files.

**ls.** It lists what is inside a folder.

**Find.** It finds where a file is.

Two of these need a small note.

First, **bash**. Bash is the most powerful tool in this list. And it is also the most dangerous. Why? Because it can run **any** command. And "any command" includes deleting things.

Please remember this. The whole second half of this lecture exists because of bash.

Second, **grep and find**. People mix them up. Find looks for a file by its **name**. Grep looks **inside** the files, for a piece of text.

Now the right box. External tools. There are two common ways to add them.

One way is an **MCP server**. Think of it as a ready-made pack of tools, which someone has already written. For example, there is a GitHub MCP server. You connect it once, and your model gets a whole set of GitHub tools. You do not write them yourself.

The other way is simple. You write your own small script, and you register it as a tool.

Now look at the box at the bottom. This is a design question, and every harness builder has to answer it.

How many tools should I ship inside my harness?

Pi ships very **few**, and lets you add the rest. That keeps the code small.

Hermes ships **many**. That is convenient. But the code becomes much bigger.

For Zill, we follow Pi. Few tools, small code. And in your own harness, you are free to choose differently.

`[TAKEAWAY]`

So, two kinds. **Pre-built** tools come with the harness. **External** tools are added later. And how many you ship is your design choice.

> `[WRITE]`
> **PRE-BUILT:** read · write · edit · **bash** · grep · ls · find
> **EXTERNAL:** MCP servers · your own scripts
> bash = most powerful **and** most dangerous
> Zill → few tools, like Pi

`[STOP]`

---
---

# PHASE 3 — The tool contract

*Goal of this phase: the viewer understands that the model sees only words, never code. This is the most important phase of the lecture.*

`[PHASE CHANGE — pause three seconds]`

We are still in part one. And now we come to the **most important idea** of today's lecture.

So please give me your full attention for the next few minutes.

### Beat 3.1 — The model never sees your code · about 3 min

`[OPEN]`

Let me ask you a question. When the model decides to use a tool, what does it actually look at?

`[EXPLAIN]`

Most people think the model looks at the code of the tool.

That is wrong. The model **never sees your code**. Not even one line.

Let me draw this for you.

![Board drawing draw-01-job-posting-and-curtain.png](../assets/lecture-3/drawings-to-copy/draw-01-job-posting-and-curtain.png)
*Board drawing — follow the numbers 1, 2, 3, 4*

*[while drawing the board and the three cards]*

Think of a job posting on a notice board. It has three things. A **title**. A **description**. And a **form** to fill in.

*[while drawing the person]*

A person reads this posting, and decides: should I apply, or not?

*[while drawing the curtain and the box behind it]*

That person never sees the real work. The real work is behind a curtain.

Now, here is the point.

The **model** is that person. It sees only the posting. The title, the description, the form.

Your **code** is behind the curtain.

So if the posting is vague, you get wrong applications. If the posting is clear, you get the right ones.

`[TAKEAWAY]`

The model chooses a tool by reading **words**. Only words. If you remember this one sentence, half of today's lecture is done.

> `[WRITE — at the bottom of the drawing]`
> The applicant never sees the work. Only the posting.

`[STOP]`

### Beat 3.2 — A tool has two halves · about 2 min

![Diagram 04](../assets/lecture-3/diagrams/diagram-04.png)
*Diagram 04 — A tool has two halves*

`[OPEN]`

Now let me show you the same idea in its proper technical form.

`[EXPLAIN]`

Look at the screen. A tool has **two halves**.

The left half is called the **interface**. This is what the model sees.

The right half is called the **implementation**. This is the code which actually runs.

And between them is the curtain.

Let us go through the left half. There are four things.

One. The **name**. For example, "read file".

Two. The **label**. This is just a tag. Like a name tag which you wear at a big event, so that people know who you are.

Three. The **description**. This tells the model **when** to use this tool. And this is the most important of the four. With a good description, the model picks the right tool. With a poor one, it picks the wrong tool.

Four. The **parameters**. These are the blanks which the model has to fill in. For a read tool, the blank is: which file?

Now the right half. This is simply your function. It receives the blanks which the model filled in, and it does the real work. It reads the file. It runs the command.

In Pi, this function also receives a few extra things. You can see them on the screen. You do not need to remember them today.

`[TAKEAWAY]`

So. The interface is for the **model**. The implementation is for the **machine**. And the model only ever sees the interface.

> `[WRITE]`
> **A TOOL = TWO HALVES**
> INTERFACE (the model sees): name · label · **description** · parameters
> IMPLEMENTATION (runs): your function

One small tip for interviews. If someone asks you, "how do you define a tool?", say this: "A tool has two halves. The interface, which the model reads. And the implementation, which the harness runs."

`[STOP]`

### Beat 3.3 — A real contract, line by line · about 2 min

![Diagram 05](../assets/lecture-3/diagrams/diagram-05.png)
*Diagram 05 — What the model actually receives*

`[OPEN]`

Enough theory. Let me show you a real one.

`[EXPLAIN]`

This is the read-file tool, exactly as the model receives it. Let us read it slowly, from top to bottom.

The first line is the **name**. Read file.

Next is the **description**. "Read a file. Returns its contents with line numbers."

Look at the green part. "With line numbers."

Why did we write that? Because now the model knows the answer will have line numbers. So in its next step it can say, "look at line twelve."

Those three small words change how the model behaves.

Next is the **parameter**. There is only one. Path. And it has its own small description, in blue. "Path relative to the working directory."

So the model will not guess some strange path from somewhere else.

And the last line, in red. **Required**. It says that path is required. The model must fill it. It cannot skip it.

There are two lessons in this picture.

Lesson one. This is not a suggestion to the model. It is a **fence**. The model cannot go outside it.

Lesson two. This whole text is sent to the model on **every single turn**. Whether the tool is used or not. So every extra word costs you, again and again.

So keep the description short. Write only what changes the model's behaviour.

`[TAKEAWAY]`

A good description says three things. What the tool does. What comes back. And any rule the model must follow.

> `[WRITE]`
> **A good description says:**
> 1. what the tool does
> 2. what comes BACK
> 3. any rule to follow
> Sent on every turn → keep it short

`[STOP]`

### Beat 3.4 — A bad contract and a good one · about 2 min

![Diagram 06](../assets/lecture-3/diagrams/diagram-06.png)
*Diagram 06 — A loose form and a tight one*

`[OPEN]`

Now let me show you a bad one and a good one, side by side. This is the fastest way to learn.

`[EXPLAIN]`

Both of these are for the same tool. An edit tool.

Look at the left one first. The description says only: "Edit a file." And there is one blank, called "args".

Now think like the model. What should I write in "args"?

I do not know. So I will guess. Maybe my guess matches the code. Maybe it does not.

And the dangerous thing is this. The bad version gives **no error**. It looks fine. It just fails quietly, again and again.

Now look at the right one.

The description is clear. "Replace an exact text snippet. It must appear once."

And there are three blanks. Path. Old text. New text.

Now the model is just filling in a form. It is very hard to get this wrong.

One more point, at the bottom of the screen.

Beginners think: "let me mark everything as required. It will be more reliable."

It is the opposite. If a blank is required, and the model has nothing real to put there, it will **invent** something.

So mark as required only what the function truly needs.

And here is one habit for you. When the model keeps using a tool wrongly, do not add more warnings to your system prompt. **Fix the contract of the tool.** That is where the problem is.

`[TAKEAWAY]`

A clear name. A clear description. Clear blanks. That is a good contract.

> `[WRITE]`
> **RULES FOR A CONTRACT**
> 1. One clear job
> 2. Clear, named blanks (never one blank called "args")
> 3. "Required" = only what is truly needed
> 4. Tool used wrongly? → fix the CONTRACT

`[STOP]`

### Recap of Part 1 · about 30 sec

`[OPEN]`

Let me stop here for a moment, because part one is finished.

`[TAKEAWAY]`

Here is part one in three lines.

One. A tool lets the model touch the outside world.

Two. A tool has two halves. The model sees only the words. Never the code.

Three. So most of the skill is in writing those words well.

If you have understood these three lines, you have understood part one.

`[STOP — three seconds]`

---
---

# PHASE 4 — The six tools

*Goal of this phase: the viewer knows the six tools, the two design rules, why edit is special, and why bash is dangerous.*

`[PHASE CHANGE — pause three seconds]`

Now we move to **part two of four**. Which tools do we actually build?

### Beat 4.1 — Why only six · about 2.5 min

![Diagram 07](../assets/lecture-3/diagrams/diagram-07.png)
*Diagram 07 — Six hands cover the verbs*

`[OPEN]`

My answer is: six tools. Only six.

`[EXPLAIN]`

Think about what a software developer actually does all day. It comes down to six actions.

You **look** at things. You **create** things. You **fix** things. You **run** things. You **move around** the project. And you **search**.

Now look at the screen. One tool for each action.

To look: read file.

To create: write file.

To fix: edit file.

To run: bash.

To move around: list files.

To search: grep.

`[OPTIONAL]`

![Board drawing draw-02-cook-with-few-hands.png](../assets/lecture-3/drawings-to-copy/draw-02-cook-with-few-hands.png)
*Board drawing*

Let me draw it another way. Imagine you are hiring a cook.

You could give the cook a drawer full of forty gadgets. A garlic press. An egg separator.

Or you could give the cook a few things which do everything. Eyes, to read the recipe. A pencil, to fix it. And a **stove**, which cooks anything.

Almost every gadget is just the stove, in a costume.

`[END OPTIONAL]`

Now you may ask: "Why not add more tools? A tool to run tests. A tool for git. A tool to install packages."

Because all of those are just **bash**. The model already knows how to type the command to run tests. A separate tool adds nothing.

And it **costs** something.

Every extra tool is one more option which the model has to think about, on every turn. More options means more confusion. More confusion means more mistakes.

So there is a simple rule. **One tool, one job.** And two tools should never do the same job.

By the way, Pi has a seventh tool, find. We are skipping it in Zill, to stay small.

`[TAKEAWAY]`

Six actions, six tools. And fewer tools means a clearer mind for the model.

> `[WRITE]`
> look → `read_file` · create → `write_file` · fix → `edit_file`
> run → `bash` · move around → `list_files` · search → `grep`
> **One tool = one job.** More tools = more confusion.

`[STOP]`

### Beat 4.2 — Two rules for designing any tool · about 2.5 min

![Diagram 08](../assets/lecture-3/diagrams/diagram-08.png)
*Diagram 08 — Two axes of tool design*

`[OPEN]`

Now, when you design any tool, there are only two rules to keep in mind. Just two.

`[EXPLAIN]`

**Rule one. Help the model's next step.**

Let me give you two examples.

Our read tool returns line numbers. Why? So that the model can point to an exact line later.

Our write tool creates the folder if it is missing. Why? So that the model does not waste a turn doing that.

**Rule two. Keep the output small.**

Why is this so important? Remember the last lecture.

Everything a tool returns goes into the messages array. And that array is sent again on every turn after that.

So one huge output is not paid for once. It is paid for again, and again, and again.

So we put a **limit** on every tool. Look at the right side of the screen.

Read stops at four thousand lines.

Bash keeps only the first six thousand and the last six thousand characters.

List files gives at most five hundred entries.

Grep gives at most two hundred results.

Why the first part and the last part for bash? Because in a long log, the useful part is usually at the start and at the end. The error is almost always at the bottom.

`[OPTIONAL]`

And what about a really big file? Look at the bottom of the screen. You read it in pieces. Chunk one, then chunk two, then chunk three. This is how Pi's read tool handles large files.

`[END OPTIONAL]`

`[TAKEAWAY]`

Two rules. **Help the next step.** And **keep the output small.**

> `[WRITE]`
> **TWO RULES FOR ANY TOOL**
> 1. Help the model's NEXT step
> 2. Keep the output SMALL (it is paid for on every later turn)
> Limits: read 4,000 lines · bash first 6,000 + last 6,000 · list 500 · grep 200

`[STOP]`

### Beat 4.3 — The edit tool · about 3 min

![Diagram 09](../assets/lecture-3/diagrams/diagram-09.png)
*Diagram 09 — Edit beats overwrite*

`[OPEN]`

Out of the six tools, one deserves special attention. The **edit** tool. Because the way you design it decides how reliable your agent feels.

`[EXPLAIN]`

There are two ways to let a model change a file.

Way one is **overwrite**. The model writes the whole file again, from top to bottom.

Way two is **edit**. The model says only: "replace this old piece with this new piece."

Let me show you the difference with numbers.

![Board drawing draw-09-extra-500-line-file.png](../assets/lecture-3/drawings-to-copy/draw-09-extra-500-line-file.png)
*Board drawing — or just write the numbers below*

> `[WRITE — slowly, while speaking]`
> File = 500 lines. I want to change 3 lines.
> OVERWRITE → model types 500 lines → 497 chances for a mistake
> EDIT → model sends about 6 lines

Suppose the file has five hundred lines. And I want to change only three.

With overwrite, the model types all five hundred lines again. That means four hundred and ninety-seven lines which it was not supposed to touch. Four hundred and ninety-seven chances for a small mistake.

With edit, the model sends about six lines. The old piece, and the new piece. The rest of the file is never touched.

So edit is much safer.

Now, edit has **one rule**. Look at the bottom of the screen.

The old piece of text must appear **exactly once** in the file.

If it appears **zero** times, the model has remembered the text wrongly. We answer: not found. Read the file and copy it exactly.

If it appears **many** times, we do not know which one it means. We answer: it appears so many times. Give more context.

If it appears exactly **once**, we make the change.

Now look at those two error messages again.

Each one tells the model **what to do next**. "Read the file." "Give more context."

This is very important. An error message in a tool is not written for a human. It is written for the **model**, so that its next try is correct.

`[OPTIONAL]`

`[ASK]`

Here is a small puzzle. Pause and think.

Suppose the error message said only: "Error. The snippet appears three times." And nothing more.

The model tries again with the same text. It fails. It tries again. It fails. Why?

*[wait two seconds]*

Because the message did not tell it what to do differently. The model is not the problem. The message is. Add "give more context", and it works.

`[END OPTIONAL]`

`[TAKEAWAY]`

Change only what you must. And when you refuse, **say what to do next**.

> `[WRITE]`
> **EDIT: the old text must appear EXACTLY ONCE**
> 0 times → "not found — read the file and copy it exactly"
> many times → "give more context"
> **An error message is written for the model's next try.**

`[STOP]`

### Beat 4.4 — bash: powerful and dangerous · about 2 min

![Diagram 10](../assets/lecture-3/diagrams/diagram-10.png)
*Diagram 10 — bash: the universal appliance*

`[OPEN]`

And now the sixth tool. The powerful one. Bash.

`[EXPLAIN]`

The other five tools only move text in and out of files.

Bash is different. Bash **runs programs**.

Look at the left side of the screen. What does bash give us?

It runs the tests. It starts servers. It runs git. It installs packages.

And most important of all: it lets the agent **check its own work**.

Without bash, the agent can only say, "I think it works." With bash, it can run the code and see.

Now look at the right side. The danger.

The same tool can delete your files. It can download something from the internet and run it. It can overwrite your team's work.

So, before anything else, we give bash two simple guards.

**Guard one is a timeout.** If a command takes more than one hundred and twenty seconds, we stop it. Otherwise one stuck command would freeze the whole agent.

**Guard two is the output limit**, which we already saw. The first six thousand and the last six thousand characters.

And one small detail. If a command prints nothing, we do not send back an empty answer. We send back a small message which says: it ran, and there was no output. So the model is never confused.

`[TAKEAWAY]`

Bash is what makes the agent a real engineer. And bash is the reason we need security.

> `[WRITE]`
> **bash** gives: tests · servers · git · install · **checking its own work**
> **bash** risks: deleting · downloading and running · overwriting
> Guard 1: timeout (120 s) · Guard 2: output limit

`[STOP]`

### Recap of Part 2 · about 30 sec

`[OPEN]`

So that is part two.

`[TAKEAWAY]`

Here it is in three lines.

One. Six tools are enough. Read, write, edit, bash, list, and grep.

Two. Every tool helps the next step, and keeps its output small.

Three. Bash is the most useful tool, and the most dangerous.

And that last line takes us to the second half of the lecture.

`[STOP — three seconds]`

> **NATURAL BREAK.** If you want two shorter videos, end the first one here. Say: "In the next video, we make all of this safe, and then we build it." Start the next video with Beat 0.2 (the four parts) and a one-minute recap.

---
---

# PHASE 5 — Why security

*Goal of this phase: the viewer feels why security is needed, and knows the three protections that are coming.*

`[PHASE CHANGE — pause three seconds]`

Now we start **part three of four**. And honestly, this is the part I care about the most.

Security.

### Beat 5.1 — Who stops a dangerous command? · about 2.5 min

`[OPEN]`

Let me ask you one question.

`[EXPLAIN]`

Suppose you build a harness. You give it to people. And one day, it deletes somebody's files.

What happens to your product?

Nobody uses it again. One incident is enough.

So security is not something you add at the end. It has to be part of the design, from the first day.

Now a second question. Who is responsible for stopping a dangerous command? Is it the model?

No. The model will **not** stop itself. If the model thinks that deleting a folder will help, it will ask to delete the folder.

It is the job of the **harness**. It is the job of our code.

Let me draw this.

![Board drawing draw-03-intern-and-senior.png](../assets/lecture-3/drawings-to-copy/draw-03-intern-and-senior.png)
*Board drawing — follow the numbers 1, 2, 3, 4*

*[while drawing the small figure at the keyboard]*

Imagine a new intern. This intern types a hundred times faster than you. He never gets tired. And he will run anything which he thinks might help.

That intern is the **model**.

*[while drawing the second figure, with a hand on his shoulder]*

Now imagine an experienced person, standing behind him, with a hand on his shoulder.

*[while drawing the speech bubble]*

Before anything risky, she says: "Wait. Are you sure?"

That person is the **harness**. That is what we are building today.

`[TAKEAWAY]`

The model **asks**. The harness **decides**.

> `[WRITE — at the bottom of the drawing]`
> We are not building the intern. We are building the person standing behind him.

`[STOP]`

### Beat 5.2 — The three protections · about 1.5 min

`[OPEN]`

So how do we build that experienced person? With three protections. Let me first list them. Then we will take them one by one.

`[EXPLAIN]`

Protection one is the **gate**. The gate decides **what** is allowed to run.

Protection two is the **jail**. The jail decides **which folder** the agent can reach.

Protection three is the **backend**. The backend decides **on which machine** the command runs.

So. What may run. Where it can reach. And on which machine.

Please keep this list on the board. For the next twenty minutes, I will keep pointing at it.

`[TAKEAWAY]`

Three protections. The gate, the jail, and the backend. We start with the gate.

> `[WRITE — keep this on the board for the rest of Part 3]`
> **THREE PROTECTIONS**
> 1. THE GATE → WHAT may run
> 2. THE JAIL → WHICH FOLDER it can reach
> 3. THE BACKEND → ON WHICH MACHINE it runs

`[STOP]`

---
---

# PHASE 6 — Protection 1: the gate

*Goal of this phase: the viewer knows the three questions of the gate, the three modes, and what happens when a call is blocked.*

`[PHASE CHANGE — point at line 1 on the board]`

Protection number one. **The gate.**

### Beat 6.1 — One checkpoint, three questions · about 3 min

`[OPEN]`

The idea of the gate is very simple.

`[EXPLAIN]`

Before any tool runs, it has to pass through one checkpoint. Every tool call. Every time. No exceptions.

Remember socket two, from the beginning of the lecture? The function called `before_tool`? This gate is what we plug into it.

Now, at this checkpoint, we ask **three questions**. In a fixed order. Let me draw it.

![Board drawing draw-04-funnel.png](../assets/lecture-3/drawings-to-copy/draw-04-funnel.png)
*Board drawing — follow the numbers 1, 2, 3, 4*

*[while drawing the funnel and the top band]*

**Question one. Is this command on the "never" list?**

There are a few commands which must never run, whatever happens. If the command is on that list, we stop it right here.

*[while drawing the middle band]*

**Question two. Which mode are we in?**

There are three modes. I will explain them in a minute. The mode decides whether this kind of action is allowed automatically.

*[while drawing the bottom band]*

**Question three. Does a human say yes?**

If the first two questions could not decide, we ask the person.

*[while drawing the green box at the bottom]*

And if the call passes all three, it runs.

![Diagram 11](../assets/lecture-3/diagrams/diagram-11.png)
*Diagram 11 — One checkpoint, three layers*

Here is the same thing, drawn neatly.

Look at the red boxes on the right. Whenever a call is stopped, we send back a message. It says "blocked", and it gives the reason.

Now, why this order? Why is the "never" list first?

Think about it. If the "never" list is first, then **nothing can cancel it**. No mode can cancel it. And no tired person, who clicks "yes" at two in the night without reading, can cancel it.

It is like airport security. Most people walk straight through. Some are checked by hand. And a very few are never allowed on the plane.

`[TAKEAWAY]`

One checkpoint. Three questions. **Never list**, then **mode**, then **human**.

> `[WRITE]`
> **THE GATE — 3 questions, in this order**
> 1. Is it on the NEVER list? → blocked
> 2. Which MODE are we in?
> 3. Does a HUMAN say yes?
> Never list is first, so nothing can cancel it.

`[STOP]`

### Beat 6.2 — The three modes · about 2.5 min

![Diagram 12](../assets/lecture-3/diagrams/diagram-12.png)
*Diagram 12 — The dial: read-only, safe, yolo*

`[OPEN]`

Now let us look at the second question. The modes. There are three, and you will use them every day.

`[EXPLAIN]`

**Mode one. Read-only.**

The agent can only look. It can read files, list files, and search. It cannot change anything.

When do you use it? When you point the agent at a project for the first time, and you do not trust it yet.

**Mode two. Safe.**

This is the normal mode. Reading is allowed automatically. But anything which **changes** something needs a yes from a human. Writing a file. Editing a file. Running a command. One at a time.

And there is one important detail about safe mode. What if there is no human connected?

Then the answer is **no**. Not yes. If nobody is there to approve, we refuse. That is the safe way to fail.

**Mode three. Yolo.**

In this mode, everything is approved automatically.

That sounds dangerous. But it has a real use. Think of an agent which runs through the night. Nobody is awake to click "yes". So you need this mode.

But there is a condition. Yolo is acceptable only when the agent is locked in a safe place.

And in Zill, we **enforce** that. If you choose yolo, and bash is running directly on your own computer, Zill refuses. I will show you the safe place in a few minutes.

And remember: even in yolo, the "never" list still works.

If you have used Claude Code, you already know this idea. Its normal mode asks you before it runs a command. And it has another mode which skips the questions. It is the same dial.

`[TAKEAWAY]`

Read-only, to **look**. Safe, to **ask**. Yolo, only in a **safe place**.

> `[WRITE]`
> **THREE MODES**
> read-only → can only look
> safe → asks before any change (nobody there = NO)
> yolo → approves everything, only in a safe place

`[STOP]`

### Beat 6.3 — The "never" list, and what a block looks like · about 3 min

![Diagram 13](../assets/lecture-3/diagrams/diagram-13.png)
*Diagram 13 — A deny rule firing, on the tape*

`[OPEN]`

Now the first question. The "never" list. What is on it?

`[EXPLAIN]`

Look at the bottom of the screen. Six things. I call them the six disasters.

One. Deleting everything in your home folder, or on your whole disk.

Two. Sudo. That means running a command with full administrator power.

Three. Formatting a disk.

Four. Downloading a script from the internet, and running it immediately.

Five. Force push. That can erase your team's work on GitHub.

Six. Writing directly onto a raw disk.

Now notice what is **not** on the list. Deleting a build folder inside your own project. That is allowed. Because that is normal, everyday work.

So the list does not ban a word like "delete". It bans **disasters**.

Now let us see what happens when one of these is tried. Look at the top of the screen. Read it with me.

The user says: "Please delete my home directory."

The model tries to do it.

And look at the red line. The answer comes back: **blocked**. This command matches a rule on the "never" list.

There are two things to notice here.

First. Nothing crashed. The harness did not stop. The model simply received a message.

Second. Look at what the model does next. It reads the reason. It says, "I should not do that." And it suggests something safer. It looks inside the project, and it finds a big folder which is safe to remove.

So a refusal is not the end of the conversation. It is just one more piece of information for the model.

Now, one honest warning.

These rules are patterns over text. And a clever command can sometimes slip past a pattern.

So the "never" list is a strong first wall. But it must **never be your only wall**.

And that is exactly why we need the second protection.

`[TAKEAWAY]`

We ban disasters, not words. And a blocked call gets **an answer**, not a crash.

> `[WRITE]`
> **THE NEVER LIST — 6 disasters**
> delete home / disk · sudo · format a disk · download-and-run · force push · write to a raw disk
> Blocked = a message to the model, **not a crash**
> The never list is the first wall, never the only wall.

`[STOP]`

---
---

# PHASE 7 — Protection 2: the jail

*Goal of this phase: the viewer understands the jail, the term "blast radius", and why we need both the gate and the jail.*

`[PHASE CHANGE — point at line 2 on the board]`

Protection number two. **The jail.**

### Beat 7.1 — One folder, and nothing outside it · about 2.5 min

![Diagram 14](../assets/lecture-3/diagrams/diagram-14.png)
*Diagram 14 — The jail and the blast radius*

`[OPEN]`

The gate checks **what** the command is. But it does not check **where** the command reaches.

`[EXPLAIN]`

Think about it. Reading a file is allowed. Fine. But **which** file?

What if the agent reads your secret keys? What if it reads a file from another project?

So we need a second protection.

Look at the screen. The green box is one folder. Our project folder. We call it the working directory.

This is the **only** place where the agent is allowed to work.

Inside the box, it is free. It can read, write, and edit.

Outside the box are your secret keys, your system files, your other projects. The agent can never reach them.

How does it work? Very simply. Every time a tool wants to touch a file, the path goes through one small check. It has three steps.

Step one. Attach the path to our project folder.

Step two. Clean it up. Remove tricks like "dot dot slash", which means "go one folder up".

Step three. Ask one question. Is the final path still inside our folder?

If yes, go ahead. If no, stop, with an error.

Now look at the red line in the picture.

The agent tries to read "dot dot slash, dot dot slash, etc, passwd". That means: go up two folders, and read a system file.

The check catches it.

And once again, it is not a crash. The error goes back to the model as a message.

`[TAKEAWAY]`

The gate decides **what** may run. The jail decides **where** it can reach.

> `[WRITE]`
> **THE JAIL = one folder**
> Every path: attach to our folder → clean it → still inside? → if not, ERROR
> Outside the folder = never reachable

`[STOP]`

### Beat 7.2 — Blast radius · about 2 min

`[OPEN]`

Now I want to give you one term. I think it is the most useful term in all of security.

**Blast radius.**

`[EXPLAIN]`

Let me draw it.

![Board drawing draw-05-firecracker-bucket-vs-warehouse.png](../assets/lecture-3/drawings-to-copy/draw-05-firecracker-bucket-vs-warehouse.png)
*Board drawing — follow the numbers 1, 2, 3, 4*

*[while drawing the bucket and the small firecracker]*

Take a small firecracker. Put it inside a steel bucket, and light it.

What is the damage? A few inches. Nothing.

*[while drawing the warehouse and the big explosion]*

Now take the **same** firecracker. Put it inside a warehouse full of fireworks. And light it.

Now the whole building is gone.

Same firecracker. Same mistake. But a completely different result.

The size of the damage is called the **blast radius**.

Why does this matter for us?

Because we cannot stop the model from making mistakes. It **will** make mistakes sometimes. That is its nature.

But we can control the room in which the mistake happens. We can make that room small.

The jail is our steel bucket.

`[TAKEAWAY]`

We cannot stop every mistake. But we can keep every mistake **small**.

> `[WRITE — at the bottom of the drawing]`
> **Blast radius** = how far the damage reaches when something goes wrong.

`[STOP]`

### Beat 7.3 — Why we need both · about 1.5 min

`[OPEN]`

Now you may ask: if we have the gate, why do we need the jail? And if we have the jail, why do we need the gate?

`[EXPLAIN]`

Because they stop different things.

The **gate** makes bad actions happen **less often**.

The **jail** makes sure that when a bad action does get through, the damage is **small**.

And something will always get through. The model is fast. And we are only human.

`[OPTIONAL]`

![Board drawing draw-06-three-rings.png](../assets/lecture-3/drawings-to-copy/draw-06-three-rings.png)
*Board drawing*

You can picture it as three rings around the agent. The outer ring is the jail. The middle ring is the "never" list. The inner ring is the mode and the human. If one ring fails, the next one catches it.

`[END OPTIONAL]`

So here is the one question you should ask about any agent.

**When the model is wrong, what is the worst thing that can happen?**

For Zill, the answer is: a mess inside one folder. And git can undo that.

That is an answer I can live with.

`[TAKEAWAY]`

The gate means **fewer** mistakes. The jail means **smaller** mistakes. We need both.

> `[WRITE]`
> GATE → fewer mistakes · JAIL → smaller mistakes
> Always ask: "When the model is wrong, what is the worst that can happen?"

`[STOP]`

---
---

# PHASE 8 — Protection 3: the backend

*Goal of this phase: the viewer understands that "what a tool does" and "where it runs" are separate, and knows the three backends.*

`[PHASE CHANGE — point at line 3 on the board]`

Protection number three. **The backend.** This one answers a question which most people never ask.

### Beat 8.1 — Where does a tool run? · about 2.5 min

`[OPEN]`

When you learn about tools, you learn **what** a tool does. But nobody asks: **where** does it run? On which machine?

`[EXPLAIN]`

Pi has a very nice idea here. Pi separates these two things. What a tool does. And where it runs.

Let me draw it.

![Board drawing draw-07-operations-switch.png](../assets/lecture-3/drawings-to-copy/draw-07-operations-switch.png)
*Board drawing — follow the numbers 1, 2, 3, 4*

*[while drawing the top box]*

At the top is the tool. Say, bash.

*[while drawing the middle box with the small lever]*

Under it is a small layer. Think of it as a switch.

*[while drawing the three boxes at the bottom]*

And under the switch are three places.

Place one. **Local.** Your own computer. It is the fastest. But for bash it is the most risky, because your real files are there.

Place two. **SSH.** That simply means a remote machine. Another computer, somewhere else, which you connect to. If something goes wrong, it goes wrong there. Not on your laptop.

Place three. **Sandbox.** This is a locked room inside your own computer. The command runs inside that room, and it can touch only what is in the room.

![Diagram 15](../assets/lecture-3/diagrams/diagram-15.png)
*Diagram 15 — Where a tool runs*

And here is the best part. You can choose the place for the **whole project**. Or you can choose it for **each tool separately**.

For example: bash in the sandbox. And read on your own computer.

`[TAKEAWAY]`

What a tool does is one thing. Where it runs is another. Keep them **separate**.

`[STOP]`

### Beat 8.2 — How Zill does it · about 2.5 min

![Diagram 20](../assets/lecture-3/diagrams/diagram-20.png)
*Diagram 20 — Zill's operations layer*

`[OPEN]`

So we are going to build the same idea into Zill.

`[EXPLAIN]`

Look at the screen. At the top are our six tools.

In the middle is a layer called **operations**. It lives in a file called `operations.py`.

Here is the rule. Our tools never touch the disk themselves. They never start a command themselves.

They always ask this middle layer. "Please read this file." "Please run this command."

And the middle layer passes it on to one of three backends. The same three places. Local. Sandbox. And SSH.

Let me say one line about each.

**Local** runs on your computer. And the jail, which we just saw, lives here.

**Sandbox** runs the command in a clean room. And the most useful thing it does is this: it **hides your secrets**. Your API keys normally sit in your computer's environment. Inside the sandbox, the command cannot see them.

**SSH** runs the command on a remote machine, using the normal ssh program.

And how do you choose? With two settings. You can see them at the bottom of the screen.

The first setting chooses the backend for the whole project.

The second setting changes it for one tool. For example: bash in the sandbox, and everything else local.

And the code of the tool does not change at all.

`[TAKEAWAY]`

Tools say **what** to do. Operations decides **where** it is done.

> `[WRITE]`
> `tools.py` = WHAT · `operations.py` = WHERE
> **3 backends:** local (my PC) · sandbox (a locked room, hides secrets) · ssh (a remote machine)
> Choose for the whole project, or per tool

`[STOP]`

### Beat 8.3 — The honest limits · about 1.5 min

`[OPEN]`

Now let me be honest with you about the limits. Because being honest is part of security.

`[EXPLAIN]`

Our sandbox, in its normal form, stops **accidents**. A leaked secret. A command which never ends. A file which becomes too big.

It does **not** stop a determined attacker.

If you need that stronger protection, there are two choices. Our sandbox has a second form which uses Docker. In that form, the command has no internet at all. Or you use a remote machine.

One more honest point. The SSH part, the way we build it today, is tested with a pretend server. Not a real one. So before you trust it, try it once on a small machine of your own.

And now you can understand the rule about yolo, which I mentioned earlier.

Yolo means "approve everything". That is acceptable only when the blast radius is small.

So in Zill, yolo with bash on your own computer is **refused**. Move bash to the sandbox, or to a remote machine, and then it is allowed.

`[TAKEAWAY]`

Know what your protection really does. And say it honestly.

`[STOP]`

### Recap of Part 3 · about 45 sec

`[OPEN]`

That finishes part three. It was the longest part. So let me say it slowly.

`[TAKEAWAY — point at the three lines on the board]`

One. The **gate** decides what may run. Three questions: the never list, the mode, the human.

Two. The **jail** decides where the agent can reach. One folder.

Three. The **backend** decides on which machine it runs. Local, sandbox, or remote.

What. Where. And on which machine.

`[STOP — three seconds]`

---
---

# PHASE 9 — The whole picture

*Goal of this phase: the viewer sees everything from today in one picture, before the build.*

`[PHASE CHANGE — pause three seconds]`

Now we start the last part. **Part four of four.** We put everything together, and then we build it.

### Beat 9.1 — The journey of one tool call · about 2.5 min

![Diagram 17](../assets/lecture-3/diagrams/diagram-17.png)
*Diagram 17 — What happens to one tool call today*

`[OPEN]`

Before we build, let me show you the whole lecture in one picture.

`[EXPLAIN]`

This is the journey of one single tool call. Follow it with me, from left to right.

Start at the purple box. The model reads the contracts, and picks a tool. **That was part one.**

Next, the yellow diamond. The safety check. That is the gate and the jail. **That was part three.**

If it is safe, go to the right. The harness runs the tool. Then the result is added to the messages array. And we go back around the loop. **That was lecture two.**

If it is **not** safe, go down. We ask the human.

If the human says yes, we run it.

If the human says no, we tell the model: blocked, and why. And then the model suggests another way.

Now look at the whole picture once more.

Is there any arrow where the program crashes?

No. There is none.

A tool can fail. A tool can be refused. But the loop never crashes. The error simply becomes a message for the model.

And models are very good at reading an error message and correcting themselves.

`[TAKEAWAY]`

A failed tool, or a refused tool, is never a crash. It is a **message**.

> `[WRITE]`
> contract → pick a tool → **safety check** → run → add result → loop
> not safe → ask human → no → tell the model why → it tries another way
> **An error is a message, never a crash.**

`[STOP]`

`[OPTIONAL — Beat 9.2 can be skipped completely]`

### Beat 9.2 — One more level: who is the user? · about 2 min

![Diagram 16](../assets/lecture-3/diagrams/diagram-16.png)
*Diagram 16 — Three levels of security*

`[OPEN]`

Let me share one thing from real work with companies. It is short, but it is valuable.

`[EXPLAIN]`

So far we have seen two kinds of control. Control over the tool call. And control over files and folders.

There is a third kind. Control **by user**. Meaning: which **person** is allowed to use which tool.

![Board drawing draw-08-enterprise-tree.png](../assets/lecture-3/drawings-to-copy/draw-08-enterprise-tree.png)
*Board drawing*

Think of a big company. It has many countries. Each country has units. Each unit has teams.

And not everybody should be able to use every tool.

Companies care about this very much. Often more than they care about how smart the agent is.

And here is the interesting part. The open-source harnesses do not do this today. Zill does not do it either.

So it is a real gap. If you can build a harness which is safe, and which a company can control person by person, that is very valuable. I am telling you this from experience.

`[TAKEAWAY]`

Three levels of security. The tool call. The files. And the **user**. The third one is still open.

`[STOP]`

`[END OPTIONAL]`

### Beat 9.3 — Four levels of understanding · about 1.5 min

![Diagram 18](../assets/lecture-3/diagrams/diagram-18.png)
*Diagram 18 — Four levels of depth on tools*

`[OPEN]`

One last idea before we build. And this one is for your career.

`[EXPLAIN]`

Suppose somebody asks you: "What is a tool?"

There are four levels at which you can answer.

Level one. "A tool lets the model access the outside world." That is correct. And that is where most people stop.

Level two. You can explain the **contract**. The interface and the implementation.

Level three. You can explain how to **gate** a tool call. Never, ask, allow.

Level four. You can explain **where** the tool runs. Local, remote, or sandbox.

After today, you are at level four.

So if somebody asks you to write a tool, do not just write a function. Say this: "First the contract. Then the code. Then the gate. Then where it runs."

`[TAKEAWAY]`

Most people know level one. You now know all four.

> `[WRITE]`
> **4 LEVELS:** 1 what a tool is · 2 the contract · 3 the gate · 4 where it runs
> "Contract first. Then code. Then the gate. Then where it runs."

`[STOP]`

---
---

# PHASE 10 — The build

*Goal of this phase: build the three files with a coding agent, and show five short demos.*

`[PHASE CHANGE — pause three seconds]`

Alright. Now we build it.

### Beat 10.1 — What we are building · about 1 min

![Diagram 19](../assets/lecture-3/diagrams/diagram-19.png)
*Diagram 19 — What we build today*

`[OPEN]`

Look at the screen. This is everything we build today.

`[EXPLAIN]`

We write three files.

`operations.py`. It decides where a tool runs.

`tools.py`. It has our six tools.

`security.py`. It has the gate and the three modes.

And we also write tests, to check that everything works.

And what do we **not** touch? `loop.py`. And `provider.py`. They stay exactly as they were.

Just like last time, we will not type this code by hand. We write a careful prompt, and we give it to a coding agent.

So please open the same project, and the same coding agent, which you used in the last lecture.

`[STOP]`

### Beat 10.2 — The prompt · about 2 min

`[OPEN]`

Here is the prompt. It is long. So let me first explain how it is organised. Then it will not look scary.

`[EXPLAIN]`

It has six blocks.

Block one. The ground rules. No extra packages. Do not change the old files.

Block two. Operations. The three backends.

Block three. Tools. The six tools, with every error message written out.

Block four. Security. The never list, and the three modes.

Block five. The tests.

Block six. A list of checks, which the agent must run at the end, and report honestly.

`[SCREEN → the terminal. Paste the prompt below. Scroll slowly. Point at each block as you name it.]`

```text
You are building the next part of Zill (lecture 3 of the series): the tools, the
execution backends (local / ssh / sandbox) and the permission gate. The parts are
cumulative: your repo already contains the package zill/ with provider.py (the
model client: neutral message format, retry with backoff) and loop.py (run_loop
with on_event and before_tool sockets), plus demos/. Do NOT rewrite or edit
provider.py or loop.py. Today plugs into the sockets they already expose:
tools is a dict name -> Tool (each with .spec and .run), and before_tool(call)
receives {"name", "args"} and returns None to allow or a reason string to block.
If you believe loop.py or provider.py must change, stop and report why instead
of changing them.

GROUND RULES
- Python 3.10+, standard library only, no third-party packages.
- Must run on Windows, macOS and Linux. Anything POSIX-only (resource limits,
  process groups) must be guarded and must degrade with a clear, documented
  message, never crash on import.
- Same code standard as before: a module docstring on every file naming the
  concept it teaches and the design rules it embodies; a docstring on every
  public function; a short comment wherever behaviour is subtle (the
  uniqueness rule, the jail, fail-closed behaviour).
- Size targets including documentation, within ~15%: operations.py 140 lines,
  tools.py 170, security.py 70, tests 130. Landing far under target means
  documentation was skipped.
- Commit after each milestone: operations, tools, security, tests, demo.
- Do not add features beyond this spec. Where the spec is ambiguous, pick the
  simpler option and note it in a one-line comment at the top of the file.

THE ONE IDEA TO PRESERVE
WHAT a tool does lives in tools.py. WHERE it runs lives in operations.py. Tools
never import subprocess and never touch the filesystem directly; every file or
command operation goes through an Operations object. The same six tools must
work unchanged on all three backends, and the backend can be chosen for the
whole project or for one tool at a time (for example: bash in the sandbox while
read_file stays local).

FLOW OF ONE TOOL CALL
model asks -> security.Policy.check (the before_tool socket) -> Tool.run ->
Operations backend -> result string -> appended to messages by the loop.
Every failure becomes a string result; nothing in this layer may crash the loop.

------------------------------------------------------------------------------
1) zill/operations.py  — where a tool runs
------------------------------------------------------------------------------
IGNORE = {".git", "node_modules", "__pycache__", ".venv"}

class Operations (base class; document it as the interface every backend meets)
  name: str                                   # "local" | "ssh" | "sandbox"
  resolve(path) -> str                        # safe path inside the root, or
                                              # raise PermissionError(
                                              #   f"{path!r} escapes the working directory")
  read_text(path) -> str
  write_text(path, content) -> None           # creates parent directories
  walk() -> list[str]                         # relative POSIX-style file paths
                                              # under the root, skipping IGNORE, sorted
  run(command, timeout) -> tuple[str, int]    # (stdout+stderr combined, exit code);
                                              # raise TimeoutError on timeout

class LocalOps(Operations)  name = "local"
  - root = os.path.realpath(workdir).
  - resolve: join onto root, realpath (flattens symlinks and ".."), then require
    the result equals root or starts with root + os.sep (compare with
    os.path.normcase so Windows is case-insensitive). Anything else raises the
    PermissionError above. This single function is the path jail.
  - run: subprocess.run(command, shell=True, cwd=root, capture_output=True,
    text=True, errors="replace", timeout=timeout). Map subprocess.TimeoutExpired
    to TimeoutError.

class SandboxOps(LocalOps)  name = "sandbox"   (a jail inside your own OS)
  Same file operations as LocalOps (still path-jailed); only run() changes.
  Two tiers, chosen by env ZILL_SANDBOX ("process" default, or "docker"):
  - "process" tier: run the command with a SCRUBBED environment containing only
    PATH, LANG, and on Windows SYSTEMROOT and TEMP, plus HOME and TMPDIR set to
    the root. So secrets in the parent environment (API keys, tokens) never
    reach the command. cwd = root. On POSIX: start_new_session=True so a timeout
    kills the whole process group, and a preexec_fn applies resource limits
    (RLIMIT_CPU = timeout + 5 seconds, RLIMIT_FSIZE = 100 MB, RLIMIT_NOFILE =
    256) inside try/except. On Windows: no rlimits; on timeout kill the process
    tree with taskkill /T /F.
  - "docker" tier (opt-in, only if the docker binary is on PATH, otherwise raise
    RuntimeError("docker not found on PATH")): run
      docker run --rm --network none --memory 512m --cpus 1 --pids-limit 128
        -v <root>:/work -w /work <image> sh -c <command>
    with image from ZILL_SANDBOX_IMAGE (default "python:3.12-slim"). Only the
    root is mounted; no network.
  - describe() -> str returns exactly what is enforced right now (tier, whether
    rlimits are active, whether network is blocked), so demos and tests print
    the truth. Docstring must state plainly: the process tier prevents
    accidents (secret leakage, runaway CPU, giant files, orphan processes); it is
    NOT a security boundary against a determined attacker. The docker tier adds
    real network and filesystem isolation.

class SSHOps(Operations)  name = "ssh"   (dangerous work stays off your machine)
  SSHOps(host, remote_root, ssh_args=(), runner=subprocess.run)
  - Uses only the system ssh binary through ONE helper _ssh(remote_command,
    stdin=None, timeout=None) that builds: ["ssh", "-o", "BatchMode=yes",
    "-o", "ConnectTimeout=10", *ssh_args, host, remote_command]. Never disable
    host-key checking. If the ssh binary is missing raise RuntimeError("ssh not
    found on PATH"). `runner` is injectable so tests never touch a network.
  - Every user-controlled string placed into a remote command goes through
    shlex.quote. No exceptions.
  - resolve: posixpath.normpath(posixpath.join(remote_root, path)); reject
    lexically (PermissionError as above) if it is not remote_root or under it,
    BEFORE any ssh call is made. Then fail closed: for existing paths confirm
    with `realpath -m -- <p>` on the remote that the real path is still under
    remote_root; if that check errors, treat it as an escape.
  - read_text: `cat -- <p>`. write_text: `mkdir -p <dir> && cat > <p>` with the
    content passed on stdin. walk: `cd <root> && find . -type f` pruning IGNORE
    directories, then strip the leading "./" and sort. run: `cd <root> && <command>`
    returning (combined output, exit code); subprocess timeout -> TimeoutError.

make_ops(kind, root, **opts) -> Operations
  kind in {"local","ssh","sandbox"}; anything else raises ValueError listing the
  valid kinds. "ssh" requires host and remote_root in opts.

ops_from_env(root, env=os.environ) -> dict[str, Operations]
  Returns a mapping for the six tool names (read_file, write_file, edit_file,
  bash, list_files, grep) -> Operations. Reads:
    ZILL_BACKEND         default "local"; applies to every tool
    ZILL_TOOL_BACKENDS   optional per-tool overrides, e.g. "bash=sandbox,read_file=local"
    ZILL_SSH_HOST, ZILL_SSH_DIR   required only if any tool uses "ssh"
  Share one Operations instance per kind. An unknown tool name in the overrides
  raises ValueError; "ssh" without host/dir raises ValueError with a message
  that names the missing variable.

------------------------------------------------------------------------------
2) zill/tools.py  — what a tool does
------------------------------------------------------------------------------
- Tool dataclass: name (str), spec (dict — the {"schema": ...} the provider
  expects), run (callable), backend (str, default "local").
- Decorator tool(description, **params): turns a plain function into a Tool. It
  reads the function's argument names, treats parameters with defaults as
  optional, and builds
    spec = {"schema": {"name": fn.__name__, "description": description,
      "parameters": {"type": "object",
        "properties": {param: {"type": "string", "description": text} ...},
        "required": [arguments without defaults]}}}
  All parameters are string-typed on purpose.
- core_tools(workdir, ops=None) -> list[Tool]: six tools. `ops` is a mapping
  tool name -> Operations (as returned by ops_from_env) or a single Operations
  applied to all; default is LocalOps(workdir). Each Tool.backend is set from its
  Operations.name. A tool talks ONLY to its own Operations object; tools.py must
  not import subprocess or open() files itself. Every path goes through
  ops.resolve first.
  1. read_file(path): contents with "N<TAB>line" numbering; past 4000 lines,
     truncate and append a line noting the total.
  2. write_file(path, content): create parent directories (via ops); return
     "Wrote <n> chars to <path>".
  3. edit_file(path, old, new): the snippet must appear exactly once.
     Zero matches: return "ERROR: snippet not found — read the file and copy it exactly".
     Several: return "ERROR: snippet appears N times — include more context to make it unique".
     On success replace once and return "Edited <path>". (Read and write both go
     through ops, so edit works on every backend.)
  4. bash(command, timeout="120"): ops.run with the timeout in seconds; on
     TimeoutError return "ERROR: timed out after <t>s"; past 12000 characters
     keep the first and last 6000 with a "... truncated ..." marker; empty
     output becomes "(exit <code>, no output)"; non-empty output is returned as is.
  5. list_files(pattern="**/*"): ops.walk(), fnmatch against the relative path
     and the basename; sorted; cap at 500 entries with an "and N more" line.
  6. grep(regex, pattern="*"): search file contents line by line over ops.walk()
     filtered by the glob `pattern`; skip files that cannot be decoded as text;
     results as "path:lineno: text" with lines clipped to 200 chars; cap at 200
     hits. An invalid regex returns "ERROR: invalid regex: <message>".
- Docstrings: each tool's description string is written for the MODEL (short,
  says what comes back and any rule that changes behaviour). The word "required"
  is applied only to what the function cannot run without.

------------------------------------------------------------------------------
3) zill/security.py  — the permission gate
------------------------------------------------------------------------------
- READ_TOOLS = {"read_file", "list_files", "grep"}.
- DENY_PATTERNS: regex strings checked against bash commands only:
    rm -rf variants (any flag order, e.g. -rf, -fr, -r -f) targeting / or ~ or $HOME
    \bsudo\b
    \bmkfs\b   or   \bdd\s+if=
    curl piped to sh/bash
    git push ... --force
    redirection onto /dev/sd devices
  `rm -rf build/` must NOT match.
- class Policy(mode="safe", approver=None, backends=None)
  mode is one of "read-only", "safe", "yolo" (anything else raises ValueError).
  approver is a callback (call, reason) -> bool, default refuses (the gate FAILS
  CLOSED). backends is a dict tool name -> backend name (build it from
  {t.name: t.backend for t in tools}).
  check(call) -> None (allow) or a reason string (block), in exactly this order:
    1. bash command matching a deny pattern: always blocked, in every mode,
       reason "command matches deny rule: <pattern>".
    2. READ_TOOLS: allowed.
    3. mode "yolo": if the call is bash and backends.get("bash","local") is
       "local" and env ZILL_ALLOW_LOCAL_YOLO != "1", block with
       "yolo + bash needs the sandbox or ssh backend (set ZILL_BACKEND=sandbox)".
       Otherwise allow.
    4. mode "read-only": block with "policy is read-only; only read/list/grep tools are allowed".
    5. mode "safe": ask the approver; anything but a true answer is blocked with
       "not approved by user".
  The jail (path resolution) is deliberately NOT repeated here: the gate decides
  WHAT may run, the jail decides WHERE it can reach, and each is a separate layer.

------------------------------------------------------------------------------
4) demos/build_demo.py
------------------------------------------------------------------------------
- Create a temporary scratch directory. os.environ.setdefault("ZILL_BACKEND",
  "sandbox"). ops = ops_from_env(scratch); tools = core_tools(scratch, ops).
- Print one line per tool: "<tool> -> <backend>", and print the SandboxOps
  describe() text so the audience sees what is really enforced on this machine.
- policy = Policy("yolo", backends={t.name: t.backend for t in tools}); build the
  tools dict {t.name: t}; call run_loop with before_tool=policy.check and a
  printing on_event. The task comes from argv, default: "Create fib.py with an
  iterative fib(n), a __main__ printing fib(30), run it and confirm the output is 832040".

------------------------------------------------------------------------------
5) tests/test_zill_tools.py  — stdlib unittest, no network, no real ssh/docker
------------------------------------------------------------------------------
Use temporary directories only. Cover at least:
  1. resolve blocks "../../etc/passwd", an absolute path outside the root, and a
     symlink that points outside (skip the symlink case if the OS refuses to
     create symlinks).
  2. edit_file: zero matches, N matches, and success each return the exact text above.
  3. read_file numbering, and truncation past 4000 lines.
  4. write_file creates missing parent directories.
  5. bash: timeout returns the "ERROR: timed out after Ns" text (use a short
     python sleep command); empty output becomes "(exit 0, no output)"; output
     longer than 12000 chars is truncated with the marker.
  6. Policy: each deny pattern blocks a sample command; "rm -rf build/" is allowed;
     read-only blocks writes; safe with the default approver refuses; safe with
     an approving callback allows; yolo + bash on "local" is refused unless
     ZILL_ALLOW_LOCAL_YOLO=1; yolo + bash on "sandbox" is allowed; a bad mode
     raises ValueError.
  7. SandboxOps scrubs the environment: set os.environ["ZILL_TEST_SECRET"]="x",
     run a python one-liner through SandboxOps that prints it, and assert it is
     NOT visible, while PATH still works. Also assert describe() returns a string.
  8. SSHOps with a fake runner: assert the command contains BatchMode=yes, that
     user-controlled strings are shlex-quoted (try a path containing a space and
     a quote), that "../x" is rejected BEFORE the fake runner is called, and that
     a missing ssh binary raises RuntimeError.
  9. make_ops / ops_from_env: default is all "local"; "ZILL_TOOL_BACKENDS=bash=sandbox"
     routes only bash; an unknown backend or unknown tool name raises ValueError;
     "ssh" without ZILL_SSH_HOST raises ValueError naming the variable.
 10. tool decorator: required list excludes parameters with defaults; every
     parameter type is "string".
Run: python -m unittest discover -s tests -v   — everything must pass.

------------------------------------------------------------------------------
6) Verify before finishing — report each result honestly
------------------------------------------------------------------------------
(a) The unit tests all pass.
(b) Live capability: with ZILL_BACKEND=sandbox, the default fib task completes
    with a verified answer 832040.
(c) Restraint: the task "Delete my home directory" produces a BLOCKED tool
    result and a civil refusal from the model.
(d) The jail: asking it to read ../../etc/passwd surfaces the PermissionError as
    an ERROR tool result, not a crash.
(e) Backend switch: run once with ZILL_BACKEND=local and once with
    ZILL_BACKEND=sandbox after setting a fake secret in the environment
    (e.g. FAKE_SECRET=1). Show that a bash command printing that variable sees
    it on local and does NOT see it in the sandbox. (Remember Policy refuses
    local+yolo bash, so use ZILL_ALLOW_LOCAL_YOLO=1 or mode "safe" with an
    auto-approver for the local run.)
(f) Per-tool routing: with ZILL_TOOL_BACKENDS=bash=sandbox and ZILL_BACKEND=local,
    the printed table shows bash -> sandbox and the other five -> local.
(g) git log shows the commits; print a final table of file, line count and a
    one-line purpose; list every deviation from this spec and every limitation you
    know of (especially: what SandboxOps does NOT protect against, and that the
    SSH backend was tested only with a fake runner, not a real server).
```

`[STOP — press Enter and let it run]`

### Beat 10.3 — While it runs · about 1.5 min

`[OPEN]`

While this is running, I want you to notice three things about the prompt.

`[EXPLAIN]`

First. It is **exact**. It does not say "write some tools". It says which functions, and which error messages. The more exact you are, the better the result.

Second. It says: do not change `loop.py`. If you think it must change, stop and tell me. That protects the work we did in the last lecture.

Third. The last line asks the agent to list everything it did **not** protect against. I always add this line. It makes the agent tell you the weak points, instead of you finding them later.

`[TAKEAWAY]`

A good prompt is exact, it protects old work, and it asks for the weak points.

`[STOP — wait for the build to finish]`

### Beat 10.4 — Five short demos · about 5 min

`[OPEN]`

It is finished. Now let us test it. One step at a time.

**First, the tests.**

`[DO: run]` `python -m unittest discover -s tests -v`

`[SAY]` First, the tests. Everything should pass. … Good.

`[STOP]`

**The backend table.**

`[DO: start the demo. It prints which backend each tool uses.]`

`[SAY]` Look at this small table. It shows which backend each tool is using. And it shows what the sandbox really protects on **my** computer. Let me read it out.

*[read the table aloud, exactly as it is printed]*

`[STOP]`

**Demo 1 — it can build.**

`[DO: run the default task — create fib.py and run it.]`

`[SAY]` I am asking it to create a small program and run it. Watch the loop.

It writes the file. It runs the file. It reads the output. And only then, it gives the answer.

It did not guess. It **checked**.

`[STOP]`

**Demo 2 — it refuses a disaster.**

`[DO: ask]` "Delete my home directory."

`[SAY]` Now I ask it to delete my home directory. Watch.

There. **Blocked.** The never list caught it. And see how the model replies. It says no, politely, and it offers something safer.

`[STOP]`

**Demo 3 — it cannot leave the folder.**

`[DO: ask]` "Read the file ../../etc/passwd"

`[SAY]` Now I ask it to read a file outside our folder.

And there is the error. A permission error. It came back as a message. Nothing crashed.

That is the jail.

`[STOP]`

**Demo 4 — the same command, two places.**

`[DO: set a fake secret, for example FAKE_SECRET=1. Run a command that prints it, first on the local backend, then on the sandbox backend.]`

`[SAY]` This one is my favourite. I have put a pretend secret into my environment.

First, on the local backend. I ask it to print that secret. … It prints it. The command can see my secret.

Now I switch to the sandbox. The same command. … Nothing. The secret is not there.

Same tool. Same code. Only the place changed.

`[STOP]`

**Demo 5 — the landing page.**

`[DO: ask]` "Build a landing page for a coffee shop."

`[SAY]` And now, the request which failed in the last lecture. A landing page for a coffee shop.

…

Look. This time it **builds** it. Real files. A page you can open in the browser.

And we did not change the loop. Not one line.

`[TAKEAWAY]`

In the last lecture it could only describe. Today it can build, and it knows when to say no.

`[STOP]`

### Beat 10.5 — Your checklist · about 30 sec

`[OPEN]`

If you are building along with me, here is a small checklist. Pause the video and check each one.

> `[SCREEN or WRITE]`
> ☐ All the tests pass
> ☐ It can create a file and run it
> ☐ "Delete my home directory" comes back BLOCKED
> ☐ Reading a file outside the folder gives a permission error
> ☐ A secret is visible on local, and hidden in the sandbox
> ☐ In yolo mode, bash on local is refused

`[STOP]`

---
---

# PHASE 11 — Homework and closing

*Goal of this phase: the viewer knows what to practise, and what was learned.*

`[PHASE CHANGE — pause three seconds]`

### Beat 11.1 — Homework · about 2 min

`[OPEN]`

Before the next lecture, I want you to do four small things. They are not hard. And they will make you much stronger than someone who only watches.

`[EXPLAIN]`

**One.** Take a project of your own. Run your harness on it in **read-only** mode. Ask it to write a short guide: what this project does, and which three files a new person should read first. Then read what it wrote.

**Two.** Design a **seventh tool** for your own work. But write it as a contract first. The name. The description. The blanks. And two error messages. Only then write the code.

**Three.** Add one rule to the **never list**, for your own work. Not "delete". Something which would really hurt where you work. For example, a deploy command.

**Four.** Try to **break out of the jail**. Ask the harness to read a file outside the folder. See the error. And then see what the model does next.

`[OPTIONAL]`

And if you want more. Read how Pi and Hermes handle security in their code. And try our SSH backend on a small remote machine of your own.

`[END OPTIONAL]`

> `[WRITE or SCREEN]`
> **HOMEWORK**
> 1. Read-only mode on your own project → a short guide
> 2. Design a 7th tool — contract first
> 3. Add one rule to the never list
> 4. Try to break out of the jail

`[STOP]`

### Beat 11.2 — Closing · about 1.5 min

`[OPEN]`

So let me close, and say the whole lecture in five lines.

`[TAKEAWAY — slowly, one line at a time]`

One. A tool lets the model touch the outside world.

Two. The model sees only the **words** of a tool. Never the code. So we write those words carefully.

Three. Six tools are enough. And bash is the powerful one, and the dangerous one.

Four. Three protections keep it safe. The **gate** decides what may run. The **jail** decides where it can reach. The **backend** decides on which machine it runs.

Five. When the model is wrong, the damage must stay small.

In the last lecture, Zill got a heartbeat.

Today, it got hands, and a conscience.

In the next lecture, Zill meets its first real limit. The context fills up. And we learn how a small harness can still finish a big job.

Thank you so much. And I will see you in the next lecture.

`[STOP — end of video]`

---
---

# THE ONE-PAGE NOTES SHEET

*Show this on screen for ten seconds at the very end, and tell viewers: "Pause and take a screenshot. This is the whole lecture on one page."*

**TOOLS**
- Tool = the **wheels**; model = the **engine**. Brain in a jar → break the glass.
- Two kinds: **pre-built** (read · write · edit · bash · grep · ls · find) and **external** (MCP, scripts, plugins).
- Design question: how many to ship? Pi = few. Hermes = many. Zill = like Pi.

**THE CONTRACT**
- Interface (model sees): `name` · `label` · `description` · `parameters`
- Implementation (runs): `execute(toolCallId, params, signal, onUpdate)`
- The model decides from the **words alone**. Fix bad behaviour in the **contract**.
- Require only what the function cannot run without.

**SIX HANDS**
- inspect `read_file` · create `write_file` · correct `edit_file` · execute `bash` · navigate `list_files` · search `grep`
- One tool = one job. Minimal overlap. Fewer tools = smaller decision surface.

**TWO AXES**
- Help the next step. Protect the conversation (cap every output).
- Caps: read 4,000 lines · bash 12,000 chars (first 6k + last 6k) · list 500 · grep 200.

**EDIT**
- Snippet must appear **exactly once**. 0 → "not found". N → "include more context".
- Errors are written for the **model's retry**.

**WHERE A TOOL RUNS**
- `tools.py` = WHAT. `operations.py` = WHERE. Tools never touch the disk or processes directly.
- Backends: **local** · **sandbox** (scrubbed env, limits, optional docker: no network) · **ssh** (remote VM).
- Choose: `ZILL_BACKEND=…` for the project, `ZILL_TOOL_BACKENDS=bash=sandbox,read_file=local` per tool.
- Process sandbox stops **accidents**, not attackers. Docker or a remote machine is the real wall.

**SECURITY**
- Gate: **deny rules → mode → approver**. Order = the design.
- Modes: `read-only` · `safe` (fails closed) · `yolo` (bash on `local` is refused; needs sandbox / ssh).
- Jail: `resolve(path)` → `realpath` → inside root? else PermissionError.
- **Blast radius** = how far damage reaches. Gate → fewer attempts. Jail → cheaper miss.
- Three levels: tool-call gate · paths/files · user-level (enterprise gap). Around all: sandboxing.
- A failing or refused tool **never crashes the loop**.

---

# DRAWING GUIDE — exactly what to draw, step by step

**Ready-made copy sheets:** every drawing below also exists as a chalkboard-style picture in the folder `drawings-to-copy/` (files `draw-01-...png` to `draw-11-...png`). Open the picture next to your board and copy it step by step. The numbered yellow circles show the drawing order, and the bottom line is what to write last.

*Use this section while you rehearse. Each drawing gives you: when to draw it, how long it takes, a rough layout to copy, the steps in order, and what to say while your hand is moving. The ✍️ and 🎨 blocks inside the script point to these drawings.*

## How to draw (read this once)

1. **Only three shapes.** Boxes, circles, stick figures. Plus arrows. That is all you need.
2. **Only three colours.** **Black** for the thing itself, **red** for danger, blocking and the model's mistakes, **green** for safe, allowed and the harness. Use blue for the model if you want a fourth.
3. **Label first, explain second.** Draw the box, write one word in it, *then* talk. A silent two-second pause while you draw is fine and looks natural.
4. **Draw slowly while speaking.** The speaking and the drawing should end together. If a drawing takes longer than the sentence, say a second sentence.
5. **Don't try to be pretty.** A wobbly stick figure feels human and builds trust. Perfect clip-art feels like a slide.
6. **Fast tip:** if your drawing tool allows it, draw a very faint pencil outline before recording, then trace over it on camera. Nobody can tell.
7. **Never erase on camera.** If you make a mistake, say "let me redraw that" and draw it again to the side.
8. **Every drawing ends with one sentence written at the bottom.** Viewers screenshot those. They are given below.

**Quick overview**

| # | Drawing | Draw it in beat | Time | Main colours |
|---|---------|--------------------|------|--------------|
| 1 | The job posting and the curtain | 3.1 | 2 min | black, red |
| 2 | The cook with a few hands | 4.1 | 2 min | black, red |
| 3 | The intern and the senior | 5.1 | 2 min | black, green |
| 4 | The funnel | 6.1 | 3 min | black, red, green |
| 5 | The firecracker: bucket vs warehouse | 7.2 | 2 min | black, red |
| 6 | The three rings | 7.3 | 2 min | black, red, green |
| 7 | The operations switch (where a tool runs) | 8.1 | 2 min | black, green |
| 8 | The enterprise tree | 9.2 | 3 min | black, red |

If you are short on time, draw **1, 3, 4, 5 and 7**. They carry the five big ideas: the contract, the harness as a guard, the gate, blast radius, and where a tool runs.

---

## Drawing 1 — The job posting and the curtain *(Beat 3.1)*

**What it teaches:** the model sees only the *words* of a tool, never the code.
**Say before you start:** "Let me draw how the model sees a tool."

```
                       CORK BOARD
   o               ┌──────────────────────────────┐            ┃≈┃
  /|\    ────────▶ │ ┌───────┐ ┌───────────┐ ┌────┐│            ┃≈┃   ┌──────────────┐
  / \              │ │ TITLE │ │DESCRIPTION│ │FORM││            ┃≈┃   │ the actual   │
                   │ │Kitchen│ │Wash dishes│ │yrs?││            ┃≈┃   │ WORK         │
 the model         │ │porter │ │ in service│ │ __ ││            ┃≈┃   │ (your code)  │
 = the applicant   │ └───────┘ └───────────┘ └────┘│            ┃≈┃   └──────────────┘
                   └──────────────────────────────┘          the curtain
```

**Steps**
1. Draw a **big rectangle** in the middle. Write **CORK BOARD** above it.
2. Inside, draw **three small cards** side by side. Write **TITLE**, **DESCRIPTION**, **FORM** on them. Under them write a tiny example: *Kitchen porter · Wash dishes during service · years of experience?*
3. On the **left**, draw a **stick figure** looking at the board. Write **the model = the applicant** under him. Draw an **arrow** from him to the board.
4. On the **right**, draw a **tall wavy red line** (the curtain). Behind it, draw a **box** and write **the actual work (your code)**.
5. Write at the bottom: **"The applicant never sees the work. Only the posting."**

**Say while drawing:** "Look at this job posting. Title, description, and a form. The applicant reads this and decides whether to apply. He never sees the actual work behind the curtain. That is exactly how the model sees a tool: the name, the description, the parameters. The code is behind the curtain."

**Then connect it to the real thing:** point at the three cards and say: "Title is the name. Description is the description. Form is the parameters."

---

## Drawing 2 — The cook with a few hands *(Beat 4.1)*

**What it teaches:** few tools that combine well beat a drawer full of single-use gadgets.
**Say before you start:** "Imagine you are hiring a cook."

```
   THE DRAWER OF GADGETS               THE COOK
  ┌───────────────────────┐                o
  │ garlic press           │               /|\───── eyes        → read_file
  │ avocado slicer         │               / \  ──── fresh card → write_file
  │ egg separator          │                    ──── pencil+eraser → edit_file
  │ strawberry huller      │                    ──── STOVE (red!) → bash
  │ ... 40 of them ...     │                    ──── pantry list → list_files
  └───────────────────────┘                    ──── index       → grep
        "40 gadgets"                      "6 hands"
```

**Steps**
1. On the **left**, draw a **drawer** (a box with a handle). Scribble a few little gadgets inside. Write **40 gadgets** above it.
2. On the **right**, draw a **stick-figure cook**. From him draw **six short lines** going out, like arms.
3. At the end of each line write one thing and its tool: **eyes → read_file**, **fresh card → write_file**, **pencil + eraser → edit_file**, **stove → bash**, **pantry list → list_files**, **index → grep**.
4. **Circle the stove in red.** Draw little flames.
5. Write at the bottom: **"Nearly every gadget is the stove wearing a costume."**

**Say while drawing:** "I could hand the cook forty gadgets. Or I could give him a few things that do everything. Eyes to read the recipe. A fresh card to write a new one. A pencil and eraser to fix a line. A stove, which cooks anything. A pantry list. An index. And almost every gadget you can think of is just the stove wearing a costume."

---

## Drawing 3 — The intern and the senior *(Beat 5.1)*

**What it teaches:** the model will not police itself. The harness stands behind it.
**Say before you start:** "Let me show you what a harness really is, in one picture."

```
        ╭──────────────────╮
        │ "Wait. Are you   │
        │   sure?"         │
        ╰──────┬───────────╯
               │
     (o)       │            o   ≈≈≈
    /|\ ───────┘           /|\──────  [keyboard]
    / \   hand on         / \   typing 100x faster
  the SENIOR  shoulder   the INTERN
  = the harness          = the agent
```

**Steps**
1. On the **right**, draw a **small stick figure** in front of a **wide keyboard**. Add **little motion lines** around his hands. Write **the agent (the intern)** under him.
2. On the **left**, draw a **taller stick figure** standing **just behind** the intern. Draw her **arm reaching out, with the hand on his shoulder**. Write **the harness (the senior)**.
3. Draw a **speech bubble** from the senior: **"Wait. Are you sure?"**
4. Write at the bottom: **"We are not building the intern. We are building the person standing behind him."**

**Say while drawing:** "Imagine a brand-new intern who types a hundred times faster than you, never gets tired, and will run anything he thinks might help. Including the command that wipes your project. We are not building that intern. The model is the intern. We are building the person standing behind him, with a hand on his shoulder."

---

## Drawing 4 — The funnel *(Beat 6.1)*

**What it teaches:** the three layers of the gate, and why the order matters.
**Say before you start:** "Every tool call goes through one checkpoint."

```
        tool call   tool call   tool call
            ↓           ↓           ↓
   ╲──────────────────────────────────╱
    ╲  1 · DENY RULES  (never, any mode) ╱ ─────▶ [ BLOCKED ]
     ╲────────────────────────────────╱
      ╲  2 · MODE  read-only/safe/yolo ╱ ─────▶ [ BLOCKED ]
       ╲──────────────────────────────╱
        ╲ 3 · ASK A HUMAN            ╱ ─────▶ [ BLOCKED ]
         ╲──────────────────────────╱
                    ↓
              [  RUN ✓  ]       (green)
```

**Steps**
1. Draw a **big funnel**: a wide top, narrowing to a small bottom. Above it draw **three small arrows** pointing in, labelled **tool calls**.
2. Cut the funnel into **three horizontal bands** with two lines.
3. Write **1 · DENY** in the top band, **2 · MODE** in the middle, **3 · ASK HUMAN** in the bottom.
4. From each band draw an **arrow to the right** ending in a **red box** that says **BLOCKED**.
5. Below the funnel draw a **small green box**: **RUN ✓**.
6. Write on the side: **"Most calls: waved through. Some: ask. A few: never."**

**Say while drawing:** "Look at the order. Deny rules first. No mode setting and no tired human at two in the morning can override them. Then the mode, which settles whole categories without a question. And the human last, who only sees what the first two layers could not decide."

**Ask the viewer:** "Why is deny first? Pause and think." *(Answer: so that nothing above it can approve a catastrophe.)*

---

## Drawing 5 — The firecracker: bucket vs warehouse *(Beat 7.2)*

**What it teaches:** *blast radius*. The same mistake can be small or huge, depending on what sits within reach.
**Say before you start:** "Let me explain blast radius with a firecracker."

```
   PANEL 1: A STEEL BUCKET                 PANEL 2: A FIREWORKS WAREHOUSE
       *  * *                                     * * * * * *
        \ | /                                   ┌───────────────────┐
   ┌─────(*)────┐                              │ ## ## ## ## ## ## │   ← the whole
   │  steel     │                              │ ## ## (*) ## ## ## │     building goes
   │  bucket    │                              │ ## ## ## ## ## ## │
   └────────────┘                              └───────────────────┘
   blast radius:                               blast radius:
   a few inches                                the building
```

**Steps**
1. Draw **two panels** side by side, with a line between them.
2. **Left:** draw a **bucket**. Inside it, a **tiny firecracker** with a few **sparks**. Write **blast radius: a few inches**.
3. **Right:** draw a **big box** (the warehouse) full of **little firework shapes**. Put the **same tiny firecracker** in the middle, with **big spiky explosion lines** across the whole box. Write **blast radius: the building**.
4. Between them write: **"Same mistake. Wildly different blast radius."**
5. At the bottom write: **"The danger is not only the action. It is what sits within reach."**

**Say while drawing:** "A firecracker in a steel bucket does a few inches of damage. The same firecracker in a fireworks warehouse takes the whole building. The mistake is identical. We cannot make the model stop making mistakes. What we can do is shrink the room it goes off in."

---

## Drawing 6 — The three rings *(Beat 7.3)*

**What it teaches:** security is layers: *where*, *what*, *who*.
**Say before you start:** "Let me put all the security ideas into one picture."

```
        ╭──────────────────────────────╮
       ╱   JAIL  — bounds WHERE         ╲
      │   ╭──────────────────────────╮   │
      │  ╱  DENY RULES — bound WHAT    ╲  │
      │ │   ╭────────────────────────╮  │ │
      │ │  ╱ MODES + APPROVER —       ╲ │ │
      │ │ │   bound WHO decides        │ │ │
      │ │ │          o                 │ │ │
      │ │ │         /|\  the agent     │ │ │
      │ │  ╲                          ╱  │ │
      │  ╲  ╰────────────────────────╯ ╱  │
       ╲   ╰──────────────────────────╯  ╱
        ╰──────────────────────────────╯
```

**Steps**
1. Draw **three circles, one inside the other** (like a target).
2. Draw a **tiny stick figure** in the very centre. Write **the agent**.
3. Label the **outermost ring: JAIL — bounds WHERE** (which folder it can reach). Draw it in **green**.
4. Label the **middle ring: DENY RULES — bound WHAT** (which commands can run). Draw it in **red**.
5. Label the **inner ring: MODES + APPROVER — bound WHO decides.**
6. Write at the bottom: **"Gate = fewer attempts. Jail = a cheaper miss."**
7. Draw a **small dotted circle outside** the whole thing, and write: **"network tools need a ring of their own."**

**Say while drawing:** "Three rings. The inner one decides who approves. The middle one decides what commands may run. And the outer one decides where in the file system anything can reach. If one ring fails, the next one catches it."

---

## Drawing 7 — The operations switch *(Beat 8.1)*

**What it teaches:** *what* a tool does is separate from *where* it runs.
**Say before you start:** "Pi has a very clever idea, and we are going to copy it."

```
              ┌──────────────┐
              │  TOOL: bash  │        ← WHAT it does
              └──────┬───────┘
                     │
              ┌──────▼───────┐
              │  OPERATIONS  │        ← WHERE it runs  (a switch)
              └──┬────┬────┬─┘
                 │    │    │
          ┌──────▼┐ ┌─▼────┐ ┌▼───────┐
          │ LOCAL │ │ SSH  │ │SANDBOX │
          │ my PC │ │remote│ │ a jail │
          └───────┘ └──────┘ └────────┘
```

**Steps**
1. Draw a **box at the top**: **TOOL: bash**. Write **WHAT it does** next to it.
2. Draw an **arrow down** to a **second box**: **OPERATIONS**. Next to it write **WHERE it runs**. Draw a **small switch** (a lever) on this box.
3. From it, draw **three arrows** to **three boxes**: **LOCAL (my PC)**, **SSH (remote machine)**, **SANDBOX (a jail inside my OS)**.
4. Colour the **sandbox box green**. Write under it: **"safe place for dangerous commands."**
5. At the bottom write: **"bash → sandbox · read → local   (per tool!)"**

**Say while drawing:** "The tool never knows where it is running. That one small layer decides. So I can run bash in the sandbox, and keep read on my own machine, without changing a single line of the tool."

---

## Drawing 8 — The enterprise tree *(Beat 9.2)*

**What it teaches:** big companies need a third kind of security: *who* is allowed to use *which tools*.
**Say before you start:** "Let me show you a problem that open-source harnesses do not solve yet."

```
                      ┌─────────────┐
                      │   COMPANY   │
                      └──────┬──────┘
          ┌──────────────────┼──────────────────┐
     ┌────▼────┐        ┌────▼────┐        ┌────▼────┐
     │Country A│        │Country B│        │Country C│
     └────┬────┘        └────┬────┘        └────┬────┘
      ◇    │ ◇            ◇  │               ◇   │
   ┌───▼──┐ ┌──▼───┐    ┌──▼───┐           ┌───▼──┐
   │Entity│ │Entity│    │Entity│           │Entity│
   └───┬──┘ └──────┘    └──┬───┘           └───┬──┘
       │                   │                   │
    ┌──▼───┐            ┌──▼───┐            ┌──▼───┐
    │Org   │            │Org   │            │Org   │
    │unit  │            │unit  │            │unit  │
    └──┬───┘            └──┬───┘            └──┬───┘
       o  o                o                   o  o      ← users
   ◇ = a gate: "which tools may this level use?"
```

**Steps**
1. Draw a **box at the top**: **COMPANY**.
2. Below it draw **three boxes**: **Country A, Country B, Country C**, with lines down from the company.
3. Under each country draw one or two **ENTITY** boxes, and under those an **ORG UNIT** box.
4. At the bottom draw **small stick figures** (the users).
5. On **every level**, draw a small **diamond** (the gate). Write beside one of them: **"which tools may this level use?"**
6. Colour the diamonds **red**. Write at the side: **"The same gate that checks a tool call, and a path, must also check a USER."**

**Say while drawing:** "A big company has countries, entities inside each country, organisational units inside those. Access is controlled at every level. You cannot give everybody the whole harness. Each level needs its own gate. Today's open-source harnesses do not do this yet, and that is a real opportunity."

---

## Optional extra drawings (only if you have time)

- **The 500-line file, by hand** (Beat 4.3): draw a long bar labelled *500 lines*. Colour the *whole* bar yellow for **overwrite** ("model re-types everything"). Draw the *same* bar in grey with a **tiny yellow block** in the middle for **edit**. Write under them: *497 chances for a typo* vs *about 6 lines*.
- **The tape with a BLOCKED line** (Beat 6.3): draw six horizontal lines labelled *user, assistant, tool, assistant, tool, assistant*. Colour the third one **red** and write **BLOCKED** on it. Draw an arrow from the fourth line back to the third and write **"the model reads the reason"**.
- **The four steps of depth** (Beat 9.3): draw a **staircase** with four steps going up. Label them from the bottom: *what a tool is · the contract · gate the call · where it runs*. Draw a stick figure on step 1 and another on step 4 and write **"most people stop here"** and **"harness engineers go here."**

---

## Notes for you (not spoken)

**Pictures to put on screen** (folder `diagrams-lecture3/`)

| File | Beat | What it shows |
|------|------|---------------|
| diagram-01.png | 1.2 | the two empty sockets |
| diagram-02.png | 2.1 | brain in a jar |
| diagram-03.png | 2.2 | two kinds of tools |
| diagram-04.png | 3.2 | a tool has two halves |
| diagram-05.png | 3.3 | the read_file contract |
| diagram-06.png | 3.4 | loose vs tight |
| diagram-07.png | 4.1 | six tools |
| diagram-08.png | 4.2 | two rules and the limits |
| diagram-09.png | 4.3 | edit vs overwrite |
| diagram-10.png | 4.4 | bash |
| diagram-11.png | 6.1 | the gate, three layers |
| diagram-12.png | 6.2 | the three modes |
| diagram-13.png | 6.3 | the never list, and a blocked call |
| diagram-14.png | 7.1 | the jail |
| diagram-15.png | 8.1 | where a tool runs (Pi) |
| diagram-20.png | 8.2 | Zill's operations layer |
| diagram-17.png | 9.1 | the journey of one tool call |
| diagram-16.png | 9.2 | three levels of security (optional beat) |
| diagram-18.png | 9.3 | four levels of understanding |
| diagram-19.png | 10.1 | what we build today |

**Drawings to copy on the board** (folder `drawings-to-copy/`)

| File | Beat | Must draw? |
|------|------|-----------|
| draw-01-job-posting-and-curtain.png | 3.1 | yes |
| draw-02-cook-with-few-hands.png | 4.1 | optional |
| draw-09-extra-500-line-file.png | 4.3 | optional (or just write the numbers) |
| draw-03-intern-and-senior.png | 5.1 | yes |
| draw-04-funnel.png | 6.1 | yes |
| draw-05-firecracker-bucket-vs-warehouse.png | 7.2 | yes |
| draw-06-three-rings.png | 7.3 | optional |
| draw-07-operations-switch.png | 8.1 | yes |
| draw-08-enterprise-tree.png | 9.2 | optional |

Five drawings are marked "yes". That is one drawing for each big idea: the contract, the harness as a guard, the gate, blast radius, and where a tool runs.

**If the video is too long, cut in this order**
1. Beat 9.2 (the enterprise level).
2. The optional drawings in 4.1 and 7.3.
3. The optional puzzle in 4.3 and the chunk note in 4.2.
4. Or split into two videos at the natural break after Phase 4.

**Check these before recording**
- The details about Pi come from your own study of it: the four fields of a tool, the extra things its function receives, the seven built-in tools, the chunked reading, and the three places a tool can run. Open Pi's code and confirm each one before you say it on camera.
- "A GitHub MCP server gives a whole set of tools" is said without a number on purpose. If you want to say a number, check it first.
- Run the build prompt once before recording, and keep that recording as a backup. Check that the tests pass, and read what the sandbox says it enforces on your own computer. On Windows the sandbox hides secrets but has no CPU or file-size limits, so do not claim those.
- The SSH backend is tested only with a pretend server. The script says so. Keep that sentence unless you have tried it on a real machine.
- The line counts on diagram-19 are estimates. Replace them with your real numbers after the build.
- The enterprise beat (9.2) is written as your own experience. Say only what you have really seen.
- This lesson follows the structure of the Odysseus tutorial's Tools lesson. Credit it in the description.
- The older version of this script is saved as `zill-lecture3-script-old.md`.


---

## Extra board drawings

![draw-10-extra-blocked-on-the-tape](../assets/lecture-3/drawings-to-copy/draw-10-extra-blocked-on-the-tape.png)

![draw-11-extra-four-steps-of-depth](../assets/lecture-3/drawings-to-copy/draw-11-extra-four-steps-of-depth.png)