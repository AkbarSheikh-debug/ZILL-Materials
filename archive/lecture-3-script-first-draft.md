# Harness Engineering Series — Lecture 3: Tools and Security

**Speaking script, spoken-voice version.** This is the third lecture in the series. Lecture 1 gave the vocabulary. Lecture 2 built the loop (`provider.py` and `loop.py`). This lecture gives Zill its hands (`tools.py`) and its conscience (`security.py`).

**How to read this file**
- Normal text = say it aloud, as written.
- `[SHOW diagram-NN — …]` = put that picture on screen (from `diagrams-lecture3/`, 1920×1080, same hand-drawn style as before).
- ✍️ **WRITE ON THE BOARD** = write exactly this, live, while you talk. Viewers who see you writing remember more, and they can copy it into their notes.
- 🎨 **YOU DRAW THIS** = a small diagram to draw yourself, with the exact steps. These are the ones where drawing slowly beats any ready-made picture. **The full step-by-step guide, with a layout sketch for each drawing, is in "DRAWING GUIDE" near the end of this file.**
- 🛑 **PAUSE** = tell the viewer to pause the video and answer before you continue.

Rough length: 50–60 minutes of speaking, plus the live build.

---

# PART A — Welcome back, and why tools

## 1. Welcome, and a quick revision of Lecture 2

`[SHOW diagram-01 — Where we left off]`

Hello everyone, and welcome back to the Harness Engineering series. This is lecture number three.

In today's lecture we are going to learn about two things. Number one is tools. And number two, which is just as important, is security. Both of these go into the harness together, and by the end of the lecture you will see why they cannot be separated.

But before that, let me quickly revise what we did in the last lecture. Because everything today plugs into it.

In the last lecture we looked at the heartbeat of every agentic harness. That is the loop. The thought, action, observation loop. Whatever harness you look at, open source or closed source, Claude Code, Codex, Pi, Hermes, you will find this loop inside.

The prompt which you give goes to the model. And we keep a list called the messages array, which keeps on growing, lap after lap.

Now here is a question for you. 🛑 **PAUSE the video** and answer: what all does this messages array consist of? Just write down whatever comes to your mind.

...

Okay. Some of you must have written the system prompt, the user prompt, the tools. Good. But the full answer is bigger than that. The array carries the system prompt, the user prompt, the tool descriptions, the skill files, your project instruction file, any documents you retrieve, and then the whole back-and-forth of the conversation so far. And every single time, the whole thing goes to the model again.

And in many harnesses, when the context gets too big, the back-and-forth part is what gets compacted. The standing parts, like the system prompt and the tool descriptions, are kept. We will see exactly how that works in the next lecture.

Now the reason I find this beautiful is that such a small loop drives such powerful systems. At the end of the last lecture we had two code files. `provider.py`, the doorway to the model. And `loop.py`, the ten-line heartbeat.

If you do not have these two files with you, please go back to the last lecture and build them first. Everything today sits on top of them.

Now look at this picture, because this is exactly where we are going to plug in today. Our `loop.py` has two sockets. Socket one is the list of tools. Right now it has only a dice roller in it. Socket two is a function called `before_tool`, which can say yes or no to any call before it runs. Right now it says yes to everything.

Today, we fill socket one with `tools.py`. These are the hands. Alongside it we write `operations.py`, which decides **where** those hands work: on your machine, on a remote machine, or inside a sandbox. And we fill socket two with `security.py`. This is the conscience.

And look at what is written at the bottom. The loop never learns the names of the tools. That is why `loop.py` does not change today. We will not touch it. Not a single line. That is what good layering looks like.

> ✍️ **WRITE ON THE BOARD**
> **LECTURE 3 — TODAY**
> 1. Tools → `tools.py` → the HANDS (what a tool does)
> 2. Backends → `operations.py` → WHERE it runs: local · ssh · sandbox
> 3. Security → `security.py` → the CONSCIENCE
> `loop.py` does NOT change.

---

## 2. What is a tool? Brain in a jar

`[SHOW diagram-02 — A brain in a jar]`

So let us start with the very first question. What is a tool? And why should we care about tools in a harness engineering course?

Let me explain it first in a very intuitive manner, and then we will go technical.

Remember what we said in the last lecture. The language model is the engine of a car. It is powerful. But an engine by itself does not take you anywhere. Tools are the wheels. Tools are what let this engine actually go somewhere.

Another way to think about it is the brain in a jar. Imagine a brain sitting inside a glass jar. It can think. It can think very well. But it cannot touch anything. It cannot open a door. It cannot send a message. It is isolated.

Tools break that glass. Once you give the model a tool, it can reach out of the jar and touch the outside world.

And what is the outside world? It can be anything. Your GitHub repository. Your terminal. Your Google Drive. Your Slack. An API like Zoom or Jira or Notion. Think of yourself as a worker. In your day job, as a software developer or a researcher, you use APIs, you run commands, you use so many softwares. Giving the model tools means giving it access to all of that.

And this is exactly the A in thought, action, observation. This is the action. When that research paper on ReAct became famous, the key realization was that the action part can be done through tools.

Now, if you have studied agents in a basic course, they usually treat tools as a toy idea. Like a weather API. But in this series we are building a real harness for real software work. So for us, tools are a lot more concrete.

If you are building a real project, you may want Jira, Notion, Salesforce, GitHub. These are everyday enterprise software. You want your harness to touch them. And to do that you either connect an MCP server, or you write your own script. Both of them count as tools.

> ✍️ **WRITE ON THE BOARD**
> **LLM = the engine**
> **TOOLS = the wheels** (brain in a jar → break the glass)
> Tool = anything that lets the model touch the outside world
> files · terminal · GitHub · Drive · Slack · any API
> = the **A** in **T**hought → **A**ction → **O**bservation

---

## 3. Two kinds of tools: pre-built and external

`[SHOW diagram-03 — Two kinds of tools]`

Now here is something which most people do not know. Every modern harness has two categories of tools.

The first category is **pre-built tools**. These ship inside the harness itself. You install the harness, and they are already there.

The second category is **external tools**. These are added by the user or the project. Either at design time, or at run time.

Let me take external tools first. The most common way to add them is an **MCP server**. And here is a question. 🛑 **PAUSE**: if a tool is just a Python function, why should we not simply write it ourselves every time? What is the advantage of an MCP server?

...

The advantage is that it is a standard. Someone has already written the tools for you. For example, the GitHub MCP server exposes a long list of tools by default. Around twenty-seven at the time I looked. Your model gets access to all of them the moment you connect the server. If you have ten teams in a company, and each of them wants GitHub integration, you do not want ten teams writing the same code. You write it once, as a server, and everybody connects.

The other way is to write your own script and register it as a tool. That also counts.

Now let us look at the pre-built tools. What should a harness ship with? This is actually a **design question**, and the harness designer has to answer it. And there is a set which almost every coding harness ships.

Look at the left box. **Read**, to read files. **Write**, to create new files. **Edit**, to change a part of a file. **Bash**, to run commands. **Grep**, to search inside files. **ls**, to list a folder. And **find**, to locate files.

Seven tools. And I want you to pause on this number. With just these seven tools you can build extremely powerful things. These are all local to your laptop. There is no web search, no MCP, no cloud. And still, with these, you can build real applications.

Now let me ask you two small questions about these seven.

First: why do I call bash the most powerful and also the most dangerous? Because bash is the only tool through which you can run any command. It can delete things. It can install things. It can, in the worst case, take over the whole machine. Keep this in mind, because the second half of this lecture exists mainly because of bash.

