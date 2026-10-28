# Harness Engineering Series — Lecture 4: Context and Compaction

**Speaking script — phase-by-phase version.**
Lecture 2 built the loop. Lecture 3 gave Zill hands and a conscience. This lecture teaches Zill to survive a long task: what goes into its context, and how a real harness keeps that context under budget.

---

## How this script is organised (read this once, not spoken)

The lecture is cut into **16 phases** (0 to 15). Each phase is cut into small **beats**. A beat is one idea, about one to three minutes.

**Every beat has the same four steps, always in this order:**

| Tag | What you do |
|-----|-------------|
| `[OPEN]` | One or two sentences that tell the viewer what is coming. |
| `[EXPLAIN]` | The explanation. Short paragraphs. **One paragraph = one breath.** |
| `[TAKEAWAY]` | One line that sums up the beat. Say it **slowly**, looking at the camera. |
| `[STOP]` | Stop talking. Breathe for two seconds. Then start the next beat. |

**Other tags (none of these are spoken):**

- `[SCREEN → diagram-07]` — put this picture on screen (folder `diagrams-lecture4/`). Keep it up until the next `[SCREEN]`.
- `[ASK]` — ask the viewers a question, tell them to pause the video, then answer it yourself.
- `[OPTIONAL]` … `[END OPTIONAL]` — you can skip this part if the video is getting long.
- `[PHASE CHANGE]` — a big change of topic. Pause for three seconds. Then say the line that follows it.
- `[DO]` / `[SAY]` — only in the build phase: `[DO]` is what you type or click, `[SAY]` is what you say while it runs.

**There is nothing to draw in this lecture.** Every idea has a ready picture. 64 pictures in total, in the order you show them.

**Rules for speaking it**

1. Anything inside `[square brackets]` is for you. Do not read it aloud.
2. Each blank line is a small pause.
3. Words in **bold** are the words to stress.
4. If you lose your place, go to the next `[OPEN]` and continue from there. Nothing will be lost.

---

## Map of the lecture (not spoken)

| Phase | What it is about | Time | Pictures |
|-------|------------------|------|----------|
| 0 | Opening and the plan | 3 min | 01, 02 |
| 1 | Revision: the fuel and the tape | 3 min | 03, 04 |
| **PART 1** | **What goes into the context?** | | |
| 2 | The nine things in every call | 5 min | 05, 06 |
| 3 | How Pi builds its prompt | 4 min | 07, 08 |
| 4 | Project context: the AGENTS.md walk-up | 4 min | 09, 10 |
| 5 | Skills and progressive disclosure | 6 min | 11, 12, 13, 14 |
| 6 | How to write a good skill | 12 min | 15 – 24 |
| 7 | The last piece, and the Part 1 recap | 2 min | 25 |
| | *— natural break: you can end video 1 here —* | | |
| **PART 2** | **Compaction: Pi vs Hermes** | | |
| 8 | Why "just summarize it" is not enough | 4 min | 26, 27 |
| 9 | How Pi compacts | 10 min | 28 – 37 |
| 10 | How Hermes compacts | 10 min | 38 – 46 |
| 11 | Pi vs Hermes, side by side | 4 min | 47 – 50 |
| **PART 3** | **DeepSeek Harness, and the cache** | | |
| 12 | How DeepSeek Harness compacts | 7 min | 51 – 57 |
| 13 | Prompt caching | 4 min | 58, 59 |
| **PART 4** | **Build it** | | |
| 14 | Zill's compaction, and the build | 10 min | 60 – 63 |
| 15 | Closing and homework | 3 min | 64 |

Total: about 90 minutes with the build. If that is too long, record Phases 0–7 as one video ("Context and skills") and Phases 8–15 as the next ("Compaction").

---
---

# PHASE 0 — Opening

*Goal of this phase: the viewer knows what today is about, and why it matters.*

### Beat 0.1 — Where we are · about 1.5 min

`[SCREEN → diagram-01]`

`[OPEN]`

Hello everyone, and welcome back to the Harness Engineering series. This is lecture number four.

`[EXPLAIN]`

Before we start, just look at your Zill repository. It should look like this picture.

From lecture two, you have **provider.py**, the model client, and **loop.py**, the heartbeat.

From lecture three, you have **tools.py**, the hands. **security.py**, the conscience. And **operations.py**, which decides where a tool runs.

If you have all five, you are on the right track. If not, please go back and finish lecture three first, because today we build on top of it.

Today we add one new file. **context.py**.

And I will tell you honestly: I think today is the most important lecture of this whole series.

`[TAKEAWAY]`

Five files are done. Today, one more: **context.py**.

`[STOP]`

### Beat 0.2 — Two different jobs · about 1.5 min

`[SCREEN → diagram-02]`

`[OPEN]`

So why do I say today is so important? Because of two words that people mix up all the time.

`[EXPLAIN]`

The first one is **context engineering**. Context engineering is the art of filling the context well. What goes in. The system prompt, the tools, the skills, the memory files, the conversation. These are the ingredients.

Most courses teach this part, and then they stop.

But a harness has a second job. It is called **context management**. That means: turn after turn, how does the harness keep this context under budget? When does it compact? What does it keep? Where does it cut? And what if the compaction itself fails?

That is not the ingredients. That is **running the kitchen**.

And today we will see how two of the best open-source harnesses in the world, **Pi** and **Hermes**, run that kitchen. Then we will look at a third one, **DeepSeek Harness**. And believe me, it is much more detailed than you think.

Then, at the end, we build our own simple version for Zill.

`[TAKEAWAY]`

Context engineering fills the window. **Context management** keeps it alive.

`[STOP]`

### Beat 0.3 — The plan for today · about 30 sec

`[OPEN]`

Let me tell you how this lecture will go, so you can follow along easily.

`[EXPLAIN]`

There are four parts.

Part one. **What goes into the context?** Including skills, and how to write a good one.

Part two. **Compaction.** How Pi does it, and how Hermes does it.

Part three. **DeepSeek Harness**, and a small thing called the cache.

Part four. We **build** compaction into Zill, and we watch it happen.

Every time we move from one part to the next, I will tell you.

`[TAKEAWAY]`

Four parts: what goes in, how Pi and Hermes compact, DeepSeek, and the build.

`[STOP]`

---
---

# PHASE 1 — Revision: the fuel and the tape

*Goal of this phase: the viewer remembers why context is a budget, and sees the tape growing.*

### Beat 1.1 — Context is the fuel · about 1 min

`[SCREEN → diagram-03]`

`[OPEN]`

Let us go back to the picture from lecture one.

`[EXPLAIN]`

We said a harness is like a car. The **LLM** is the engine. The **tools** are the wheels.

And the **context** is the fuel.

Now, what is the thing about fuel? The tank has a size. When it runs out, you have to refill it. And you cannot just keep pouring forever.

Context is exactly like that. It is a very precious resource. It has a **budget**.

`[TAKEAWAY]`

Context is not a bottomless tank. It is a **budget**.

`[STOP]`

### Beat 1.2 — The tape only grows · about 2 min

`[SCREEN → diagram-04]`

`[OPEN]`

Now let us see how fast that fuel gets used.

`[EXPLAIN]`

Remember our loop from lecture two. We call the model. If it wants a tool, we run the tool. And then we **append** the result to the messages array. And we go round again.

`[ASK]` The loop takes two main arguments. Can you tell me what they are? Pause the video and think.

The answer: the **messages**, and **max turns**. And of course, it also gets the tools.

Now look at that messages array. We call it the **tape**. Every turn, something is added to it. Nothing is ever taken out. And on every single call, the **whole tape** is sent to the model again.

So look at the chart on the right. Turn one, maybe 3,000 tokens. Turn five, 9,000. Turn ten, 24,000. Turn twenty, 51,000. And by turn thirty of a real task, the tape hits the ceiling.

Nobody wrote a bug here. The loop is doing exactly what we told it to do. Append everything, forever.

`[TAKEAWAY]`

The tape only grows. And on a long task, it **will** hit the ceiling.

`[STOP]`

`[PHASE CHANGE]`

Okay. So now we know the problem. Before we fix it, we need to know exactly **what** is inside the context. That is part one of four.

---
---

# PART 1 — What goes into the context?

---

# PHASE 2 — The nine things in every call

*Goal of this phase: the viewer can list everything the model sees, and knows which part is compacted.*

### Beat 2.1 — Nine things ride into every call · about 3 min

`[SCREEN → diagram-05]`

`[OPEN]`

Every time Zill calls the model, a lot of things go along with that call. Let us list them, one by one.

`[ASK]` Before I show you, try it yourself. What do you think goes into the context on every call? Pause the video and make your list.

`[EXPLAIN]`

Okay, let us see.

Number one. The **system prompt**. How the agent must behave.

Number two. The **tools**. And not just their names. The full contract we learned in lecture three. The name, the label, the description, and the parameters.

Number three. The **skills**. But here is something interesting. For a skill, only its **name and a short description** go in. Not the whole skill. Even if the skill file is a thousand lines long, only one or two lines go in. We will see why in a few minutes.

Then numbers four, five and six. These are the messages array itself. The **user** messages. The **assistant** messages, meaning what the model said and thought. And the **tool calls with their results**.

Number seven. **Memory files.** Files like AGENTS.md or CLAUDE.md, which you write by hand and which stay with your project across sessions.

Number eight is optional. Some harnesses, like **Hermes** and **OpenClaw**, decide on their own what was important in a conversation, and save small memory fragments to disk. Pi does not do this.

And number nine. A small one that people forget. The **current working directory**, and **today's date**.

So, nine things.

Now look at the right side of the picture. Out of these nine, which ones get compacted?

Only four, five and six. The **messages array**. The system prompt is never compacted. The tools are never compacted. The skills, the memory files, the date: never compacted.

`[TAKEAWAY]`

Nine things go into every call. But only **the conversation** is ever compacted.