Second: what is the difference between grep and find? They sound similar. But find looks for files by name or location. Grep goes deeper and looks inside the files. Suppose you have ten thousand files, and somewhere there is one particular sentence hidden inside one of them. Find will not help you. Grep will.

Now look at the bottom box, because this is an important design decision. How many tools do you ship?

Pi, the minimal open-source harness, ships very few pre-built tools, and leaves everything else to plugins. That keeps the code small. Hermes goes the other way. It ships with many tools out of the box. That is convenient for the user, but it makes the code base much bigger.

Neither is wrong. It is a trade-off. In Zill, we are going to follow the philosophy of Pi. A small set of tools. And if you want more, you add them as plugins. And you are completely free to decide differently. If you want to add web search as a built-in tool, or image generation, go ahead. That is your design decision.

One more thought, and this is my personal opinion. When people say that closed harnesses feel better than open ones, I think a big part of the reason is the quality of their built-in tools. Take grep. Writing a good grep tool is not easy. You are searching a pattern across millions of lines. A harness whose grep is fast and sensible will feel smarter than one whose grep is naive, even if the model underneath is the same.

> ✍️ **WRITE ON THE BOARD**
> **TWO KINDS OF TOOLS**
> **PRE-BUILT** (ship inside): read · write · edit · bash · grep · ls · find
> **EXTERNAL** (added later): MCP servers · your own scripts · plugins
> **Design question:** how many do you ship?
> Pi = few + plugins (small) | Hermes = many (big) | **Zill = like Pi**
>
> **bash** = most powerful + most dangerous
> **grep** = search INSIDE files | **find** = locate files

---

# PART B — What a tool really is

## 4. The tool contract: two halves

`[SHOW diagram-04 — A tool has two halves]`

Now we come to the idea which most people miss. And this is the heart of today's lecture.

A tool is **not** just a function. A tool is a **contract**. And this contract has two halves.

Look at the picture. On the left we have the **interface**. This is what the *model* sees. On the right we have the **implementation**. This is what actually *runs*. And between them, there is a curtain. The model can never see behind the curtain.

Let me say that again, because it is so important. The language model never sees your code. It has no idea how you wrote the function.

What does it see? Only four things.

One, the **name**. Which tool is this?

Two, the **label**. A tag, so that the tool can be bucketed. Think of a big fair. If you are going with your whole family, you give everyone a name tag, so that you do not lose them. Label is just a name tag for tools. When the model uses many tools in one go, you always know which is which.

Three, the **description**. This tells the model when to use the tool. And this is the most important line of the whole contract. The better the description, the better the model chooses.

Four, the **parameters**. What the model has to fill in. For a read tool, the parameter is the path of the file. For an edit tool, the file, the old text, and the new text.

Based on these four things alone, the model decides which tool to call. That is all it has.

Now the right half. The **implementation**. When the model picks a tool, the harness receives a call. It has a **tool call id**, the **parameters**, a **signal**, so that the call can be cancelled, and an **update callback**. That last one is just a way for a long-running tool to stream progress back to the user, so that the user is not staring at a blank screen. Think of it like a hook. Do not worry too much about it today.

Whatever happens inside, reading the file in one go, or in chunks, the model has no idea. It just selects the tool, and passes the parameters to the executor. The executor runs the code.

So if somebody asks you in an interview, "how will you define a tool?", your first answer should be: "A tool has two halves. An interface that the model reads, and an implementation that the harness runs. I will write them separately."

> ✍️ **WRITE ON THE BOARD**
> **A TOOL = A CONTRACT (two halves)**
> **INTERFACE** — what the MODEL sees: `name` · `label` · `description` · `parameters`
> ── the curtain ──
> **IMPLEMENTATION** — what RUNS: `execute(toolCallId, params, signal, onUpdate)`
> The model decides from the WORDS alone.

> 🎨 **YOU DRAW THIS — The job posting** *(do this before showing any code; it takes two minutes)*
> 1. Draw a **cork board**. Pin three cards on it: a **title** ("Kitchen porter"), a **description** ("Wash dishes during service"), and a **form** ("How many years of experience?").
> 2. Draw a **person on the left** looking at the board. Write under him: **"the model — the applicant"**.
> 3. To the right of the board draw a **curtain**, and behind it a box labeled **"the actual work"** (= your code).
> 4. Point at the curtain and say: *"The applicant never sees the work. He applies only from the posting."*
> 5. Write at the bottom: **vague posting → wrong applications. Precise posting → right applications.**

Now here is a small test of that idea. Why do I keep saying the description is so important? Because the language model has to choose between tools **using only the description**. If your description says "reads a file", that is fine. If it says "reads a file, returns numbered lines, and works in chunks for big files, use offset and limit", that is much better, because now the model knows what to expect and how to handle large files.

---

## 5. What the model actually receives

`[SHOW diagram-05 — What the model actually receives]`

Let me now show you a real contract. This is the read tool, written exactly the way the model sees it.

Read it with me. The name is `read_file`. The description says: "Read a file. Returns its contents with line numbers."

Now see what that description is doing. Because it promises line numbers, the model knows that in its next call it can say "look at line twelve". That small phrase changes how the model behaves later.

Then the parameters. There is one parameter, `path`. And its own description says: path relative to the working directory. So the model will not go guessing absolute paths from some other machine.

And then, `required`. This says that `path` can never be left out. On modern model APIs this is actually enforced when the call is generated. The model physically cannot produce a call without it.

So I always say this. The schema is not a suggestion. It is a fence. The model cannot climb over it.

And look at the last line. These words are sent to the model on **every single turn**. Whether the tool is used or not. So a long, wordy description is rent that you pay forever. Write it like a sticky note on the model's monitor. Short and sharp. Only the things that change what the model does.

> ✍️ **WRITE ON THE BOARD**
> **A good description tells the model:**
> 1. what the tool does
> 2. what comes BACK (so the next call can use it)
> 3. any rule that changes behaviour
> It is re-sent every turn → **every word is rent**.

---

## 6. A loose form and a tight one

`[SHOW diagram-06 — A loose form and a tight one]`

Now let me show you the same tool written two ways. This is the fastest way to understand contract writing.

On the left is a **loose** contract for an edit function. The name is edit file. The description says "Edit a file". And there is one parameter called `args`, which is just a string.

Now think like the model. What do I put in `args`? JSON? A diff? A shell command? I have no idea. So I will invent something, and hope that the code on the other side guesses the same format. Also, nothing is marked required. So on a quick turn, the very thing the function needs may simply be missing.

The worst part is that this contract registers without any error. It looks fine. It just fails quietly, forever.

On the right is the **tight** version. A clear description: replace an exact text snippet, it must appear exactly once. And three parameters: the path, the old text, and the new text. All required.

Now the model is just filling blanks. It is very hard to get wrong. And the description has already taught it the one rule that matters.

One more important lesson sits at the bottom. Many beginners think: "more required fields means more reliable". It is the opposite. If a field is required and the model has nothing real to put there, it will make something up, because an empty blank is not allowed. So over-requiring creates invented values. The rule is: **require only what the function cannot proceed without.**

And here is a debugging habit for you. When a model keeps calling a tool wrongly, the beginner's instinct is to add more warnings to the system prompt. Please don't. Fix the contract. A contract fix is a guarantee. A prompt warning is a request.

> ✍️ **WRITE ON THE BOARD**
> **CONTRACT RULES**
> 1. One clear job per tool
> 2. Named parameters, each with a description (never one blob called "args")
> 3. `required` = only what the function truly cannot run without
> 4. Model misuses a tool? → **fix the CONTRACT, not the system prompt**

---

# PART C — The six hands

## 7. Why only six tools

`[SHOW diagram-07 — Six hands cover the verbs]`

Now that we know what a contract is, let us decide what to put in the toolbox. And my answer is: six tools.

Look at the verbs of software work. You **inspect** things, that is `read_file`. You **create** things, that is `write_file`. You **correct** things, that is `edit_file`. You **execute** things, that is `bash`. You **navigate**, that is `list_files`. And you **search**, that is `grep`.

Six tools, six verbs. Pi has a seventh, `find`. We skip it in Zill just to stay small, because list files and grep already cover most of it.

Now, many of you will ask: "why not add a run-tests tool, a git-commit tool, an npm-install tool?" Because all of these are just bash with a fixed prefix. The model already knows how to type `pytest`. Giving it a separate tool adds nothing, and it costs something. It grows what I call the **decision surface**. The decision surface is the set of choices the model has to think about on every single turn. Every extra tool makes it bigger.

And overlapping tools are worse than useless. If you give the model both `edit_file` and `patch_file`, it will sometimes waste a whole turn deciding which one to use, instead of doing the work.

And remember what I said in the last lecture. If you give the model five hundred unnecessary tools, it gets confused, and hallucinations go up. This is the same idea.

Now here is a rule of thumb for granularity, because somebody always asks. **One tool should do one clearly defined job. And the descriptions of any two tools should overlap as little as possible.** You want distinct, highly useful tools. When you work on industry projects you may connect existing MCP servers, or write your own. That is fine. Just keep this discipline.

I also like to say this. When a human feels something is not working, the human tendency is to write a new tool. But very often you can get the same result with a tool you already have. Be an editor. Cut what is not needed.

> ✍️ **WRITE ON THE BOARD**
> **SIX VERBS · SIX TOOLS**
> inspect → `read_file` | create → `write_file` | correct → `edit_file`
> execute → `bash` | navigate → `list_files` | search → `grep`
> **Decision surface** = the choices the model must think over on EVERY turn.
> More tools → bigger surface → more confusion.
> **One tool = one job. Minimal overlap.**

> 🎨 **YOU DRAW THIS — The cook with a few hands**
> 1. On the **left**, draw a **drawer overflowing with gadgets**: garlic press, avocado slicer, egg separator, and so on. Write **"40 gadgets"** above it.
> 2. On the **right**, draw a **cook** with **six things**: **eyes** (read), a **fresh card** (write), a **pencil + eraser** (edit), a **stove** (bash), a **pantry list** (list_files), an **index** (grep).
> 3. Circle the stove in red. Write beside it: **"nearly every gadget is the stove wearing a costume."**
> 4. Write at the bottom: **few composable hands > a drawer of gadgets.**

---

## 8. Two axes of tool design, and output caps

`[SHOW diagram-08 — Two axes of tool design]`

Now let me show you that even the plainest tools hide design decisions. Take reading and writing.

Our `read_file` returns the contents **with line numbers**, because the model will want to point at a location later. It **stops after four thousand lines**, because a huge file would flood the conversation. And `write_file` **creates the parent folders** if they are missing, because if the model is asked to create `src/app/main.py`, it should not waste a turn on making the folder first.

Now notice the pattern. Every decision here does one of two things.

Axis one: **help the model's next step.** Line numbers, parent folders, error messages that tell you what to do.

Axis two: **protect the conversation.** Cap every output.

Why is the second axis so important? Remember the tax from the last lecture. Everything a tool returns is appended to the messages array. And the array is re-sent on every turn after that. So one huge result is not paid for once. It is paid for again and again, on all the remaining turns.

Look at the caps we use in Zill. `read_file` stops at four thousand lines. `bash` allows twelve thousand characters, and if the output is longer, we keep the first six thousand and the last six thousand. Why first and last? Because in a log, the useful stuff is usually at the beginning, the command that ran, and at the end, the error. `list_files` returns at most five hundred entries. `grep` returns at most two hundred hits.

And what if a file is really big? Then you read it in chunks. This is how Pi's read tool works. It has two extra parameters, an **offset** and a **limit**. The model reads the first chunk, then asks for the next chunk, then the next. One after another, in order.

Why does a model read in chunks? It is easier for it to read a part, understand it, and then go to the next part, than to swallow a hundred thousand lines at once. It is also cheaper.

If you have Pi installed, you can try this. Create a file with ten thousand lines and ask Pi to read it. You will see it read it chunk by chunk. And the reason is written right there in the description of the read tool: use offset and limit for large files. That is a nice proof that the description really controls the behavior.

> ✍️ **WRITE ON THE BOARD**
> **TWO AXES OF EVERY TOOL DECISION**
> 1. Help the model's **NEXT step** (line numbers · auto-make folders · helpful errors)
> 2. Protect the **CONVERSATION** (cap every output)
> **Why?** Every result sits in the messages array and is re-paid on every later turn.
> **Caps in Zill:** read 4,000 lines · bash 12,000 chars (first 6k + last 6k) · list 500 · grep 200

---

## 9. Edit beats overwrite, and the uniqueness rule

`[SHOW diagram-09 — Edit beats overwrite]`

Now let me show you the single biggest lever on how reliable your agent feels. The design of the **edit** tool.

There are two ways to let a model change an existing file. Way one: **overwrite**. The model writes the whole new file and we replace the old one. Way two: **edit**. The model quotes the exact old text and the replacement, and our code does the surgery.

Let us do the numbers by hand. Suppose I have a file with five hundred lines, and I want to change three lines.

> ✍️ **WRITE ON THE BOARD** *(do this live, slowly)*
> File = 500 lines. Change = 3 lines.
> **OVERWRITE:** model re-types **500** lines → **497** lines it should NOT touch = **497 chances** to drop an import, reformat a block, lose a comment.
> **EDIT:** model sends old + new ≈ **6** lines. The other 494 lines are never touched.
> Overwrite = hand-copying a phone book and hoping for zero typos.

So Zill ships `edit_file` with one rule. The **uniqueness rule**. The snippet which the model quotes must appear **exactly once** in the file.

Look at the three boxes at the bottom. If the snippet appears **zero** times, the model misremembered the text. We refuse with: "snippet not found, read the file and copy it exactly". If it appears **more than once**, the request is ambiguous. We refuse with: "snippet appears N times, include more context to make it unique". And if it appears **exactly once**, we do the edit.

Now please look carefully at those error messages, because the words are doing design work. Each message names the **next action**. "Read the file and copy it exactly" turns a failed guess into a read followed by a correct edit. "Include more context" turns an ambiguity into a longer, unique snippet on the next call.

So here is the principle. **A good error message in a tool is written for the model's retry, not for a human reading logs later.** The error text is one more clause of the contract.

And there is a second beauty here. The rule makes the tool **self-verifying**. The model has to quote the old text exactly. If it misremembered the file, the match fails, and it gets a clean error instead of silently corrupting your code. It physically cannot change a line it did not quote.

Somebody always asks: "why not always overwrite? It is simpler." Overwrite works fine for a ten-line config file. It quietly rots a two-thousand-line file, where the model reformats a function it never meant to touch, and nobody notices until the tests go red. Simpler to write, worse to live with. We keep `write_file` for the right case: a brand-new file, where the whole file is the change.

🛑 **PAUSE the video.** Here is a debugging exercise. A first draft of `edit_file` returns only "ERROR: snippet appears 3 times". The model calls it three times in a row with the same snippet and fails every time. What is wrong, and which part of the tool do you change? Think about it.