`[STOP]`

### Beat 2.2 — System prompt, user, assistant · about 2 min

`[SCREEN → diagram-06]`

`[OPEN]`

People often ask me: what is the difference between the system prompt and a user message? Let me make that clear.

`[EXPLAIN]`

The **system prompt** tells the agent **how to behave**. For example, Pi's system prompt starts like this: "You are an expert coding assistant operating inside pi, a coding agent harness." Then it lists the tools available.

It is the same for **every session**. Anyone who starts Pi gets this same text. It is written by the harness.

The **user message** is **what you want right now**. For example: "Migrate this code base to Rust." That changes in every session. It is written by you.

And the **assistant message** is what the model says. Its thinking, its reply, and the tool calls it makes. It grows every turn.

`[TAKEAWAY]`

The system prompt is the **high-level guideline**. The user message is **today's job**.

`[STOP]`

---
---

# PHASE 3 — How Pi builds its prompt

*Goal of this phase: the viewer sees that a real harness assembles the prompt from parts, fresh every time.*

### Beat 3.1 — Five pieces, stacked in order · about 2.5 min

`[SCREEN → diagram-07]`

`[OPEN]`

Now, that list of nine things is fine for a context engineering class. But we are doing harness engineering. So let us see what a real harness, Pi, actually does.

`[EXPLAIN]`

The words can be a little confusing here. When Pi says "system prompt", it does not mean one fixed paragraph. It means **everything it assembles** and sends to the model before the conversation. And it builds this with a function called **buildSystemPrompt**.

It stacks five pieces, in order. Start from the bottom of the picture.

Piece one. The **base template**. "You are an expert coding assistant operating inside pi", plus the list of available tools. So Pi merges the tools into this first piece.

Piece two. **appendSystemPrompt**. Any extra text you want to glue on.

Piece three. **Project context**. Every AGENTS.md or CLAUDE.md file it finds. This is the memory part from our list of nine.

Piece four. **Available skills**. Only the name, the description, and where the file lives. And notice the small note on the left: this piece is added only if the read tool exists. Why? Because if the model cannot read files, it cannot open a skill anyway.

Piece five, stamped **last**. The current date and the current working directory.

And look at the red bracket on the right. All five pieces become **one string**, and that string is **rebuilt on every call**.

`[TAKEAWAY]`

The prompt is not written once. It is **assembled**, fresh, every time.

`[STOP]`

### Beat 3.2 — Same template, three prompts · about 1.5 min

`[SCREEN → diagram-08]`

`[OPEN]`

Why does that matter? Let me show you with three examples.

`[EXPLAIN]`

Example A. Monday, in a repo called app. The date says the fourteenth. One AGENTS.md is found. Three skills.

Example B. Tuesday, same repo. What changed? Only the **date**. Everything else is the same. That is date injection.

Example C. Same day, but this time the read tool is switched off. Now the skills block is **gone**, because the model has no way to open a skill.

So the template stays constant. But the assembled prompt moves with the date, with the files, and with the skills.

`[TAKEAWAY]`

The template is constant. **The assembly is not.**

`[STOP]`

---
---

# PHASE 4 — Project context: the AGENTS.md walk-up

*Goal of this phase: the viewer understands how Pi finds memory files, and why it does it every time.*

### Beat 4.1 — The walk-up · about 2.5 min

`[SCREEN → diagram-09]`

`[OPEN]`

Let us zoom into piece three, the project context. How does Pi find those memory files?

`[EXPLAIN]`

Think about how people actually work. You might have one AGENTS.md at the top level, with how you like to do all your projects. And inside one particular project, a CLAUDE.md with the rules for that project.

Pi collects them like this.

First, it loads the **global** file, from its own folder in your home directory. That is your personal, cross-project instructions. That goes in first.

Then it **walks up**. It starts at the folder you are working in, the cwd. Here that is the src folder. Nothing there. Then it goes to the parent: the repo. It finds CLAUDE.md, and grabs it. Then the parent of that: work. Nothing. Then the parent: your user folder. It finds AGENTS.md, and grabs it. And it keeps going, all the way up to the root of the file system.

In every folder it checks four names, in this order: AGENTS.md, AGENTS.MD with capitals, CLAUDE.md, and CLAUDE.MD.

Now look at the final order on the right. The global file first. Then the furthest folder. And the **closest** file **last**.

Why last? Because the file nearest to your work should have the **last word**. If two files say different things, the closest one wins.

And one more small detail. Pi **dedups by path**. The same file is never loaded twice.

`[TAKEAWAY]`

Global first, then furthest to closest. **The file nearest your work speaks last.**

`[STOP]`

### Beat 4.2 — Why walk again every time? · about 1.5 min

`[SCREEN → diagram-10]`

`[OPEN]`

Here is a question. Why does Pi do this walk again and again? Why not just once at the start?

`[EXPLAIN]`

Look at this timeline. On turn four, the agent is using npm. Then **you** open CLAUDE.md, in the middle of the session, and add one line: "use pnpm, never npm".

On turn five, the prompt is rebuilt. The walk runs again. It finds your edit. And now the agent uses pnpm.

That is why the walk runs on every rebuild. So that a change you make in the middle of a session is picked up on the very next turn.

Two quick questions people ask me.

Is there a limit on how many files it takes? No. It takes every one it finds. So keep only a **few** memory files per project, otherwise you will confuse the model.

And what if two files disagree? The one closest to your repo is read last, and it wins.

And one honest point about Pi. These files are Pi's **only** memory. Pi has nothing else. It relies on **you** to keep these files up to date.

`[TAKEAWAY]`

The walk runs **every time**, so an edit made mid-session is seen on the next turn.

`[STOP]`

---
---

# PHASE 5 — Skills and progressive disclosure

*Goal of this phase: the viewer knows what a skill is, why only its top is loaded, and how it differs from a tool.*

### Beat 5.1 — A skill file is a trailer · about 2 min

`[SCREEN → diagram-11]`

`[OPEN]`

Now, piece four: skills. Many people are confused about skills. So let me make this very simple.

`[EXPLAIN]`

A skill is one markdown file, called **SKILL.md**.

At the top, it has a small labelled section. This is called the **frontmatter**. It has two things: a **name**, and a **description**. Here the name is "processing-pdfs", and the description says it extracts text and tables from PDF files.

Below that is the **body**. The real instructions. That can be long. Hundreds of lines.

Now here is the key idea. Only the top part, the name and the description, sits in the context. Every turn. For every skill.

The body is loaded **only when the model picks that skill**.

Think of it like a movie trailer. The trailer is short, and it tells you what the movie is about. You only watch the full movie if the trailer makes you want to.

This idea has a name. It is called **progressive disclosure**. You disclose the skill little by little, only when it is needed.

`[TAKEAWAY]`

Only the trailer is always loaded. The full movie loads **only when it is picked**.

`[STOP]`

### Beat 5.2 — Three levels of loading · about 1.5 min

`[SCREEN → diagram-12]`

`[OPEN]`

Actually, there are not two levels. There are three.

`[EXPLAIN]`

Level one. The **name and description**. Loaded at startup, for every skill.

Level two. The **body** of SKILL.md. Read only when the skill is triggered.

Level three. Extra files that live next to the skill. A reference file, an examples file, a scripts folder. These are read only if that **specific** thing is needed.

So you can bundle as many files as you like with a skill. A bundled file costs nothing until it is actually opened.

`[TAKEAWAY]`

The model pays for a skill in **three instalments**, and usually stops at the first.

`[STOP]`

### Beat 5.3 — Tool or skill? · about 1 min

`[SCREEN → diagram-13]`

`[OPEN]`

Let me check if this is clear. What is the difference between a **tool** and a **skill**?

`[EXPLAIN]`

A **tool** is **how** to do one action. Read a file. Run a command. Search with grep. Its full contract is in the context every turn. Tools are the hands.

A **skill** is **what** to do, and **when** to do it. It is more like a recipe, a procedure. And only its name and description are in the context until it is picked.

A recipe can call for many hands. But a hand never tells you the recipe.

`[TAKEAWAY]`

A tool is **how**. A skill is **what, and when**.

`[STOP]`

### Beat 5.4 — A real skill: my writing style · about 1.5 min

`[SCREEN → diagram-14]`

`[OPEN]`

Let me give you a real example of a skill I made myself.

`[EXPLAIN]`

I was building a product with a writing agent. And the problem was, whatever it wrote looked AI-generated. You know the classic signs. Double dashes everywhere. Words like "delve", or "honestly".

So I gave my agent a few chapters of my own book, and I asked it to create a skill. It came back with a file called **writing-style.md**. A name, a description, and a long list of rules.

And now, every time that agent writes, the skill loads. I never have to explain my style again. A new book, a blog post, a landing page: the skill carries the style every time.

And this is my personal philosophy. The core of a harness should stay **small**. The power comes from the skill files you write. Hermes takes the other approach. It ships with a big core and many skills already built in. Both are valid. But for your own product, the best skills come from **your own** experience.

`[TAKEAWAY]`

Write your rules **once**, as a skill. Reuse them everywhere.

`[STOP]`

---
---

# PHASE 6 — How to write a good skill

*Goal of this phase: the viewer can write a skill that gets found, stays small, and is tested.*