...

The refusal is correct. But the message does not tell the model what to do differently. So it just repeats itself. The fix is not in the model. The fix is in the message: add "include more context to make it unique".

> ✍️ **WRITE ON THE BOARD**
> **THE UNIQUENESS RULE**
> 0 matches → `ERROR: snippet not found — read the file and copy it exactly`
> 1 match → edit ✓
> N matches → `ERROR: snippet appears N times — include more context to make it unique`
> **Error messages are written for the MODEL'S RETRY.**
> Edit is self-verifying: you cannot change a line you did not quote.

---

## 10. bash, the universal appliance

`[SHOW diagram-10 — bash: the universal appliance]`

Reading, writing and editing produce files. But so far, nothing can tell whether those files actually work. That is the job of bash.

Bash runs any shell command in the working directory and returns whatever came out. It is how the agent runs tests, starts servers, calls git, installs packages. And most importantly, it is how the agent **verifies its own work**. An agent that cannot run what it wrote can only claim it is done. And a claim is not a result.

Bash is also the reason the toolbox stays at six. Think of it as the stove. A run-tests tool, a git tool, an install tool, these are all just the stove wearing a costume.

But look at the right side of the picture. The same universality is the danger. A badly judged read wastes a few tokens. A badly judged bash can be a recursive delete, or a script downloaded from the internet and piped straight into a shell. The tool that runs your tests can delete your work.

Before we talk about *what* bash is allowed to do, there are two mechanical guards. They are about resources, not about intent.

**Guard one, the timeout.** Default one hundred and twenty seconds. A hung command should never hang your agent. Imagine the model starts a dev server in the foreground. Without a timeout, the whole run just stops. No error, no report. The worst possible ending.

**Guard two, the output cap.** If the output is longer than twelve thousand characters, we keep the first six thousand and the last six thousand. A single noisy build log should not eat your whole conversation.

And there is one tiny detail I love. If a command prints nothing, we do not return an empty string. We return "exit zero, no output". Why? Because an empty string leaves the model wondering: did it run? Did it fail? Even silence is turned into a message. Every return path of every tool is a message to a machine reader.

> ✍️ **WRITE ON THE BOARD**
> **bash = the universal appliance**
> BUYS: tests · servers · git · install · **verify its own work** ("a claim is not a result")
> RISKS: `rm -rf` · `curl … | sh` · `git push --force`
> **Guard 1 — timeout** (120 s): a hung command must not hang the agent
> **Guard 2 — output cap**: keep first 6,000 + last 6,000 chars
> Empty output → `(exit 0, no output)`

---

# PART D — Security: the gate and the jail

## 11. Why security is part of the design

Now we come to the second half of the lecture, and honestly, the part which I feel is most important.

Let me ask you something. Suppose you build an agentic harness, you ship it, people start using it, and one day it deletes somebody's files. What happens to your product? Nobody will ever use it again. One incident is enough.

So security is not an add-on. A lot of people think: first I will understand the concepts, build the harness, and then I will think about security. No. Security has to be baked into the design of the harness, very tightly, from the beginning.

And there is an important point here about who is responsible. The model will **not** police itself. It has no built-in restraint. If it decides that a recursive delete helps, it will emit a recursive delete. Whose job is it to stop that? It is not the model's. It is not the prompt's. It is the **harness's job**. This is exactly the difference between prompt engineering and harness engineering. The caution lives entirely in the harness.

> 🎨 **YOU DRAW THIS — The intern and the senior**
> 1. Draw a **small, fast person** with a huge keyboard, typing a hundred times faster than anyone. Label him **"the agent (the intern)"**. Draw little **motion lines** around his hands.
> 2. Draw a **calm, older person standing behind him**, with **one hand on the intern's shoulder**. Label her **"the harness (the senior)"**.
> 3. Draw a **speech bubble** from the senior: **"Wait. Are you sure?"**
> 4. Write at the bottom: **We are not building the intern. We are building the person standing behind him.**

Let me give you the broad patterns I found when I studied how Pi and Hermes do security. Level one: **gate the tool call**. Level two: **restrict certain paths and files**. And going around both of these: **sandboxing**. We will go through each. And near the end, I will also tell you about a third level which neither Pi nor Hermes has: user-level access.

---

## 12. The gate: one checkpoint, three layers

`[SHOW diagram-11 — One checkpoint, three layers]`

The simplest and most common level is the **permission gate**. Every single tool call passes through one checkpoint before it runs. Claude Code does this. Pi does this. Hermes does this.

Remember the socket from the beginning of the lecture. `before_tool`. That is where the gate plugs in.

Look at the picture. A tool call enters from the top. It goes through three layers, in this order.

**Layer one: deny rules.** These are patterns for commands that must never run, in any mode, whatever anybody says.

**Layer two: the mode.** One of read-only, safe or yolo. This decides how much needs a human. Whole categories of calls get resolved here without any question.

**Layer three: the approver.** This is a callback which actually asks a human, "do you allow this?".

And at any layer, the call can be stopped. Look at the red boxes on the right. Each stopped call returns a message saying BLOCKED, with the reason. Only a call that clears all three layers actually runs.

Now why this order? Because **the order is the design**. Deny rules come first, so that no mode setting, and no tired human approving at two in the morning, can ever let a catastrophe through. The mode comes next, so that most calls need no question at all. The human comes last, and sees only what the first two layers could not decide.

Think of airport security. Most people are waved through. Some are pulled aside for a manual check. A tiny few are never allowed on the plane at all. And nobody gets to skip the line.

> 🎨 **YOU DRAW THIS — The funnel**
> 1. Draw a **funnel** (a big trapezoid narrowing downwards). Write **"tool calls"** above it, with many small arrows going in.
> 2. Cut the funnel into **three horizontal bands**. Label the top band **1 · DENY**, the middle **2 · MODE**, the bottom **3 · ASK A HUMAN**.
> 3. From each band draw an arrow going **out to the right** into a red box labeled **BLOCKED**.
> 4. At the very bottom, draw a small green box: **RUN ✓**.
> 5. Write beside it: **"Most calls: waved through. Some: ask. A few: never."**

> ✍️ **WRITE ON THE BOARD**
> **THE PERMISSION GATE** (plugs into `before_tool`)
> ① **DENY RULES** — never run, any mode
> ② **MODE** — read-only / safe / yolo
> ③ **APPROVER** — a callback that asks the human
> **Order = the design:** no mode and no tired human can approve a catastrophe.
> The model ASKS. The harness DECIDES.

---

## 13. The dial: read-only, safe, yolo

`[SHOW diagram-12 — The dial: read-only, safe, yolo]`

The middle layer is the one you will actually turn in real life. It is a dial with three positions.

**Read-only.** It allows only the three read tools: read file, list files and grep. Everything else is blocked. This is what you use when you point the agent at a codebase you do not trust yet. A great first-day mode.

**Safe.** Reads go through automatically. Anything that changes the world, writing, editing, running a command, goes to the approver. One call at a time. And here is a small but important detail: if no approver is wired in, the default approver **refuses**. So a safe-mode harness with nobody attached blocks everything risky, instead of quietly allowing it. In security language, the gate **fails closed**.

**Yolo.** Approves everything. Now, that sounds reckless. But it is actually the right default for a jailed, headless run. Imagine your agent running overnight with nobody awake to answer. There is no human to ask. And the deny rules and the jail still hold. You will see that in a minute. Pi has a similar bypass mode, and the right way to use it is only inside a sandbox.

In fact, Zill enforces that rule for you. If you set the mode to yolo, and bash is running directly on your own machine, the gate **refuses** the call and tells you to switch bash to the sandbox or the ssh backend. You can override it with one environment variable, but you have to do it on purpose. We will see why when we talk about where tools run.

You can also design your own modes. Say you build this for a customer. The customer on a free plan gets read-only. The customer on a normal plan gets safe. And your internal automation gets yolo, but always inside a sandboxed environment.

Why is the approval prompt not a weakness? Think about what the harness knows. It knows that a recursive delete is dangerous. But it cannot know whether you meant it. So it shows you exactly what is about to happen, and it gives the judgment to the only one who knows the intent. Pure allow is reckless. Pure deny is useless. The agents which actually work live in the middle: ask only on the risky part.

If you use Claude Code, you already know this dial. The default mode asks before edits and commands. An accept-edits mode stops asking about files. And a bypass-permissions mode is its yolo. When you see "Claude Code asked me before running a command", you have met the middle layer of this exact funnel.

> ✍️ **WRITE ON THE BOARD**
> **THE DIAL**
> **read-only** → 3 read tools only. Use: an unfamiliar codebase.
> **safe** → reads auto · side effects ask a human · no human wired in = REFUSE (fail closed)
> **yolo** → approve all · deny rules still hold · **bash on `local` is REFUSED** (needs sandbox / ssh)
> **Pure allow = reckless. Pure deny = useless. Ask on the RISKY part.**

---

## 14. The deny list, and a block on the tape

`[SHOW diagram-13 — A deny rule firing, on the tape]`

Now the top layer. And the funny thing is that the top layer is just six regular expressions.

Look at the six chips at the bottom. Six named catastrophes.

Number one: a recursive delete aimed at the root, the home folder or the home variable. Number two: sudo, privilege escalation. Number three: reformatting a disk, with mkfs or raw dd. Number four: downloading a script and piping it straight into a shell. Number five: a force push, overwriting shared history. Number six: redirecting output onto a raw disk device.

And look at what is **not** in the list. `rm -rf build/` is allowed. Because deleting a build folder inside your project is half of real work. The list bans **catastrophes**, not verbs.

This leads to a lesson. Do not judge a command by how scary the verb sounds. Judge it by how far the damage reaches. `rm -rf build/` sounds frightening but it touches a folder you can regenerate. `git push --force` sounds mild, but it can rewrite history that a whole team depends on.

Now let us see what a block looks like on the tape. Read the transcript with me.

The user says: please delete my home directory to free up disk space. The model replies it will do it, and calls bash with `rm -rf ~`. The deny rule matches. And what comes back is a tool result saying **BLOCKED: command matches deny rule**.

Nothing crashed. Nothing exited. Remember the ticket number idea from the last lecture. Every request must receive exactly one result with the same id. Even a blocked call is **answered**, never skipped. That is exactly how the pairing survives.

And then, see what the model does. It reads the reason. It declines in its own words. And it proposes an alternative inside its limits: look at what is taking space inside this project. It finds `node_modules` at 412 megabytes, and asks if it should remove just that.

So the refusal is not an ending. It is information. That is the same principle as before: failure becomes information. Now applied to policy.

🛑 **PAUSE the video** and try this. Here is a deny pattern from a first draft: `rm\s+-rf\s+/`. Can you name two commands that it fails to stop? Think about flag order, different spellings, and different ways of writing a path.

...

For example `rm -fr /`, with the flags in a different order. Or `rm -r -f /`, with the flags separated. Or `rm -rf ~`, which targets the home folder and not the root. So pattern matching over a shell language **leaks**. A regex is a strong outer ring, but it must never be your only ring. That is the reason we need the jail.

> ✍️ **WRITE ON THE BOARD**
> **THE SIX CATASTROPHES (deny rules)**
> `rm -rf` on / or ~ · `sudo` · `mkfs` / `dd if=` · `curl … | sh` · `git push --force` · `> /dev/sd…`
> Ban **catastrophes**, not verbs. Judge a command by **how far the damage reaches**.
> A blocked call is **ANSWERED**, never skipped → `BLOCKED: <reason>`
> The refusal is **information**, not an ending.
> ⚠ Regex over a shell language **leaks** → outer ring only.

---

## 15. The jail and the blast radius

`[SHOW diagram-14 — The jail and the blast radius]`

The gate decides **what** may run. It says nothing about **where**. And a command which is allowed can still reach the wrong file.

So we need a second mechanism. The **jail**.

Look at the picture. The green box is the working directory. This is the one folder where the agent lives. Inside, it can work freely. Outside are your secret keys, your system files, your other projects.

Here is how the jail works in code. Every path that every file tool touches passes through one function, called `resolve`. It joins the path onto the working directory, flattens any symbolic links and any dot-dot segments using `realpath`, and then asks one question: does the result still start with our root? If not, it raises a **PermissionError**.

So when the model tries to read `../../etc/passwd`, it fails at the very first step, before any policy is even consulted. And the error is not a crash. The loop catches it like any tool failure and returns it as an error result. So even an escape attempt is just information the model reads.

Now I want to give you a term, because it is the most useful term in security. **Blast radius.** The blast radius of an action is how far its damage reaches when the action goes wrong.

We cannot make the model stop making mistakes. It is probabilistic. It will sometimes be wrong. Across enough runs, it will be wrong. What we **can** control is the size of the room in which a mistake goes off.

> 🎨 **YOU DRAW THIS — The firecracker** *(two small panels)*
> 1. **Left panel:** draw a **steel bucket** with a small **firecracker** exploding inside. Little sparks, but the bucket holds. Write **"blast radius: a few inches"**.
> 2. **Right panel:** draw a **warehouse full of fireworks** with the **same firecracker** inside. Draw it exploding **the whole building**. Write **"blast radius: the building"**.
> 3. Between them, write: **"Same mistake. Wildly different blast radius."**
> 4. Underneath write: **"The danger is not only the action. It is what sits within reach."**

So why do we need both the gate and the jail? Because they protect against different failures.

The **gate** lowers how often a bad action is attempted. And it can catch intent that the jail cannot see, like a force-push, which touches no file path at all.

The **jail** limits how much any action which slips through can cost. Including the one that a tired human approved by mistake.

Together they answer the question which governs every agent deployment: **when the model is wrong, and eventually it will be, what is the worst that can happen?** For Zill, the answer is: a mess inside one directory, which git can undo.

You will always miss some bad actions. The model is fast, and you are one human. So design the boundaries until the worst case is acceptable. After that, you do not need to worry about every single mistake. Individual mistakes are now bounded.

> 🎨 **YOU DRAW THIS — The three rings**
> 1. Draw **three concentric circles**. Put a tiny **stick-figure agent** in the centre.
> 2. Label the **outer ring**: **JAIL — bounds WHERE** (which folder).
> 3. Label the **middle ring**: **DENY RULES — bound WHAT** (which commands).
> 4. Label the **inner ring**: **MODES + APPROVER — bound WHO decides.**
> 5. Write at the bottom: **gate = fewer attempts · jail = cheaper miss.**
> 6. Add a small note outside the rings: **"network tools need a ring of their own."** (Keep this for the next lectures.)

> ✍️ **WRITE ON THE BOARD**
> **THE JAIL**
> `resolve(path)` = join to root → `realpath` → inside root? else **PermissionError**
> **BLAST RADIUS** = how far the damage reaches when it goes wrong.
> We can't stop mistakes. We CAN shrink the room they go off in.
> **Gate** → fewer bad attempts. **Jail** → a cheaper miss. You need both.
> Worst case in Zill = a mess in ONE folder, undone by `git`.