*(These rules come from Anthropic's own guide on authoring skills, made visual.)*

### Beat 6.1 — Say less · about 1 min

`[SCREEN → diagram-15]`

`[OPEN]`

So how do you write a good skill? Rule number one is a surprising one. **Say less.**

`[EXPLAIN]`

The model already knows a lot. It knows what a PDF is. It knows what React is. It knows why Rust is fast.

So do not explain those things in your skill. Look at the picture. A good instruction is about 50 tokens. The verbose one says the same thing in 150 tokens, because it also explains what a PDF is and why libraries exist.

Cut that. For every paragraph you write, ask: does this earn its token cost?

`[TAKEAWAY]`

Only add what the model **does not already know**.

`[STOP]`

### Beat 6.2 — The two required fields · about 1 min

`[SCREEN → diagram-16]`

`[OPEN]`

Next, the top of the skill. There are exactly two required fields.

`[EXPLAIN]`

The **name**. At most 64 characters. Only lowercase letters, numbers and hyphens. And it cannot contain the words "claude" or "anthropic".

The **description**. At most 1,024 characters. It must not be empty. And it must say what the skill does, **and** when to use it.

No XML tags in either one. And both are checked.

`[TAKEAWAY]`

Two fields, and **both are validated**.

`[STOP]`

### Beat 6.3 — The description is how a skill gets found · about 1.5 min

`[SCREEN → diagram-17]`

`[OPEN]`

Now, the description is the most important line you will write. Let me tell you why.

`[EXPLAIN]`

Remember, the model only sees the name and the description. That is all it has to decide whether to use your skill. So if the description is bad, your skill will **never be found**.

Look at the good one. "Extract text and tables from PDF files, fill forms, merge documents." That is **what** it does. Then: "Use when working with PDF files or when the user mentions PDFs." That is **when** to use it.

Now the bad ones. "I can help you process Excel files." Always write in the third person. Never "I" or "you".

And "Helps with documents". Far too vague. If you have a hundred skills, how will the model pick this one?

`[TAKEAWAY]`

Write **what** it does and **when** to use it. The model picks on this one sentence alone.

`[STOP]`

### Beat 6.4 — Name skills after the activity · about 1 min

`[SCREEN → diagram-18]`

`[OPEN]`

The same goes for the name.

`[EXPLAIN]`

Name the skill after the **activity**. Processing PDFs. Analyzing spreadsheets. Managing databases. Writing documentation.

And avoid names like helper, utils, documents, or tools. They say nothing about what the skill does.

`[TAKEAWAY]`

A name should say what the skill **does**, not that it helps.

`[STOP]`

### Beat 6.5 — How much freedom to give · about 1.5 min

`[SCREEN → diagram-19]`

`[OPEN]`

Now, the body of the skill. How detailed should it be? This one is a little non-intuitive.

`[EXPLAIN]`

Anthropic uses a nice picture for this.

Some tasks are a **narrow bridge**, with a cliff on both sides. Only one path is safe. A database migration is like this. Or something very specific to your company. For these, give **low freedom**. Give the exact script, and say "do not change it".

Other tasks are an **open field**. Many paths reach the goal. A code review is like this. For these, give **high freedom**. Give the goal, and let the model choose. If you over-specify an open field, the skill actually gets **worse**.

`[TAKEAWAY]`

Narrow bridge: exact steps. Open field: **just the goal**.

`[STOP]`

### Beat 6.6 — One folder, loaded piece by piece · about 1 min

`[SCREEN → diagram-20]`

`[OPEN]`

Next, how long should the skill be?

`[EXPLAIN]`

Keep the body of SKILL.md under about **500 lines**. If it gets bigger, split it into other files in the same folder.

Look at this pdf folder. SKILL.md is always read first. FORMS.md, reference.md, examples.md are read only when needed. And the scripts folder is special: the scripts are **run**, not read. Only their output costs tokens.

So SKILL.md becomes a table of contents for everything beside it.

`[TAKEAWAY]`

Bundle as much as you like. **Nothing costs anything until it is opened.**

`[STOP]`

### Beat 6.7 — Keep references one level deep · about 1 min

`[SCREEN → diagram-21]`

`[OPEN]`

But be careful with how you link those files.

`[EXPLAIN]`

On the left, SKILL.md points to advanced.md, which points to details.md. That is two levels deep. The model may only skim that last file, and miss what is in it.

On the right, SKILL.md points directly to every file. One level. That is what you want.

`[TAKEAWAY]`

SKILL.md links to everything. **Nothing links further down.**

`[STOP]`

### Beat 6.8 — Checklist or loop · about 2 min

`[SCREEN → diagram-22]`

`[OPEN]`

This next one, I find the most useful of all. And not many people know it.

`[EXPLAIN]`

If your skill has many steps, give it a **checklist**. Step one, analyze the form. Step two, create the field map. And so on. The model copies the checklist into its reply, and ticks items off as it goes. A written checklist stops steps from being skipped. That is a vertical shape.

The second shape is a **feedback loop**. A circle. Make the change. Run a validator. If it fails, fix the errors, and run the validator again. Only continue when it passes.

So the skill checks its **own** work. It never moves on without reading its own output.

The more feedback loops you have in your skills, the more robust your whole product becomes.

`[TAKEAWAY]`

A checklist stops skipping. **A loop that verifies beats an instruction that hopes.**

`[STOP]`

### Beat 6.9 — Write the tests before the skill · about 2 min

`[SCREEN → diagram-23]`

`[OPEN]`

Now the big question. You wrote a skill. How do you know it actually **works**?

`[EXPLAIN]`

Anthropic's advice reorders the whole process. Write the tests **before** the skill.

Step one. Run the task with **no** skill. Step two. Write down what failed. Step three. Build three test scenarios from those failures. Step four. Write the **smallest** skill that fixes them. And step five. Run the tests again.

Let me tell you what I did for my writing-style skill. I used it to write a hundred articles. I sent every article to an AI-detection API. And I gave one rule: the skill is not done until every article scores under five percent "AI".

Only then did it go to production.

And notice who set that bar. **I** did. That is the human's job. Do not let the model make up its own criteria.

`[TAKEAWAY]`

Build the skill against **real** failures, not imagined ones.

`[STOP]`

### Beat 6.10 — Two Claudes, one skill · about 1.5 min

`[SCREEN → diagram-24]`

`[OPEN]`

And one last trick, which almost nobody uses.

`[EXPLAIN]`

Use two separate sessions.

Claude A helps you **write** the skill.

Then you open a **fresh** session, Claude B, which knows nothing about how the skill was written. Give it the skill, and let it use the skill on real tasks. And tell it to be **harsh**. Report everything that went wrong.

Then go back and improve the skill from what Claude B **actually** did. Not from guesswork.

It is like a small competition. One writes, one judges. A bit like a GAN, if you know those. And the writer is never "done" until the judge passes it.

`[TAKEAWAY]`

Improve the skill from what a **fresh session** did, not from guesswork.

`[STOP]`

---
---

# PHASE 7 — The last piece, and the Part 1 recap

*Goal of this phase: close the list of prompt pieces, and lock in Part 1.*

### Beat 7.1 — Date and folder · about 1 min

`[SCREEN → diagram-25]`

`[OPEN]`

We covered four of Pi's five pieces. The last one looks tiny, but it matters.

`[EXPLAIN]`

The **date** and the **working directory**, stamped at the end of the prompt.

Why? Say you tell your agent, "schedule the email for tomorrow, same time". Which tomorrow? The model does not know what day it is. It was trained months ago.

Or, "run the tests in this project". Which project? It needs to know the folder.

So the harness must tell it. Many people forget this. Do not.

`[TAKEAWAY]`

The model does not know what day it is. **The harness must tell it.**

`[STOP]`

### Beat 7.2 — Recap of Part 1 · about 1 min

`[OPEN]`

Let us quickly lock in part one.

`[EXPLAIN]`

One. Nine things ride into every call, but only the **conversation** is ever compacted.

Two. Pi **assembles** its prompt from five pieces, fresh every call: base template, appended text, project context, skills, and the date with the folder.

Three. Skills use **progressive disclosure**. Only the name and description are always loaded. And a good skill is short, easy to find, and **tested**.

`[TAKEAWAY]`

Now you know **what** goes into the context. Next: how to keep it under budget.

`[STOP]`

`[PHASE CHANGE]`

*— Natural break. If you are splitting this into two videos, end video 1 here. —*

Okay. Now comes the part that I think very few people in the world actually know. We are going to open up Pi and Hermes, and see exactly how they compact the context. This is part two of four.

---
---

# PART 2 — Compaction: Pi vs Hermes

---

# PHASE 8 — Why "just summarize it" is not enough

*Goal of this phase: the viewer sees that compaction has many levels of depth, and that tool results are the main cost.*

### Beat 8.1 — Level one is not enough · about 2.5 min

`[OPEN]`

Let me ask you something first.

`[ASK]` If **you** were building a harness, how would you do compaction? Pause the video and think about it for a moment.

`[EXPLAIN]`

Most people say something like this. "When the context gets close to full, I will ask another LLM to summarize the past." Some people say "a sliding window", or "throw away old tool results". Those are good thoughts.

`[SCREEN → diagram-26]`

But here is the truth. If I am interviewing someone for an AI engineer role, and I ask "how is compaction done?", and the answer stops at "ask another LLM to summarize", it tells me the person has never really built a harness. At least, not a production one.

Because that answer is only **level one**. Look at the ladder.

Level two. **When** do we start? If the window is 200,000 tokens, we cannot start at 200,000. We must start some time before. But when exactly?

Level three. **What** do we keep word for word, and what do we summarize? Do we treat all messages the same? Or keep the new ones and summarize the old ones? How many new ones?

Level four. **Where** does the cut fall? Remember, the messages are user, assistant, tool call, tool result. What if the cut lands right between a tool call and its result? Then the fresh part starts with a result, and we no longer know what question it was answering.

And level five. What if the compaction **itself** fails?

Production harnesses live up at level five. So let us climb.

`[TAKEAWAY]`

"Just summarize it" is **level one**. Production harnesses answer all five.

`[STOP]`

### Beat 8.2 — Where the tokens actually go · about 1.5 min

`[SCREEN → diagram-27]`

`[OPEN]`

Before we look at Pi, one fact you must keep in mind. Where does the context actually go?

`[EXPLAIN]`

Look at this bar. The system prompt is small. The user messages are tiny. The assistant replies are modest.

The huge part is the **tool results**. File contents. Directory listings. Build logs. Test output.

A user asks a ten-token question: "Why is the build red?" The agent runs bash, and gets back a five-thousand-line error log. Maybe sixty thousand tokens. And that log stays on the tape, and is re-sent on **every later turn**.

So this is a pattern you see in almost every agent system. The context fills up with the world the agent is **observing**, not with what anyone says.

Keep this in mind. It will explain one of the smartest things Hermes does.

`[TAKEAWAY]`

Manage the **tool results**, and most of the budget is managed.

`[STOP]`

---
---

# PHASE 9 — How Pi compacts

*Goal of this phase: the viewer can explain Pi's trigger, token count, cut point, and summary.*

### Beat 9.1 — When Pi compacts · about 1.5 min

`[SCREEN → diagram-28]`

`[OPEN]`

Let us start with Pi. Question one: **when** does Pi compact?

`[EXPLAIN]`

This long bar is the context window. The blue arrow is **contextTokens**, how many tokens we are carrying right now.

At the right end, Pi keeps a reserve. It is called **reserveTokens**, and by default it is **16,384** tokens.

The rule is simple. When contextTokens becomes bigger than the context window minus 16,384, Pi compacts.

Why keep that reserve? Because compacting itself needs room. The model still has to write a reply on the turn that triggered it. So you leave space for the answer.

`[TAKEAWAY]`

Pi compacts **early**, keeping 16,384 tokens of room to write the reply.

`[STOP]`

### Beat 9.2 — Where Pi gets the token number · about 1.5 min

`[SCREEN → diagram-29]`

`[OPEN]`

But wait. To know when we cross that line, we have to **count** the tokens. How does a harness do that?

`[EXPLAIN]`

`[ASK]` How would you measure how many tokens are in the context right now? Pause and think.

The answer is: the API tells us. Every time the model replies, the provider sends back a **usage block**. It says exactly how many tokens that call used.

So Pi finds the **last assistant reply**. Everything up to that point is exact. Pi calls that **usageTokens**.

But after that reply, a few more messages may have arrived. A tool result, maybe a new user message. The provider has not counted those yet. So Pi **estimates** them. It calls those **trailingTokens**.

And the total is simply usageTokens plus trailingTokens.

`[TAKEAWAY]`

Exact where the provider told us. **Estimated only for the newest few.**

`[STOP]`

### Beat 9.3 — Walking back to the last usage block · about 2 min

`[SCREEN → diagram-30]`

`[OPEN]`

Now, even this simple idea has an edge case. Let me show you a real walk-through.

`[EXPLAIN]`

Here are the last eight entries of a session. Numbers 21 to 28. The newest one is number 28.

Pi walks **backwards**, looking for the most recent assistant message with a **usable** usage block.

Number 28 is a user message. No usage. Number 27 is an assistant message. But look, it is red. This call was **aborted** halfway. The connection dropped. So it never got a usage block.

`[ASK]` So which message gives us the usable usage block? Pause and look at the picture.

Number **24**. The provider told us exactly: 178,900 tokens up to that point.

Then everything after it is estimated. 600, 15, 30, and 1,223. Add them up, and we get about 180,768 tokens.

`[TAKEAWAY]`

Even **counting** tokens has edge cases. A harness must handle them.

`[STOP]`

### Beat 9.4 — How Pi estimates · about 1 min

`[SCREEN → diagram-31]`

`[OPEN]`

And how exactly does Pi estimate those trailing tokens?

`[EXPLAIN]`

Simple rules.

For **text**: count the characters, and divide by four.

For a **tool call**: count the name plus the JSON arguments.

For an **image**: always count it as 4,800 characters.

These estimates deliberately run a little **high**. Why? Because compacting a little too early costs you a bit. But compacting too late crashes the call.

`[TAKEAWAY]`

A rough chars-divided-by-four rule, used **only** for the newest messages.

`[STOP]`

### Beat 9.5 — Walking backwards to find the cut · about 1.5 min

`[SCREEN → diagram-32]`

`[OPEN]`

Okay. Pi knows it must compact. Now question two: **what** does it compact?

`[EXPLAIN]`

Pi has another setting: **keepRecentTokens**, which is **20,000**.

It walks backwards from the newest message, adding up the tokens as it goes. As soon as the running total reaches 20,000, it **stops**. That is the cut.

Everything on the right of the cut, the most recent 20,000 tokens, stays **word for word**. Because that is what you are working on right now.

Everything on the left of the cut goes to the summarizer.

`[TAKEAWAY]`

Keep the most recent 20,000 tokens **untouched**. Summarize the rest.

`[STOP]`

### Beat 9.6 — Pi is not allowed to cut just anywhere · about 2 min

`[SCREEN → diagram-33]`

`[OPEN]`

Now this is where you see the real depth. Pay careful attention here.

`[EXPLAIN]`

What if that 20,000-token line lands right on a **tool result**?

Think about it. The old part gets summarized. The fresh part starts with... a tool result. An **answer**, whose **question** was just summarized away.

It is like walking into a cloakroom with a coat and no ticket. And the API will actually **reject** the whole message array.

So Pi has a list of legal places to cut. A user message: fine. An assistant message: fine. Also a bash execution, a custom entry, a branch summary, or an earlier compaction summary.

But a **toolResult**: never. A tool result must always stay attached to the tool call that asked for it.

`[TAKEAWAY]`

Cutting between a tool call and its result **breaks the history**. Pi never cuts there.

`[STOP]`

### Beat 9.7 — Two questions about the same message · about 1.5 min

`[SCREEN → diagram-34]`

`[OPEN]`

There is one more subtle thing. Pi asks two different questions about each message.

`[EXPLAIN]`

Question one: **can we cut here?** Question two: **does this message start a turn?**

A turn means: the user's question, and everything that answers it.

A user message: yes we can cut, and yes it starts a turn.

A tool result: no, and no.

But look at the assistant row. Yes, we **can** cut there. But no, it does **not** start a turn.

So this row is exactly why a cut can land in the **middle** of a turn. Pi keeps the assistant's work, but the user's question that started this turn is now on the old side.

`[TAKEAWAY]`

Every turn start is a legal cut. But **not every legal cut starts a turn.**

`[STOP]`

### Beat 9.8 — A split turn: two summaries · about 1.5 min

`[SCREEN → diagram-35]`

`[OPEN]`

So what does Pi do when the cut lands in the middle of a turn?

`[EXPLAIN]`

It makes **two** summaries.

One is the normal **history summary**, of everything before this turn. It gets a budget of 80 percent of reserveTokens.

The second one is a **turn prefix summary**: what was asked at the start of this turn, which now sits on the old side. That one gets a budget of 50 percent of reserveTokens.

Then both are joined into **one** summary message. The history summary first, then a section called "Turn Context, split turn".

So the model never loses the question it is in the middle of answering.

`[TAKEAWAY]`

A split turn means **two LLM calls**, but **one stored summary**.

`[STOP]`

### Beat 9.9 — What Pi's summary contains · about 1 min

`[SCREEN → diagram-36]`

`[OPEN]`

And what does that summary look like?

`[EXPLAIN]`

It always has the same shape. Six sections.

The **goal**. The **constraints and preferences**. The **progress**: what is done, what is in progress, what is blocked. The **key decisions**, and for each decision, **why** it was made. The **next steps**. And the **critical context**.

And then, at the end, the list of files read and modified. And notice: that list is added by **code**, not written by the model. So it is always correct.

Why a fixed shape? So that the next model always knows exactly where to look.

`[TAKEAWAY]`

A **fixed shape**, so the next model always knows where to look.

`[STOP]`

### Beat 9.10 — Pi, end to end · about 1 min

`[SCREEN → diagram-37]`

`[OPEN]`

Let us put Pi together in one line.

`[EXPLAIN]`

Start with the session entries. **prepareCompaction** counts the tokens and checks the 16,384 rule. **findCutPoint** walks back 20,000 tokens, and never stops on a tool result. Then one or two LLM calls write the summary. And you get a new, shorter context.

Pi decides **where** to cut first. Then it summarizes everything before the cut.

All of this is in Pi's open source code, in one file called compaction.ts. It is just very hard to pull out and teach, which is why I made these pictures.

`[TAKEAWAY]`

Pi: one clean cut, one summary, **one big drop** in size.

`[STOP]`

`[PHASE CHANGE]`

If you think that was detailed, wait until you see Hermes. It does almost everything differently.

---
---

# PHASE 10 — How Hermes compacts

*Goal of this phase: the viewer can explain Hermes' trigger, head-middle-tail, free pruning, micro-compaction, and its four failure guards.*

### Beat 10.1 — When Hermes compacts · about 1.5 min

`[SCREEN → diagram-38]`

`[OPEN]`

Same first question. **When** does Hermes compact?

`[EXPLAIN]`

Hermes first works out the **effective window**. That is the context length, minus **max_tokens**, the room reserved for the reply.

Then it triggers compaction at **50 percent** of that effective window.

Half! Pi waits until it is almost at the edge. Hermes starts at the halfway point.

`[TAKEAWAY]`

Pi waits for the edge. **Hermes starts at half.**

`[STOP]`

### Beat 10.2 — Three corrections to the trigger · about 1.5 min

`[SCREEN → diagram-39]`

`[OPEN]`

But that 50 percent is not the whole story. Hermes has three corrections for edge cases.

`[EXPLAIN]`

Correction one: a **floor**. Never trigger below **64,000** tokens. Otherwise a small model would compact while half its window is still empty.

Correction two: a **small window**. If the window is under **512K** tokens, raise the trigger from 50 percent to at least **75 percent**.

Correction three: **too small**. What if the window itself is smaller than the floor? For example, a 32,000-token model with a 64,000-token floor. That makes no sense. So then Hermes uses **85 percent** of the window instead.

Why am I telling you all these numbers? Because this is how harnesses are really built. Edge cases are the job.

`[TAKEAWAY]`

The rules stop a small model compacting **too early**, or **never at all**.

`[STOP]`

### Beat 10.3 — Head, middle, tail · about 2 min

`[SCREEN → diagram-40]`

`[OPEN]`

Now question two: **what** does Hermes keep? And this is a big difference from Pi.

`[EXPLAIN]`

Hermes splits the conversation into three parts.

The **head**: the system prompt, plus the **first three messages**. Kept as they are.

The **tail**: the most recent messages, about **20 percent** of the trigger, measured in tokens. Also kept word for word.

And the **middle**. Only the middle gets summarized.

Why protect the head? Think about it. When a user starts a session, they are fresh. The first few messages usually say what they **really** want. In the middle, people wander off, get distracted, try other things. So the first messages hold the **true intent**.

Pi keeps only the tail. Hermes keeps the head **and** the tail.

`[TAKEAWAY]`

The beginning and the end are protected. **Only the middle is summarized.**

`[STOP]`

### Beat 10.4 — Step one is free · about 2 min

`[SCREEN → diagram-41]`

`[OPEN]`

Now remember what I told you about tool results being the biggest part of the context? Here is where Hermes uses that.

`[ASK]` Hermes prunes old tool results before it summarizes anything. Why do you think Pi does not do this, and why is it so smart? Pause and think.

`[EXPLAIN]`

Before any summary, Hermes **prunes** old tool results. It rewrites each old tool result as one short, descriptive line.

So a huge result, say a long test log, becomes just this: "terminal: ran npm test, exit 0, 47 lines". If a tool result had a thousand-line error, you often only needed the last line anyway.

Two more rules. If the same file was read five times, only the newest copy is kept. And old images are dropped.

And here is the best part. This is fully **deterministic**. There is no LLM involved. It costs **nothing**.

So most of the space is won back **before** any model is even called.

`[TAKEAWAY]`

Most of the space is won back **before any model is called**.

`[STOP]`

### Beat 10.5 — What Hermes's summary contains · about 1 min

`[SCREEN → diagram-42]`

`[OPEN]`

Now the summary of the middle. Pi had six sections. Hermes has eleven.

`[EXPLAIN]`

Historical task snapshot. Goal. Constraints and preferences. Completed actions. **Active state**. Blocked. Key decisions. Resolved questions. **Relevant files**. Critical context. And pruned skills.

So Hermes also records the exact **working state**: what is active right now, and which files matter.

And one nice safety rule in critical context: never write an API key into the summary. Write "REDACTED" instead.

`[TAKEAWAY]`

Eleven sections, including the **exact state** of the work.

`[STOP]`

### Beat 10.6 — Hermes, end to end · about 1 min

`[SCREEN → diagram-43]`

`[OPEN]`

Let us put Hermes together.

`[EXPLAIN]`

Step one. Prune old tool results. Free.

Step two. Protect the head. Step three. Protect the tail. Also free.

Step four. Summarize the middle. This is the **only** expensive step.

And step five. The next time it compacts, Hermes does not start from zero. It **updates** the summary it already has.

`[TAKEAWAY]`

**Four cheap steps** around one expensive one.

`[STOP]`

### Beat 10.7 — Micro-compaction · about 2 min

`[SCREEN → diagram-44]`

`[OPEN]`

Hermes has one more technique that I find really beautiful. It is called **micro-compaction**.

`[EXPLAIN]`

What does Pi do? It waits until the context is full, then compacts everything at once. Batch compaction.

Micro-compaction spreads that same work out. After every completed exchange, meaning the user message, the assistant reply and the tool result, Hermes folds that **one** exchange into a **rolling summary**.

Look at the picture. E1 and E2 are already folded into the rolling summary. The red line is the cursor. E3 to E7 are not folded yet, so they are kept as they are. After the next turn, the cursor moves one step.

So when the limit comes, the summary is already ready. No big pause.

One honest note: in Hermes, this is **off by default**. You have to switch it on.

`[TAKEAWAY]`

The bill is paid in **small instalments**, instead of one large pause.

`[STOP]`

### Beat 10.8 — Two rhythms · about 1 min

`[SCREEN → diagram-45]`

`[OPEN]`

You can actually see this difference if you plot the context size over time.

`[EXPLAIN]`

Pi on the left. The context climbs, then one long pause and a big drop, then it climbs again. A sawtooth.

Hermes with micro-compaction on the right. Many tiny pauses. The line stays almost **flat**.

The same total work. Spread differently across the session.

`[OPTIONAL]`

A viewer once asked me: won't folding every turn cause problems with the KV cache? Good question. Every fold changes the conversation, so yes, the cached part after the fixed prefix has to be computed again. We will talk about caching in part three. I have not seen this documented as a problem in Hermes, so it may be handled separately. I would check before relying on it.

`[END OPTIONAL]`

`[TAKEAWAY]`

Sawtooth or flat line: **same work**, different feel for the user.

`[STOP]`

### Beat 10.9 — When compaction itself fails · about 2 min

`[SCREEN → diagram-46]`

`[OPEN]`

And now level five of our ladder. What if the compaction **itself** fails? Pi just retries. Hermes has a plan for four different failures.

`[EXPLAIN]`

Guard one: **the floor**. The system prompt and the tool schemas can never be summarized. So if a user has a huge system prompt and a thousand tools, those fixed parts alone might fill the window. Hermes knows this can happen.

Guard two: **two strikes**. If two compaction passes barely help, Hermes **stops trying**. It does not loop forever.

Guard three: **cooldown**. Summarizing needs an LLM. What if that LLM is rate-limited? Then Hermes waits **600 seconds**, ten minutes, and tries again.

Guard four: **fallback**. First it tries an auxiliary model. If that fails, the main model. And if no model is available at all, say your API bill is unpaid, it builds a summary with **no model at all**, just using character budgets. Fully deterministic.

Because compaction has to produce **something**.

`[TAKEAWAY]`

Compaction may fail. It is **never allowed to loop**.

`[STOP]`

---
---

# PHASE 11 — Pi vs Hermes, side by side

*Goal of this phase: the viewer can compare both designs in one breath.*

### Beat 11.1 — When, and where · about 1.5 min

`[SCREEN → diagram-47]`

`[OPEN]`

Let us put the two side by side.

`[EXPLAIN]`

**When.** Pi keeps a fixed reserve of 16,384 tokens. Always the same room. Hermes triggers at a percentage of what is left: 50, or 75, or 85.

Pi reserves a **constant**. Hermes reserves a **proportion**.

`[SCREEN → diagram-48]`

**Where.** Pi picks a **legal** cut point, never on a tool result, and summarizes a split turn separately.

Hermes cuts by token budget, and then **moves** the cut until the tail is valid.

`[TAKEAWAY]`

Pi **chooses** a safe boundary. Hermes **repairs** the one it took.

`[STOP]`

### Beat 11.2 — The summary, and the scorecard · about 2 min

`[SCREEN → diagram-49]`

`[OPEN]`

And the summary itself.

`[EXPLAIN]`

Both keep the decisions. Pi has six sections, plus the files read and modified. Hermes has eleven, and also keeps the **working state**.

Every harness picks its own shape. Claude Code has its own too.

`[SCREEN → diagram-50]`

So here is the full scorecard.

When: window minus 16,384, versus 50 percent of the effective window.

What is kept: the last 20,000 tokens, versus head and tail.

Summary: six sections versus eleven.

Free step: Pi has none. Hermes prunes tool results first.

If it fails: Pi retries. Hermes has the floor, two strikes, cooldown, and fallback.

And Hermes can also micro-compact every turn.

This is a big reason, I feel, why Hermes has become so popular. They thought about these edge cases very carefully. When you ship to production, your users never see compaction, so it simply has to **work**.

`[TAKEAWAY]`

Same problem. **Two very different designs.** Both are valid.

`[STOP]`

`[PHASE CHANGE]`

Now, there is a third harness I want to show you. One that takes a completely different approach to where compaction even lives. This is part three of four.

---
---

# PART 3 — DeepSeek Harness, and the cache

---

# PHASE 12 — How DeepSeek Harness compacts

*Goal of this phase: the viewer knows DeepSeek Harness' design (a plugin on an append-only log), its trigger, its pipeline, and its summary shape.*

*(Facts from the DeepSeek Harness repository: `deepseek-ai/deepseek-harness`, package `dsh-compaction-basic`. Check the README for the current defaults before recording.)*

### Beat 12.1 — Compaction is a plugin · about 1.5 min

`[SCREEN → diagram-51]`

`[OPEN]`

DeepSeek has an open-source harness too. It is called **DeepSeek Harness**. And its big idea is about **where** compaction lives.

`[EXPLAIN]`

In Pi and Hermes, compaction is built **into** the harness.

In DeepSeek Harness, the core agent loop is kept small, and compaction is a **plugin**. The loop only has a socket, a "seam", called **ctx.compaction**. And you plug an engine into it.

The basic engine is a package called **dsh-compaction-basic**. That is the one that folds.

There is an optional **tool-result pruner**. It trims big tool outputs first. Sounds familiar? It is the same idea as Hermes' free step.

And there is a command package that gives you a **/compact** command, so you can trigger it by hand.

So if you want a different summarizer, you swap the plugin. You do not touch the loop.

`[TAKEAWAY]`

Pi and Hermes build compaction **in**. DeepSeek Harness **plugs it in**.

`[STOP]`

### Beat 12.2 — The log never forgets · about 1.5 min

`[SCREEN → diagram-52]`

`[OPEN]`

The second big idea is even more interesting. In DeepSeek Harness, compaction **never deletes anything**.

`[EXPLAIN]`

Every session is an **append-only log** of events. Things are only ever added. Never removed.

What the model actually sees is **derived** from that log. They call it the **surface**.

When compaction happens, it does not delete old events. It only changes the surface. One summary, wrapped in a tag called **compacted-summary**, replaces a range of old messages. They call that range the "shadowed range". The recent tail stays intact.

And the compaction itself is written into the log as events: compaction start, compaction summary, compaction end. These are log-only events, so the model does not see them.

So compaction is lossy for the **model**, but not for **you**. If you ever need the exact old text, you read it back from the log.

`[TAKEAWAY]`

The model sees a summary. **The log keeps everything.**

`[STOP]`

### Beat 12.3 — When DeepSeek Harness compacts · about 1.5 min

`[SCREEN → diagram-53]`

`[OPEN]`

Same first question again. **When?**

`[EXPLAIN]`

DeepSeek Harness uses **two** limits, and whichever comes first wins.

Limit one: **80 percent** of the window.

Limit two: the window, minus the output cap, minus an extra headroom of **65,536** tokens.

The trigger is the smaller of the two.

And after compaction, it keeps the newest **16 percent** of the window minus the output cap, word for word.

Let me show you why the two limits matter. Look at the table.

A 200,000-token model with a 32,000 output cap. 80 percent is 160,000. But the headroom rule gives about 102,000. That is smaller, so that one fires first.

Now a one-million-token model, same output cap. 80 percent is 800,000. The headroom rule gives about 902,000. Now the 80 percent rule fires first.

So on a small window, the headroom rule bites. On a huge window, the 80 percent rule bites. You could say it is Pi's fixed reserve and a Hermes-style percentage, **both at once**.

`[TAKEAWAY]`

Two limits, **whichever bites first**. Then keep the newest 16 percent.

`[STOP]`

### Beat 12.4 — End to end · about 2 min

`[SCREEN → diagram-54]`

`[OPEN]`

Now let us walk through the whole pipeline.

`[EXPLAIN]`

There are **two triggers**.

Trigger one is **pressure**. It is checked **before** the request is built, every step. That is the normal one.

Trigger two is **overflow**. That is when the provider actually comes back with an error: context window exceeded. That happens **after** a failed call.

Both go into the same pipeline.

First: prune tool results, if the pruner plugin is installed. Free. No model call.

Then re-measure. If it fits now, **skip the summary**. Done. That saves a whole LLM call.

If it still does not fit, make **one** summary call. And here is a clever detail. That call replays the same system prompt and the same tools, so that the provider's **prefix cache stays warm**. We will understand why that matters in a few minutes.

The summary replaces the oldest span.

For an overflow, it shrinks harder in one pass, and retries **once**. That setting is called maxOverflowRetries, and its default is one.

And if the summary fails? It logs a warning, and carries on with the full history. It does not crash.

`[TAKEAWAY]`

Two triggers, **one pipeline**: prune for free first, summarize only if needed.

`[STOP]`

### Beat 12.5 — DeepSeek's summary shape · about 1 min

`[SCREEN → diagram-55]`

`[OPEN]`

And DeepSeek's summary also has a fixed shape.

`[EXPLAIN]`

Eight sections. Primary request and intent. Key technical concepts. Files and code. Errors and fixes. Pending jobs. Current work. Next step. And critical context.

It is wrapped in that compacted-summary tag, and the model is told: this is a checkpoint, continue, and do not acknowledge it. So the model does not stop and say "thanks for the summary".

Only the summary **text** is kept. No reasoning, no tool calls.

And it is honest about its limits. It cannot shrink the system prompt, the tools, or one single giant tool call.

`[TAKEAWAY]`

Pi: six sections. Hermes: eleven. **DeepSeek Harness: eight.**

`[STOP]`

### Beat 12.6 — Three harnesses side by side · about 1 min

`[SCREEN → diagram-56]`

`[OPEN]`

Let us put all three on one page.

`[EXPLAIN]`

When. Pi: window minus 16,384. Hermes: 50 percent of effective. DeepSeek: the smaller of 80 percent, or window minus output minus 65,536.

Keep. Pi: last 20,000 tokens. Hermes: head and tail. DeepSeek: newest 16 percent.

Free step. Pi: none. Hermes: prune tool results. DeepSeek: an optional pruner.

Summary. Six, eleven, eight sections.

On failure. Pi retries. Hermes has four guards. DeepSeek warns and carries on, and retries an overflow once.

Same five questions. Three different answers.

`[TAKEAWAY]`

There is no single right design. There are **trade-offs**.

`[STOP]`

### Beat 12.7 — Inside the DeepSeek model `[OPTIONAL]` · about 1.5 min

`[OPTIONAL]`

`[SCREEN → diagram-57]`

`[OPEN]`

One last thing about DeepSeek. Context management does not only live in the harness. It also lives in how the **model** was trained.

`[EXPLAIN]`

In the DeepSeek-V3.2 paper, they describe a rule for the model's own **thinking** during tool use.

While tool results keep arriving, the thinking is **kept**. The model can keep reasoning across many tool calls.

But when a **new user message** arrives, the old thinking is **dropped**. The tool calls and their results stay. Only the old reasoning goes.

And for their search agents, they also tested strategies for when the context is nearly full. One of them, called "discard all", simply wipes the tool history and keeps the original question. And surprisingly, simple strategies like that worked really well.

`[TAKEAWAY]`

Context management lives in the harness **and** in how the model was trained.

`[STOP]`

`[END OPTIONAL]`

---
---

# PHASE 13 — Prompt caching

*Goal of this phase: the viewer understands why the cache exists, and why compaction affects it.*

### Beat 13.1 — Stop paying twice · about 2 min

`[SCREEN → diagram-58]`

`[OPEN]`

Now I want to talk about something that is not discussed very often, but it matters a lot for cost. **Prompt caching.**

`[EXPLAIN]`

Think about what our loop does. Every single turn, we re-send **everything**. The system prompt, every tool schema, every earlier turn. Just to add one new tool result at the end and ask "what next?"

The model is stateless, so yes, it needs the whole thing. But the beginning is the **same** every time.

So the provider can keep the work it already did. Look at the picture. Call one: everything is new. Call two: the same prefix is **cached**, only the new part is computed. Call three: the cached part is even longer.

The point where caching starts is marked with something called **cache_control**. A breakpoint.

Why does this save money? If you have taken an inference course, you know there are two phases: **prefill** and **decode**. In prefill, the model computes the key and value vectors for every input token. For the cached part, those K and V vectors are **already computed**. So no prefill for that part.

That means a lower bill, and a lower **TTFT**, time to first token. The answer starts faster.

And one more word: **TTL**, time to live. How long the cache is kept. For example, five minutes, or one hour. Different harnesses support different TTLs. Pi, for example, supports the one-hour TTL.

So even if the provider caches automatically, the harness should say **where** the breakpoints go and **how long** to keep them.

`[TAKEAWAY]`

The model is stateless. The cache is how you **stop paying twice** for the same prefix.

`[STOP]`

### Beat 13.2 — Every fold breaks the cache once · about 1.5 min

`[SCREEN → diagram-59]`

`[OPEN]`

Now connect this to compaction. What happens to the cache when we compact?

`[EXPLAIN]`

Before the fold: the system prompt and tools are cached. The long history is cached. Only the new message is new.

After the fold: the system prompt and tools are **still** cached, because they did not change. But the summary is new. And the recent messages now sit in a different position, so they must be computed again.

So every fold costs you **one cache miss**.

Two rules come out of this.

Rule one. Keep the system prompt and the tools **stable**, and at the **front**. Then they stay cached across every fold. That is exactly why DeepSeek Harness replays them in its summary call.

Rule two. If you fold **every turn**, like micro-compaction, you get a cache miss **every turn**. That is the price of a flat line.

`[TAKEAWAY]`

Fold rarely, fold cleanly, and **keep the front of the prompt still**.

`[STOP]`

`[PHASE CHANGE]`

Okay. We have seen how the best harnesses do it. Now it is our turn. Let us build compaction into Zill. This is part four of four.

---
---

# PART 4 — Build it

---

# PHASE 14 — Zill's compaction, and the build

*Goal of this phase: the viewer understands Zill's simple fold, the seam, and runs the build.*

### Beat 14.1 — Zill's fold: one fold, two halves · about 2 min

`[SCREEN → diagram-60]`

`[OPEN]`

Pi and Hermes have thousands of lines for this. Zill is a minimal harness. So we keep only the **core idea**.

`[EXPLAIN]`

Here is the whole mechanism in one breath.

When the tape is over budget, cut it in two.

The **old half**, everything except the last six messages, goes to **one** LLM call, which writes a summary.

The **recent half**, the last six messages, is kept **word for word**. Six is a constant called **KEEP_RECENT**.

The new tape is short. One summary message that starts with "Conversation so far, compacted". Then the six kept messages.

And we borrow three cheap ideas from what we saw today.

From Hermes, we protect the **head** in a small way: the user's original request is copied into the summary **word for word**, so it survives any number of folds.

Also from Hermes, tool results are **clipped hard** before we send them to the summarizer. They are the bulk.

And from Pi and Hermes, the summary has **fixed sections**: goal, constraints, progress, decisions, files, errors, next steps.

And our token meter is the simplest one: characters divided by four. Exactly Pi's estimate rule.

`[TAKEAWAY]`

Summarize the past. **Keep the present sharp.**

`[STOP]`

### Beat 14.2 — The seam · about 1.5 min

`[SCREEN → diagram-61]`

`[OPEN]`

Our simple fold has exactly the problem we saw in Pi. Let us find it.

`[EXPLAIN]`

The place where the summary meets the kept slice is called the **seam**.

Our cut "keep the last six" does not know about tool calls and results. Look at the left. The cut falls between "write four.txt", the call, and "Wrote four.txt", its result.

So after the fold, look at the right. The kept slice starts with a tool result whose call was summarized away. An **orphan**. The coat with no ticket. And the API rejects it.

The fix is one line. While the kept slice starts with a tool message, drop it.

And notice what we do **not** do. We do not invent a fake call to match it. That would be lying to the agent about its own past. Dropping the orphan is safe, because its meaning is already in the summary.

It is the same rule as Pi's "never cut on a toolResult", done the cheap way.

`[TAKEAWAY]`

An orphan tool result is **dropped**, never patched with a fake call.

`[STOP]`

### Beat 14.3 — What we build today · about 1.5 min

`[SCREEN → diagram-63]`

`[OPEN]`

So here is exactly what we build today.

`[EXPLAIN]`

One new file: **zill/context.py**. Two constants: four characters per token, and keep the six most recent. And five small functions. estimate_tokens, the meter. render, which turns old messages into a transcript. compact, the fold itself. mend, which fixes the seam. And a fallback summary that needs no model at all, Hermes' last resort, in case the summarizer is down.

One tiny change in **loop.py**: a new socket called **before_turn**. Before every model call, the loop hands the tape to this function, and uses whatever comes back. That is how compaction plugs in. A bit like DeepSeek Harness: the loop does not even know compaction exists.

A **test file**, with a fake model, so the tests need no network.

And a **demo**, with a budget of only 1,500 tokens, absurdly small, so we can watch the fold happen in front of us.

`[TAKEAWAY]`

One file, one socket, one test file, **one demo**.

`[STOP]`

### Beat 14.4 — The build · about 5 min

`[OPEN]`

Okay. Let us build it. Open Claude Code in your Zill repository, and paste this prompt.

`[DO]` Paste the prompt below into Claude Code, in the Zill repo. (Also saved as `zill-lecture4-build-prompt.md`.)

```text
You are building the next part of Zill (lecture 4 of the series): context
management, meaning the compaction fold that keeps the message array under a
token budget. The parts are cumulative. Your repo already contains the package
zill/ with provider.py (complete(model, system, messages, tools) returns
{"text", "tool_calls", "usage": {"input", "output"}} and uses the neutral
message format {"role": "user"|"assistant"|"tool", "text", ...}), loop.py
(run_loop with the on_event and before_tool sockets), tools.py, operations.py,
security.py, plus demos/ and tests/ from lectures 2 and 3.

Today adds ONE new file, zill/context.py, and ONE small socket in loop.py.
Build exactly what this spec describes and nothing else.

GROUND RULES
- Python 3.10+, standard library only, no third-party packages.
- Must run on Windows, macOS and Linux.
- Same code standard as before: a module docstring on every file naming the
  concept it teaches and the design rules it embodies; a docstring on every
  public function; a short comment wherever behaviour is subtle (the seam,
  the fallback, the "never loop" rule).
- Size targets including documentation, within about 15%: context.py 120
  lines, the loop.py change 10 lines or fewer, tests 140, demo 70.
- Commit after each milestone: loop socket, context.py, tests, demo.
- Do not add features beyond this spec. Where the spec is ambiguous, pick the
  simpler option and note it in a one-line comment at the top of the file.
- Read provider.py and loop.py before you start, and match their names and
  message shapes exactly. If anything below contradicts them, stop and report
  it instead of guessing.

THE ONE IDEA TO PRESERVE
One fold, two halves. When the tape (the message array) is over budget, the
OLD half is folded into one model-written summary message, and the RECENT half
(the last KEEP_RECENT messages) is kept word for word. Summarize the past,
keep the present sharp. The system prompt and the tool definitions are never
part of the fold. They are not in the messages list at all.

------------------------------------------------------------------------------
1) zill/loop.py: the only change allowed to an existing file
------------------------------------------------------------------------------
- Add a keyword parameter before_turn=None to run_loop.
- At the start of every turn, BEFORE provider.complete is called:
    if before_turn is set: messages[:] = before_turn(messages)
  Replace the list IN PLACE, so the caller's list shows the fold too.
- If before_turn raises, report it through on_event (or print one line) and
  continue the turn with the unchanged messages. A broken compactor must never
  kill the run.
- Nothing else in loop.py changes. All existing tests must still pass.

------------------------------------------------------------------------------
2) zill/context.py: the fold
------------------------------------------------------------------------------
Constants
  CHARS_PER_TOKEN = 4       # a budget meter, not a tokenizer
  KEEP_RECENT     = 6       # never summarize the freshest messages
  CLIP_CHARS      = 600     # per message, in the transcript we summarize
  CLIP_TOOL_CHARS = 300     # tool results are clipped harder: they are the bulk
  MARKER          = "[Conversation so far, compacted]"
  SUMMARY_INSTRUCTION = a system prompt for the summarizer that says:
    You compress agent transcripts into a handover note. Use exactly these
    headings: Goal; Constraints and preferences; Progress (done / in progress /
    blocked); Key decisions and why; Files created or edited and their purpose;
    Unresolved errors; Next steps. Be dense and factual, and stay under 250
    words, because the summary itself rides on every later call. Never copy
    secrets such as API keys or passwords: write [REDACTED].

estimate_tokens(messages) -> int
  Sum of len(str(m)) over the list, integer-divided by CHARS_PER_TOKEN.
  The docstring says plainly that this is a rough estimate, which is enough
  because we fold long before the hard ceiling.

render(messages) -> str
  A plain-text transcript, one block per message:
    [role]                   for user and assistant messages
    [tool: <name>]           for tool messages
  followed by the text clipped to CLIP_CHARS (CLIP_TOOL_CHARS for tool
  messages), with " …[clipped N chars]" when something was cut. For an
  assistant message, add one line per tool call: "-> called <name>(<args>)"
  with the arguments clipped to 120 chars. A message whose text starts with
  MARKER (an earlier summary) is kept up to 4,000 chars, because an earlier
  summary must survive into the next one.

original_request(messages) -> str | None
  The text of the first user message that does not start with MARKER. If the
  first message IS an earlier summary, return the text after its
  "Original request (verbatim):" line instead, so the original request
  survives any number of folds.

compact(model, messages, budget_tokens, complete=None, on_compact=None) -> list
  - complete defaults to provider.complete. It is injectable so that the tests
    need no network.
  - If estimate_tokens(messages) <= budget_tokens, or len(messages) <=
    KEEP_RECENT + 1: return messages unchanged (the same object).
  - old, kept = messages[:-KEEP_RECENT], messages[-KEEP_RECENT:]
  - kept = _mend(kept)                     # see THE SEAM below
  - summary = ONE call to complete(model, SUMMARY_INSTRUCTION,
      [{"role": "user", "text": "Summarize this transcript:\n\n" + render(old)}],
      <no tools: pass the empty value that provider.complete accepts>)["text"]
  - If that call raises or returns empty text, do not crash. Use
    _fallback_summary(old) instead, and start it with
    "(fallback summary: the summarizer was unavailable)".
  - head = MARKER + "\nOriginal request (verbatim): " + original_request(messages)
    (clipped to 2,000 chars, omitted if None) + "\n\n" + summary
  - Roles must still alternate correctly. If kept[0] is a user message, merge
    head into it: {"role": "user", "text": head + "\n\n---\n\n" + kept[0]["text"]}.
    If kept is empty after mending, return [{"role": "user", "text": head}].
    Otherwise return [{"role": "user", "text": head}] + kept.
  - Return a NEW list. Never mutate the input list or its message dicts.
  - If the result is STILL over budget, return it anyway. One fold per call,
    never a retry loop. (Hermes' lesson: compaction may fail, it may never
    loop.) The next turn can fold again.
  - If on_compact is given, call on_compact(tokens_before, tokens_after, head)
    after a fold, so a demo can show it.

THE SEAM: _mend(kept) -> list
  The cut before the last KEEP_RECENT messages does not know about call and
  result pairs. If it lands between a tool call and its result, the kept slice
  starts with an ORPHAN tool result whose call was summarized away, and the
  API rejects the whole array. Drop leading messages whose role is "tool"
  until the slice starts on a legal message. Never invent a fake call to match
  an orphan: its meaning is already in the summary. If provider.py pairs
  results with calls by an id, also drop any tool message in kept whose id has
  no matching call in kept.

_fallback_summary(old) -> str
  A deterministic summary with no model at all (Hermes' last resort): the
  tool names used with counts, the paths passed to write_file / edit_file, the
  last three tool results that contain "ERROR" (each clipped to 200 chars),
  and the last assistant text (clipped to 500 chars). Clip the whole thing to
  3,000 chars.

Wiring: the caller passes
  before_turn=lambda msgs: compact(model, msgs, budget_tokens)
to run_loop. Nothing else needs to know that compaction exists.

------------------------------------------------------------------------------
3) demos/context_demo.py: watch the fold happen
------------------------------------------------------------------------------
- Budget from argv, default 1500 tokens (absurdly small on purpose). If that
  default produces no fold with this provider, lower it until it does, and
  report the value you chose.
- Reuse the tools and permission setup from demos/build_demo.py (lecture 3),
  in a fresh temporary folder, so that the demo runs unattended.
- before_turn wraps compact: before each model call it prints
  "turn N: sending X tokens". When a fold happens, it prints
  "*** compacted: X -> Y tokens ***" and the first 600 chars of the head.
- Task: "Create five files one.txt through five.txt, each with 20 lines of the
  word ping, one write_file at a time with a read_file check after each; then
  write MANIFEST.md listing each file and its line count, verified by counting
  the lines (wc -l, or a Python one-liner on Windows)."
- After the run, check from Python that all five files have 20 lines and that
  MANIFEST.md names all five. Print PASS or FAIL, and the number of folds.
  With the default budget, zero folds also means FAIL.

------------------------------------------------------------------------------
4) tests/test_zill_context.py: stdlib unittest, fake complete, no network
------------------------------------------------------------------------------
a) estimate_tokens: a message of about 400 chars gives about 100 tokens.
b) Under budget: compact returns the very same object.
c) KEEP_RECENT + 1 messages, over budget: returned unchanged.
d) Over budget: the result starts with MARKER, ends with the last kept
   messages unchanged, has at most 1 + KEEP_RECENT messages, and the input
   list is not mutated.
e) The seam: when the kept slice would start with a tool message, that message
   is dropped; when every kept message is a tool message, the result is the
   head message alone.
f) Original request: after TWO folds (fold, append more messages, fold again)
   the first user request is still present word for word.
g) A summarizer that raises: the fallback is used, no exception escapes, and
   the result is shorter than the input.
h) A 50,000-char tool result appears clipped in the transcript sent to the
   summarizer (the fake complete records what it receives).
i) Alternation: when the kept slice starts with a user message, the head is
   merged into it and no two user messages are adjacent.
j) The loop socket: run_loop with a fake provider calls before_turn once per
   turn, replaces the list in place, and survives a before_turn that raises.

------------------------------------------------------------------------------
VERIFY BEFORE FINISHING: report each one honestly, with the output
------------------------------------------------------------------------------
(a) All tests pass, including the lecture 2 and 3 tests.
(b) demos/context_demo.py with the default budget of 1500 folds at least once
    and prints PASS.
(c) The same demo with budget 100000 never folds and also prints PASS.
(d) Paste one real summary head that the demo produced.
(e) git log shows today's commits.
If something cannot be verified (for example, no API key), say so plainly
instead of claiming success.
```

`[SAY]` While this runs, look at a few things in the prompt.

`[SAY]` First, it says: today adds ONE file and ONE socket, and nothing else. A good prompt keeps the change small, so you can review every line of it.

`[SAY]` Second, look at the rules inside compact. "Return a NEW list, never mutate the input." And: "if the result is still over budget, return it anyway. One fold per call, never a retry loop." That is Hermes' lesson: compaction may fail, it may never loop.

`[SAY]` And third, look at the verify section at the end. It says what "done" looks like: tests pass, the demo folds at least once and prints PASS, and with a huge budget it never folds and still passes. And it says: if you cannot verify something, say so honestly.

### Beat 14.5 — Watch it fold · about 3 min

`[SCREEN → diagram-62]`

`[OPEN]`

Now the fun part. Let us watch compaction happen.

`[DO]` Run the demo with the default budget of 1,500 tokens.

```bash
python demos/context_demo.py
```

`[SAY]` Look at the counter. Turn one, a few hundred tokens. Then it climbs. 900. 1,300. 1,600.

`[SAY]` And there. "Compacted." The number drops. That dip is Zill writing its own recap. It just replaced the whole history with one paragraph.

`[SAY]` And look, the task keeps going. It writes four.txt, five.txt, and then MANIFEST.md. And at the end: PASS. The task never noticed that its memory was folded.

`[SAY]` This is exactly the sawtooth from the picture. Climb, fold, climb, fold.

`[DO]` Scroll up and show the summary head it printed.

`[SAY]` Read this summary. "Original request, verbatim." The whole task, word for word. Then files created: one, two, three. Decisions. And what remains to be done. Exactly what a colleague would want in a handover note.

`[DO]` Run it again with a huge budget.

```bash
python demos/context_demo.py 100000
```

`[SAY]` Now it never folds, and it still passes. So compaction does not change **what** the agent does. It only lets it keep going past its own window.

`[TAKEAWAY]`

That dip is Zill writing its own recap, **and the task never notices**.

`[STOP]`

---
---

# PHASE 15 — Closing and homework

*Goal of this phase: the viewer leaves with the three decisions, and a clear homework.*

### Beat 15.1 — Three decisions you must make · about 1.5 min

`[SCREEN → diagram-64]`

`[OPEN]`

Let me leave you with the one thing I want you to remember from today.

`[EXPLAIN]`

It is not enough to know the components of a context. That is only the start.

If you design your own harness, compaction comes down to three decisions.

**When** do I compact? A fixed reserve like Pi, a percentage like Hermes, or both like DeepSeek.

**How** do I compact? What is kept exact, where the cut falls, and what is pruned for free.

**What** does the summary look like? Which sections must always survive?

And for production, one more. What happens when compaction **fails**?

`[TAKEAWAY]`

When, how, and what. **And what if it fails.**

`[STOP]`

### Beat 15.2 — Homework · about 1.5 min

`[OPEN]`

Before the next lecture, I want you to do three things.

`[EXPLAIN]`

One. Run the demo with a small budget, and **read the summary** Zill wrote about itself. Mark one thing it dropped that you think was important. Then change the summary instruction so that it keeps it.

Two. Play with the two numbers. Change **KEEP_RECENT** from six to two, and then to twelve. Change the budget. Watch how often Zill folds, and whether the task still passes. You will feel the trade-off we talked about all lecture.

Three. Pi and Hermes are not the only ones. **Codex** compacts in yet another way. Its techniques are public. Go and compare it with Pi, Hermes and DeepSeek Harness. Ask yourself the same five questions.

Thank you so much for watching, and I will see you in the next lecture.

`[TAKEAWAY]`

When, how, what, and what if it fails. **Ask these of every harness you meet.**

`[STOP]`

---
---

## Notes for you (not spoken)

### Picture cue list

| Beat | Picture | What it shows |
|------|---------|---------------|
| 0.1 | 01 | Where we are: 5 files done, context.py today |
| 0.2 | 02 | Context engineering vs context management |
| 1.1 | 03 | Context is the fuel |
| 1.2 | 04 | The tape only grows (bar chart) |
| 2.1 | 05 | Nine things in every call, only 4–6 compacted |
| 2.2 | 06 | System prompt / user / assistant |
| 3.1 | 07 | Pi's buildSystemPrompt: five pieces |
| 3.2 | 08 | Same template, three prompts |
| 4.1 | 09 | AGENTS.md walk-up |
| 4.2 | 10 | Walk again on every rebuild |
| 5.1 | 11 | A skill file is a trailer |
| 5.2 | 12 | Three levels of loading |
| 5.3 | 13 | Tool vs skill |
| 5.4 | 14 | My writing-style skill |
| 6.1 – 6.10 | 15 – 24 | Say less · two fields · description · name · freedom · folder · one level · checklist/loop · tests first · two Claudes |
| 7.1 | 25 | Date and folder |
| 8.1 | 26 | "Just summarize it" is level one (ladder) |
| 8.2 | 27 | Where the tokens go |
| 9.1 – 9.10 | 28 – 37 | Pi: when · token number · walk back · estimate · cut · legal cuts · two questions · split turn · summary · end to end |
| 10.1 – 10.9 | 38 – 46 | Hermes: when · corrections · head/middle/tail · free pruning · summary · end to end · micro-compaction · two rhythms · failure guards |
| 11.1 – 11.2 | 47 – 50 | Pi vs Hermes: when · where · summary shapes · scorecard |
| 12.1 – 12.7 | 51 – 57 | DeepSeek Harness: plugin · log · when · end to end · summary · three-way table · DeepSeek model |
| 13.1 – 13.2 | 58, 59 | Prompt caching · every fold breaks the cache once |
| 14.1 | 60 | Zill's fold |
| 14.2 | 61 | The seam |
| 14.3 | 63 | What we build today |
| 14.5 | 62 | The sawtooth (show while the demo runs) |
| 15.1 | 64 | Three decisions |

All pictures: `diagrams-lecture4/diagram-01.png` … `diagram-64.png`. To re-export one after an edit, open `zill-lecture4-diagrams.html?s=N` in a browser (or with headless Edge, as before).

### If the video is too long, cut in this order

1. Beat 12.7 (inside the DeepSeek model). It is already marked optional.
2. Beat 10.8's optional note about the KV cache.
3. Beats 6.6 and 6.7 (folders and one-level references). Mention them in one sentence instead.
4. Beat 9.4 (how Pi estimates). Keep 9.3, which already shows the idea.
5. Split into two videos at the natural break after Phase 7.

### Things to verify before recording

- **Pi numbers**: reserveTokens 16,384; keepRecentTokens 20,000; split-turn budgets 80% / 50%; the image estimate 4,800 chars; the candidate filenames; the legal cut entry types. These come from your book's Pi section. Check them against Pi's `compaction.ts` and resource loader if Pi has updated.
- **Hermes numbers**: 50% trigger, 64,000 floor, 512K → 75%, 85% rule, head = first 3 messages, tail = 20%, 600-second cooldown, 11 sections, micro-compaction off by default. Also from your book. Check against the current Hermes source.
- **DeepSeek Harness numbers**: `thresholdRatio 0.8`, `headroomTokens 65536`, `retainRatio 0.16`, `maxOverflowRetries 1`, `compactionRetries 1`, the eight summary sections, and the `<compacted-summary>` wrapper all come from the `dsh-compaction-basic` README in `deepseek-ai/deepseek-harness`. The maintainers note that the 0.8 / 0.16 defaults have no recorded corpus justification. Re-read the README before recording, because defaults change.
- **DeepSeek-V3.2 (Beat 12.7)**: the rule about keeping thinking across tool calls and dropping it on a new user message is from the V3.2 paper (arXiv 2512.02556). The "discard all" strategy is described in that paper's search-agent context-management section. I did not quote any score, so do not add numbers without checking the paper.
- **Anthropic skill rules** (64 / 1,024 chars, no "claude"/"anthropic" in names, under 500 lines, one level deep): from Anthropic's skill authoring best-practices page. Check that page once.
- **Prompt caching TTL**: 5 minutes default and 1 hour optional are Anthropic's options. "Pi supports the 1-hour TTL" is from your transcript. Check it in Pi's provider code.
- **The build prompt has not been run yet.** Run it once before recording, so the demo output you show on camera is real. The line counts on diagram 63 (≈110) are targets, not measured.
- First-person stories (the writing-style skill, the 100-article test, the interview remark) are yours from the transcript. Keep them only if they are true for you.