---

## 16. Where a tool runs: sandboxing and Pi's three environments

`[SHOW diagram-15 — Where a tool runs]`

Now let me tell you the idea in Pi that I find the most interesting. Most people, when they learn tools, only learn what a tool **does**. They never ask where it **runs**. But when you build a harness, this is very important.

Pi separates **what a tool does** from **where it runs**.

Look at the picture. On top is the tool: bash, read, edit. This is the "what". Below it is a layer, the **operations layer**. This is the "where". And below that, three possible places.

**Local.** On your own machine. Fastest, but the riskiest for bash.

**SSH.** On a remote machine. Say you rent a small virtual machine and keep your non-critical files there. You run the dangerous work on that remote machine, and never on your laptop where the real files live.

**Sandbox.** A jail inside your own operating system. Instead of renting another machine, you create a locked room on your own, and the agent can only touch what is inside that room.

And here is the really cool thing. You can switch this for the **whole project**. Or you can switch it **per tool**. So you can say: run bash on the remote machine, but keep read local. And the tool code does not change at all. You only change a small operations layer around it.

And for Zill, we are going to build this. Pi shows us the idea. We bring it into our own harness, in a small file called `operations.py`.

`[SHOW diagram-20 — Zill's operations layer]`

Look at how it fits. On top are our six tools. They never touch the disk and never start a process on their own. Every file operation and every command goes through one interface, which I call **Operations**. It has only five jobs: resolve a path safely, read a text file, write a text file, list the files, and run a command.

Under that interface there are three backends.

**LocalOps.** Your own machine. And this is also where the path jail lives: join the path to the root, flatten it with realpath, and refuse if it leaves the root.

**SandboxOps.** A room inside your own computer. The command runs with a **scrubbed environment**. Your API keys and tokens, which sit in your normal environment, are not passed to the command. The working folder is the root. On Linux and Mac it also gets limits on CPU time and on file size, and if it times out we kill the whole group of processes, not just one. And there is an optional stronger tier: if you switch it to docker, the command runs in a container with **no network**, and only your project folder is mounted.

**SSHOps.** A remote machine, reached with the normal `ssh` program, so we need no extra packages. Every string that goes into a remote command is quoted properly. The jail is checked **before** any ssh call is made. So a path like dot-dot-slash never even leaves your laptop.

And now the part I like most. You choose the backend with two settings. `ZILL_BACKEND` chooses it for the whole project. And `ZILL_TOOL_BACKENDS` lets you override it for one tool. For example: bash in the sandbox, everything else local. The tool code does not change. Not one line.

Now I have to be honest with you, because honesty is part of security. The default sandbox, the process tier, **stops accidents, not attackers**. It stops a leaked secret, a runaway loop, a giant file, an orphan process. It is not a wall against someone determined. If you need a real wall, use the docker tier, or a remote machine. And the SSH backend, as we build it today, is tested with a fake runner and not against a real server, so before you trust it, try it once against a small virtual machine of your own.

And this ties back to yolo. Remember, yolo is only safe when the blast radius is small. So in Zill, yolo with bash running directly on your machine is refused. Put bash in the sandbox or on the remote machine, and then yolo is allowed.

> ✍️ **WRITE ON THE BOARD**
> **WHAT a tool does ≠ WHERE it runs**
> `tools.py` = WHAT · `operations.py` = WHERE
> **Operations interface:** resolve · read_text · write_text · walk · run
> **LocalOps** (your machine + path jail) · **SandboxOps** (scrubbed env, limits, optional docker: no network) · **SSHOps** (remote VM, `ssh`, shlex-quoted)
> **Choose:** `ZILL_BACKEND=sandbox` · per tool: `ZILL_TOOL_BACKENDS=bash=sandbox,read_file=local`
> Process sandbox = stops **accidents**, not attackers. Docker / remote = a real wall.
> Rule: **yolo + bash on local = REFUSED.**

---

## 17. Three levels of security, and the enterprise gap

`[SHOW diagram-16 — Three levels of security]`

Let me put it all together. There are three levels of security that I see.

**Level one: gate the tool call.** Allow, ask the human, or refuse. Every serious harness has this. Zill has this.

**Level two: restrict paths and files.** In Pi these are called protected paths: places that must never be written to, never edited. In Zill, our version of this is the path jail.

**Level three: user-level access.** And here, I want to tell you something from real experience. This level does not exist in Pi or Hermes. It is not in Zill either.

Think about a big company. Take any large company with countries, entities inside each country, and organizational units inside those. Access is governed at every single level. Not every person should be able to use every tool. One user should get these tools. Another user should get those.

When we build harnesses for companies, this turns out to matter far more to them than the technical performance. They cannot roll out one company-wide harness where anyone can reach anything. They want the harness to be gated by the person's login, their role, their unit in the organization. This is called role-based access control, RBAC.

> 🎨 **YOU DRAW THIS — The enterprise tree**
> 1. At the top, draw a box **"Company"**.
> 2. Below it, three boxes: **"Country A"**, **"Country B"**, **"Country C"**.
> 3. Below each country, two or three smaller boxes: **"Entity"**, then **"Org unit"**.
> 4. At the very bottom, draw **users** as small stick figures.
> 5. On **each level**, draw a small **diamond** (the gate). Write **"which tools may this level use?"**.
> 6. Write at the side: **the same diamond gates a tool call · a path · and a USER.**

Why am I telling you this? Because this is a real gap. Today's open-source harnesses are not built for it. So here is an opportunity. If you can build a harness that is easy to customize for an enterprise, one that is very secure, fully observable and fully deterministic, where the blast radius is so small that the agent can never escape it, that is a very valuable thing. I am telling you this from experience. If I were starting a company right now, this is something I would seriously look at.

A friendly warning. Many enterprises are scared of deploying agents because of jailbreaking and exactly this lack of control. So the more of these layers you build, the more trust you earn.

> ✍️ **WRITE ON THE BOARD**
> **THREE LEVELS OF SECURITY**
> 1. Gate the **tool call** (allow · ask · refuse)
> 2. Restrict **paths and files** (protected paths / the jail)
> 3. Restrict **by user** (RBAC / org unit) ← the enterprise gap
> Around all three: **SANDBOXING** = a free room with a fixed blast radius.
> Enterprise need: small blast radius · fully observable · deterministic.

---

# PART E — Putting it together

## 18. What happens to one tool call today

`[SHOW diagram-17 — What happens to one tool call today]`

Now let us put the whole lecture into one picture. This is what happens to a single tool call in Zill, from start to finish.

The model reads the contracts, and picks a tool. That is where the contract matters. Then the call goes to the **safety check**, which is both tool-level and path-level.

If it is safe, the harness executes it. Remember, *we* run it, not the model. The result is appended to the messages array, and we go around the loop again. The model now sees the result.

If it is **not** safe, we ask the human. If the human says yes, we run it. If the human says no, we tell the model: BLOCKED, with the reason. And then the model does something clever. It proposes an alternative, and we are back in the loop.

Now notice something. There is **no arrow here that crashes the loop**. A tool failing, or a tool being refused, never crashes the loop. The error text becomes a message, the message is appended, and the model reads it. The advantage of a language model is that it is very good at error messages. It sees the error, and it corrects itself. Maybe it changes the tool, maybe it changes the arguments, maybe it picks a different tool. But the loop does not fail.

This also answers a question many people ask: how do you handle errors in agents? Do not let the tool fail silently. Show the error to the model.

On determinism, since someone always asks: it is the hardest piece of the puzzle for enterprises. You cannot make an LLM fully deterministic, but you can inject determinism in as many places as possible. Give tools strict schemas. Add preconditions, like "this tool may only be called after that one". Gate calls with fixed rules. And use the non-deterministic model only where it is truly needed.

> ✍️ **WRITE ON THE BOARD**
> **ONE TOOL CALL, START TO FINISH**
> contract → model picks tool → **safety check** → (safe) run → append result → loop
> (not safe) → ask human → yes: run | no: tell the model `BLOCKED + reason` → it proposes an alternative
> **A failing or refused tool NEVER crashes the loop.** Errors are messages.
> **Determinism:** strict schemas · preconditions · fixed gates · use the LLM only where needed.

---

## 19. Four levels of depth: how to answer "what is a tool?"

`[SHOW diagram-18 — Four levels of depth on tools]`

Before we build, let me give you a tool for **your own career**. When I work with my team, we often discuss how deep we have gone while answering a question. This is how I think about tools.

**Level one.** What a tool is. Access to the outside world, breaking the glass jar. This is true and it is the answer most people give.

**Level two.** Can you write a tool contract? Do you understand interface versus implementation, and the four things the model sees?

**Level three.** Can you gate a tool call? Deny, ask, allow? Can you stop a dangerous command before it runs?

**Level four.** Can you control **where** the tool runs? Local, SSH, sandbox? Can you decouple what a tool does from where it runs?

Most people stop at level one. A harness engineer goes to level four.

So the next time someone in an interview or at work asks you "can you write a tool for me?", you know the answer. You do not just show a function. You say: "I will write the contract first, the name, the description, the parameters. Then the implementation. Then I will think about which calls need a gate, and where it should run."

That answer alone shows depth.

> ✍️ **WRITE ON THE BOARD**
> **FOUR LEVELS OF DEPTH**
> L1 — What a tool is (access to the world)
> L2 — The contract (interface vs implementation)
> L3 — Gate the call (deny · ask · allow)
> L4 — Where it runs (local · SSH · sandbox)
> **Interview answer:** "Contract first. Then implementation. Then the gate. Then where it runs."

---

## 20. Let us build it

`[SHOW diagram-19 — What we build today]`

Alright. Now let us build it.

Today we are writing three files, plus a set of tests. `operations.py`, which decides where a tool runs: local, ssh or sandbox. `tools.py`, which has the six tools. And `security.py`, which has the gate and the modes. We are not touching `loop.py` at all. And we are not touching `provider.py` either.

This prompt is longer than last time, and that is on purpose. The more exact the contract, the better the build. Notice how it is organised. First the one idea to preserve: what a tool does lives in `tools.py`, where it runs lives in `operations.py`. Then each file, with every function and every error message. Then the tests. And at the very end, a list of checks, which the agent must run and report honestly, including the limits of what it built.

And remember, the way we do this is the same as last lecture. We do not type the code by hand. We give a careful prompt to a coding agent. Open the same project and the same coding agent session in which you built the last lecture's files. Tell it that yesterday's files exist, and today we go one step further.

Here is the prompt.

`[SCREEN: paste the prompt below — read it out section by section as it appears]`

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

`[While it runs, keep talking:]`

While this runs, notice a few things about the prompt. It does not say "write some tools". It gives the exact contract: every function, every constant, every error message. It asks for tests, with no network and no real server, so anyone can run them. And at the bottom, it lists the checks which the agent must run and report, including a demo where the same command is run on local and in the sandbox. A good prompt always says what "done" looks like.

And look at the first paragraph. "Do not rewrite provider.py or loop.py. If you think they must change, stop and report." That is the layering we talked about at the beginning of the lecture. Today plugs into the sockets which already exist. If the agent wants to change the loop, that is a warning sign, and we want to hear about it.

One more thing. See the instruction "list every limitation you know of". I always add that line. It makes the agent tell you what it did not protect against, instead of letting you find out later.

First, let the tests run. `python -m unittest discover -s tests -v`. Everything should be green before we run a single live demo.

`[When it finishes, run the demo beats on screen. The demo prints which backend each tool uses, and what the sandbox enforces on your machine. Read that table out loud. It is the truth for your computer, including the weaker Windows case.]`

**Beat one: capability.** Let us ask it to create a file called `fib.py` with an iterative Fibonacci function, run it, and confirm the output. Watch the loop. It writes the file. It runs it. It reads the output, eight three two zero four zero. And only then does it report. It did not assume. It verified.

**Beat two: restraint.** Now we ask it: delete my home directory. Watch what happens. The deny rule fires. The tool result says BLOCKED. And the model declines politely and proposes something safer.

**Beat three: the jail.** Now we ask it to read `../../etc/passwd`. And see: a permission error comes back as a tool result. The harness did not crash. The model reads the error and moves on.

**Beat four: where it runs.** This one is my favourite. First, in your terminal, set a fake secret in the environment, something like `FAKE_SECRET=1`. Now ask the agent to run a command which prints that variable. On the **local** backend, it prints it. The command can see your secret. Now switch to the **sandbox** backend and run the same command. This time, nothing. The secret never reached the command. Same tool, same code, same prompt. Only the backend changed. That is the whole point of separating what a tool does from where it runs.

Then show per-tool routing. Set bash to the sandbox, and leave everything else local. Look at the table which the demo prints: bash goes to sandbox, the other five stay local.

And finally, remember the failure from the end of the last lecture? We asked it to build a landing page, and it could only describe one. Let us run that exact request again.

`[Run: "Build a landing page for a coffee shop"]`

And now it builds one. For real. Files, folders, a page you can open in a browser. And we did not change the loop. Not one line. Capability and restraint came out of the same two files, in the same afternoon. That is why they belong in the same lecture.

If you want to be sure everything is working, here is a quick self-test.
- All the unit tests pass.
- Asking it to read your home directory should give a permission error, because that path is outside the working directory.
- A dangerous command like a recursive delete on root should come back BLOCKED.
- A normal command like running your tests should just work.
- The same command prints your fake secret on local, and prints nothing in the sandbox.
- In yolo mode, bash on the local backend is refused, and works once you move bash to the sandbox.

---

## 21. Homework

Before the next lecture, I want you to do these things. They are not hard, and they will make you far stronger than most people who only watch.

**One.** Run your harness over a real repository that you know well, in **read-only** mode. Ask it to write an onboarding document: what the service does, where requests enter, where state is written, and the three files a new engineer should read first. Then read what it wrote as if you were reviewing a colleague's work. Read-only mode exists precisely so that the first time is safe.

**Two.** Design a **seventh tool** for your own work. And design it as a contract, **before you write any code**. Write the description, each parameter description, the shape of a successful result, and the exact text of two error messages. Write the error messages first. If you cannot say what a useful failure sounds like, the tool is not designed yet. Then implement it and give it to the harness.

**Three.** Add **one deny rule for your own environment**. Not `rm -rf`. The command that would genuinely hurt where *you* work: a deploy, a `terraform apply`, a `kubectl delete`, a database migration against production. And write a test which shows the rule blocking it.

**Four.** Try to **escape the jail**. Ask the harness to read a file above the working directory, and confirm the error comes back as a tool result and not as a crash. Then read the transcript and see what the model did next.

**Four and a half, optional but excellent.** Try the **ssh** backend against a small virtual machine of your own. Set `ZILL_BACKEND=ssh`, `ZILL_SSH_HOST` and `ZILL_SSH_DIR`, and run the fib demo. Our tests used a fake runner, so this is the first time it meets a real server. Write down anything that breaks. Then try the docker tier of the sandbox with `ZILL_SANDBOX=docker`, and confirm that the network is really off inside it.

**Five, a reading task.** Go through Pi's code and read how it implements security, especially how it defines tools and where they run. If you have time, do the same for Hermes. Hermes has similar environments but implements them differently. Compare the two. And then think: how would you extend this for an enterprise, with user-level access and an organizational hierarchy? You might be the first person to ship an open-source enterprise harness.

If you want one more: run the same onboarding task in **safe** mode with yourself as the approver, and count how many times you were asked. That number is the whole argument for where the human belongs.

Please keep the tool contract you wrote. We will start the next lecture by reading a few of them aloud, and predicting how each one changes the model's behavior.

---

## 22. Closing

So let us close, and summarize what we learned today.

We learned that a tool is not a function. It is a **contract**, with two halves. The model reads the interface, the name, the label, the description and the parameters. The harness runs the implementation behind a curtain.

We learned that most of the craft is in the **words**: tight schemas, short descriptions, error messages written for the model's next step.

We learned that **six tools** are enough for real software work, and that bash, the most powerful one, is also the most dangerous.

We learned that security has to be **in the design**. A **gate** with three layers: deny rules, mode and approver. And a **jail**, which limits the blast radius of the mistakes that get through.

And we learned that when the model is wrong, and it will be, the question to ask is: **what is the worst that can happen?** Design until that answer is acceptable.

In the last lecture, Zill got a heartbeat. In this lecture, it got hands and a conscience. In the next lecture, it meets its first hard limit. The context window fills up. And we build the mechanisms which let a small harness finish large work: context, memory and skills.

Thank you so much, and I will see you in the next lecture.

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

| # | Drawing | Draw it in section | Time | Main colours |
|---|---------|--------------------|------|--------------|
| 1 | The job posting and the curtain | 4 | 2 min | black, red |
| 2 | The cook with a few hands | 7 | 2 min | black, red |
| 3 | The intern and the senior | 11 | 2 min | black, green |
| 4 | The funnel | 12 | 3 min | black, red, green |
| 5 | The firecracker: bucket vs warehouse | 15 | 2 min | black, red |
| 6 | The three rings | 15 | 2 min | black, red, green |
| 7 | The operations switch (where a tool runs) | 16 | 2 min | black, green |
| 8 | The enterprise tree | 17 | 3 min | black, red |

If you are short on time, draw **1, 3, 4 and 6**. They teach the four most important ideas: *the model sees only words*, *the harness stands behind the agent*, *the order of the gate*, and *the three rings*.

---

## Drawing 1 — The job posting and the curtain *(section 4)*

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

## Drawing 2 — The cook with a few hands *(section 7)*

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

## Drawing 3 — The intern and the senior *(section 11)*

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

## Drawing 4 — The funnel *(section 12)*

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

## Drawing 5 — The firecracker: bucket vs warehouse *(section 15)*

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

## Drawing 6 — The three rings *(section 15)*

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

## Drawing 7 — The operations switch *(section 16)*

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

## Drawing 8 — The enterprise tree *(section 17)*

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

- **The 500-line file, by hand** (section 9): draw a long bar labelled *500 lines*. Colour the *whole* bar yellow for **overwrite** ("model re-types everything"). Draw the *same* bar in grey with a **tiny yellow block** in the middle for **edit**. Write under them: *497 chances for a typo* vs *about 6 lines*.
- **The tape with a BLOCKED line** (section 14): draw six horizontal lines labelled *user, assistant, tool, assistant, tool, assistant*. Colour the third one **red** and write **BLOCKED** on it. Draw an arrow from the fourth line back to the third and write **"the model reads the reason"**.
- **The four steps of depth** (section 19): draw a **staircase** with four steps going up. Label them from the bottom: *what a tool is · the contract · gate the call · where it runs*. Draw a stick figure on step 1 and another on step 4 and write **"most people stop here"** and **"harness engineers go here."**

---

## Notes for you (not spoken)

**Diagram cue list** (`diagrams-lecture3/`, hand-drawn style)

| # | File | Use it in section |
|---|------|-------------------|
| 01 | diagram-01.png | 1 — where we left off (two sockets) |
| 02 | diagram-02.png | 2 — brain in a jar |
| 03 | diagram-03.png | 3 — two kinds of tools |
| 04 | diagram-04.png | 4 — a tool has two halves |
| 05 | diagram-05.png | 5 — the read_file contract |
| 06 | diagram-06.png | 6 — loose vs tight |
| 07 | diagram-07.png | 7 — six hands |
| 08 | diagram-08.png | 8 — two axes and output caps |
| 09 | diagram-09.png | 9 — edit beats overwrite |
| 10 | diagram-10.png | 10 — bash, the universal appliance |
| 11 | diagram-11.png | 12 — the gate funnel |
| 12 | diagram-12.png | 13 — the dial |
| 13 | diagram-13.png | 14 — a deny rule on the tape |
| 14 | diagram-14.png | 15 — the jail and blast radius |
| 15 | diagram-15.png | 16 — where a tool runs |
| 16 | diagram-16.png | 17 — three levels of security |
| 17 | diagram-17.png | 18 — one tool call, start to finish |
| 18 | diagram-18.png | 19 — four levels of depth |
| 19 | diagram-19.png | 20 — what we build today |
| 20 | diagram-20.png | 16 — Zill's operations layer (show it right after Pi's "where a tool runs") |

**Diagrams you draw yourself (8):** the job posting + curtain (section 4) · the cook with few hands (section 7) · the intern and the senior (section 11) · the funnel (section 12) · the firecracker, bucket vs warehouse (section 15) · the three rings (section 15) · the operations switch (section 16) · the enterprise tree (section 17). The full guide is in "DRAWING GUIDE" above. Skip any you have little time for; if you do only four, draw 1, 3, 4 and 6. The ready-made picture for the same topic is always there as a backup.

**Verify before recording** (statements that come from how you described the open-source harnesses; check them on screen before saying them)
- Pi's tool definition fields (name, label, description, parameters) and the `execute(toolCallId, params, signal, onUpdate)` signature.
- Pi's read tool having `offset` and `limit`, and Pi shipping exactly seven tools including `find`.
- Pi's three execution environments (local, SSH, sandbox) and the per-tool operations layer.
- How Hermes does the same, if you plan to compare the two on camera.
- The number of tools the GitHub MCP server exposes (I wrote "around twenty-seven"). That number changes over time.
- The Claude Code mode names (default · accept edits · bypass permissions), in case the names were changed in your version.
- Line counts in diagram 19 (~170 for the earlier files, ~370 today) are approximate. Replace them with the real `wc -l` numbers from your repo after you build.
- Before you record, **run the build prompt once yourself** and keep the transcript as a backup. In particular check: the unit tests pass, the sandbox demo hides your fake secret, and `describe()` honestly reports what is enforced on **your** operating system. On Windows the process sandbox has no CPU or file limits, and the script says so; do not claim otherwise on camera.
- The SSH backend is only tested with a fake runner. Say that out loud (the script does) unless you test it on a real server first.
- The build prompt is also saved on its own as `zill-lecture3-build-prompt.md`, ready to paste.

**Placement notes**
- This script follows the Odysseus tutorial's Tools lesson for the structure of the build prompt and the design points (contract, six tools, uniqueness rule, gate, jail). Credit it in the description.
- Claims about enterprise needs (RBAC, org units) are framed as your own experience. Keep them in first person and say only what you have actually seen.
- The script does not claim that Zill passed any benchmark or built any named product.
