# Lecture 6 — Harness, Fleet and Client (the last lecture)

Read this out exactly as written. The only extra things are small cues in square brackets:

- [PICTURE 12] = put picture 12 on screen (folder `diagrams-lecture6/`).
- [ASK, wait 3 sec] = ask the viewers this question, wait 3 seconds, then keep reading. The answer is the next lines.
- [PAUSE] = take a breath, a new topic starts.
- [DO: ...] = something you type or run on screen.

# PART 1 — One class: harness.py

[PICTURE 01]

Hey everyone, welcome back to the Harness Engineering series. This is lecture number six, and it's the last one.

Before we start, open your Zill folder. You should have ten files. provider.py and loop.py from lecture two. tools.py, security.py and operations.py from lecture three. context.py from lecture four. And memory.py, skills.py, session.py and subagent.py from last time.

If you have those ten, you're ready. If something's missing, go back and finish lecture five first, because today we build right on top of it.

Now look at the picture. Ten green files, and every one of them works on its own. We tested each one. But here's the thing. None of them knows the others exist. There's no single object you can point at and say, "that is the agent."

So today three more files join the repo. harness.py, which ties everything together. fleet.py, which runs many agents at once. And client.py, which is the front door, so a person, or a script, can actually start Zill.

And I'll be honest with you. Today is plumbing. None of these files teaches a new hard idea. The hard ideas were the first five lectures. But this is the part that turns a pile of working files into a tool you'd actually use. So let's do it properly.

[PICTURE 02]

Here's the plan. Three stops.

First, harness.py. Where do the ten files meet?

Second, fleet.py. How do we run twenty-five projects at once?

And third, client.py. How does a person, a script, or a website start the agent?

After that, we build all three into Zill, and we run it on real projects. Zill will be finished.

[PAUSE]

[PICTURE 03]

Let's start with harness.py. And I want to start with a picture, because the whole file is basically this.

Ten files, five on each side. And in the middle, one class. We call it Harness.

Look at the lines. Each file plugs into the harness at one place. The provider and the loop. The tools and the permission gate. The compaction, the memory, the skills, the sessions, the helpers.

And now look at the note under the middle box. No cleverness of its own. I want you to remember that sentence. The Harness class decides nothing. It doesn't have a state machine. It doesn't have special rules. All it does is take each file we already wrote and plug it into the socket that file was built for.

That's why this lecture is short, and that's also why it's a good sign. If your assembly class is complicated, it usually means two of your layers have grown into each other, and you can't swap one without breaking the other.

[PICTURE 04]

Now, one word I want to be careful with. Object.

When I say "create a harness," what I really mean is this. You create an instance of the Harness class.

Look at the picture. On the left, a harness for a shop website. On the right, a harness for a snake game. Each one has its own model, its own tools, its own permission gate, its own system prompt, its own messages list, and its own session file.

And in the middle, in red. They share nothing.

That sounds like a small detail, but it changes how you think. A harness isn't a script that runs once and disappears. It's a thing that holds a whole conversation inside it. Make two, and you have two agents that don't know about each other. And that's going to matter a lot when we get to the fleet.

[ASK, wait 3 sec] How many of you are comfortable with the words class and instance? If it feels fuzzy, don't worry. Just remember this. The class is the recipe. A harness is one thing you cooked from it.

[PICTURE 05]

Now let's look inside. This is the constructor, the part that runs when you create a harness, shown in a shortened form.

Read it from top to bottom, and read the tags on the right as well.

First, it builds the tools. That's core_tools from lecture three. Then the policy, the permission gate, also from lecture three.

Then it adds the remember tool, the use_skill tool, and the spawn_agent tool. Those three come from lecture five.

Then there's the line in red. Every tool gets wrapped in a gate. What that means is, before any tool runs, the policy gets to look at the call. If it says no, the tool doesn't run, and the model just gets a message back saying it was blocked. So there's no way to call a tool and skip the gate. It's built into how the tools are made.

Then it builds the system prompt, with your ZILL.md memory and the skills list. And finally, run hands everything to the loop.

Look at this whole picture once more. It's the whole series, in eight lines. That's what I mean when I say the class is the series, assembled.

[PICTURE 06]

Now, what does run do?

Five small steps. You can follow them left to right.

One, add the task to the messages list. Two, write it to the session file, so it's on disk before anything else happens. Three, compact if the conversation is over budget. Four, ask the model. Five, for every tool the model asks for, pass it through the gate, then run it.

And then there's the arrow that loops back. Steps three to five repeat, every lap, until the model answers in plain text with no tool calls. That plain text is what run returns.

Notice there's no separate place where "progress" is stored. The messages list is the state. That's also why resuming a crashed session in lecture five was so easy. There was never anything else to save.

[PAUSE]

[PICTURE 07]

Now here's something I find really interesting. And it's the reason I wanted to spend a minute on harness.py at all.

Every harness has a loop, tools, a gate and compaction. Those are the same everywhere. But where you put the budget check is a decision, and different harnesses make it differently.

At the top, Hermes and Codex. They check the context budget once, before the loop is called. Compact if needed, and then run.

At the bottom, Pi, and Zill. They check at the top of every lap. And since the top of a lap comes right after the tools from the previous lap finished, that means the check runs right after the tool results come in.

Why does that matter? Because tool results are what blow up the window. One big file, one long test log, and your messages list jumps in size. If you only checked once at the start, a long task can quietly grow past the window halfway through, and nothing is watching.

So Zill follows Pi. The check lives in the before_turn hook, which runs at the top of every lap.

[ASK, wait 3 sec] Here's a question for you. If both harnesses have exactly the same files, why do they behave differently on a long task?

It's because of how the files are assembled. The files are the same. The wiring is different. That's a design decision, and harness.py is where you make it. Building every part correctly is not the same thing as building the harness.

[PICTURE 08]

And because the core is this modular, adding new things is easy. Look at where each one goes.

Want tracing, so you can see every model call and tool call? Edit harness.py, and send each event to a log file or to OpenTelemetry.

Want short-term memory? That belongs next to the long-term memory, so you edit memory.py.

Want an evaluator, something that scores a finished run? That's a brand new file, evaluator.py. The harness doesn't even need to know it exists.

And a new tool? Write it with the tool decorator, and pass it in extra_tools. It'll go through the same gate as every other tool.

So most features touch one place. That's what modular means. You extend it without rewriting it. Keep that in mind for after the series ends, because that's where you'll take Zill next.

[PAUSE]

# PART 2 — Many harnesses: fleet.py

[PICTURE 09]

Alright, on to the second file. Fleet.

Here's the situation. You've built a harness. And now you don't want one project. You want twenty-five.

Remember, a harness is an object. So the answer is almost too simple. If you want twenty-five projects, make twenty-five harnesses, each in its own folder.

Look at the picture. On the left, a list of jobs. A job is just three things. A name, a folder, and a task. In the middle, four workers. Each worker takes a job, creates a fresh harness inside that job's folder, and runs it. And on the right, the results. Same order as the jobs, with the failures marked.

I like to think of it as a job board. Imagine a wall of cards in a small factory, and four workers. Each one takes a card, walks into their own room, does the job alone, and pins the outcome back on the board. A failure comes back as a red note, it doesn't stop the shift.

And notice what the board never does. It never tells a worker how to do the job. The board only decides who works on what, and when. All the judgment stays inside each room, inside each harness. That's a really useful split. Plain code on the outside, judgment on the inside.

[PICTURE 10]

And here's the whole file. About thirty lines.

The top function, run_fleet, uses a thread pool. That's something Python already has built in, so we install nothing. It starts a few workers, hands them the jobs, and collects what comes back.

The bottom function, run_one, runs a single job.

Three details carry the whole design. I numbered them.

Number one. Each job gets its own folder. And remember from lecture three, the folder is also the jail. The file tools can't go outside it. So one project can't touch another project's files.

Number two. Look at the try and except at the bottom. If a job crashes, we don't let that error escape. We turn it into a result, with ok set to False. Why does that matter more here than in a single run? Imagine job number three out of twenty-five crashes at two in the morning. If that error escaped, the whole batch could stop, and the other twenty-two jobs never run. This way, you wake up to a list with a few failures in it, and not to nothing.

Number three. The sort at the end. The workers finish in whatever order they finish in, so we sort the results back into the order of the jobs. That's it.

And look at the box at the bottom. Nothing clever. That's the lesson. Orchestration, the thing with the most marketing around it, turns out to be a thread pool.

[PICTURE 11]

Now you might be wondering. We already have sub-agents from last time. Why do we need a fleet?

Look at the three columns. They all run more than one piece of work. What's different is what they share.

A sub-agent, on the left. One parent splits up its own task, and hands a piece to a child. The child works with a clean context, and reports back to the parent. It's all one job. They share the parent's goal.

A fleet, in the middle. Many unrelated projects. Each has its own harness, folder, context, memory and session. Nobody reports to anybody. They share nothing.

And on the right, a third option people often ask about. One harness, serving many users, with a session ID for each. That can work. But now everything shares one memory and one context. And a coffee website and a snake game really shouldn't share a memory. Why would a snake game need to know about coffee prices?

So here's the rule I use. Sub-agents when it's one job split into pieces. A fleet when they're many separate projects.

[PICTURE 12]

One more question, and it's a good one. Why do we limit the number of workers at all? Why not just start all twenty-five at once?

[ASK, wait 3 sec] What do you think the limit is about? CPU?

It isn't. Think about what an agent actually does most of the time. It waits. It sends a request to the model, and waits for the reply. That's a program sitting idle, waiting on the network. So your laptop can hold a lot of them without any trouble.

The real ceiling is on the other side. The provider. Requests per minute. Tokens per minute. And of course, your bill.

Look at the left. Twenty-five jobs at once. They all hit the API together, they all get a rate limit error together, and they all back off together, and then they all retry together, at the same moment. That's a mess.

On the right, four at a time. The API stays comfortably under its limit.

So max_workers is a rate limiter. It's not a CPU setting. That's why the default is four.

[PAUSE]

# PART 3 — The front door: client.py

[PICTURE 13]

On to the last file. Client.

Everything so far is a class. And a class is something code can use. But a tool is something a person can run. So client.py closes that gap.

And it works the same way Claude Code does. Have you tried running Claude Code with a dash p? It runs without a screen. You give it a task, it does it, prints the result, and exits. That's called headless mode.

Zill gets the same two modes. On the left, interactive. You type python dash m zill. You get a prompt, you chat, and it stops to ask you before it changes anything. On the right, headless. You type python dash m zill dash p, and your task in quotes. It takes the task, runs it, and exits.

And behind both doors is exactly the same Harness. Only the default mode changes.

[PICTURE 14]

Let me show you why the default changes. It's one question. Was dash p given?

If not, a human is sitting there. So the mode is safe, and the approver is a function that asks you, "approve write file, yes or no?"

If dash p was given, nobody is here. So the mode becomes yolo, and the approver is nothing. Why? Because if Zill stopped to ask a question, and nobody was there to answer, it would wait forever. Imagine twenty-five jobs, all waiting for a person who's asleep.

But, you remember from lecture three, our policy won't allow yolo together with bash on your own machine. So when you go headless, the client also switches the backend to the sandbox. That's the arrow at the bottom. Yolo is only allowed because the commands run in a box.

And look at this. That input call, the one that says "approve, y or n," is the entire human-in-the-loop story of Zill. One line. Everything else about supervision is the policy we wrote in lecture three.

Now there's something that confuses people, so let me say it clearly. Headless is not the same thing as auto-approve. Both skip the question. But with auto-approve, you're at your own machine, you chose not to be asked, and you can still watch and hit Ctrl+C. With headless, nobody is watching at all. A job on a remote server. A step in your build pipeline. A fleet running overnight. That's why in headless mode the jail and the deny rules have to be tight. They're the only supervision left.

[PICTURE 15]

One last thing before we build. And this is a question I get a lot.

Say you've built a website, and when a user asks something, you don't want one API call. You want a whole agent to run. What do you do? Claude Code on your laptop can't help, because the website isn't on your laptop.

Look at the three options.

One. Run Claude Code with dash p on a server. Every request starts a fresh process, and sends back the output. It works, and it's the tested product. But you're running a whole command line tool for every single request, and that's usually the most expensive way.

Two. Use the Claude Agent SDK. That gives you the same loop and tools as Claude Code, as a library you can call from your own server code. A better fit than starting a process per request.

Three. Use your own harness. And this is where building Zill pays off. Zill is already a class. So it's already an SDK. Look at the little snippet. A function that takes a question, creates a harness in a fresh folder, and runs it. We made it read-only, so the agent can look around but can't change anything, and persist set to false, so it doesn't write session files for every web request.

And that's why we built Zill as a class and not as a script. The command line, the fleet and a web server are three different doors on one object.

[PAUSE]

# PART 4 — Build it into Zill

[PICTURE 16]

Alright. Let's build it. We're adding four small files, and then we'll test them.

The first is harness.py, the Harness class we just walked through. The second is fleet.py, about thirty lines. The third is client.py, the front door. And the fourth is a tiny file called __main__.py, which is what makes python dash m zill work.

On top of that, there are tests that use a fake model, and a couple of demos.

One thing I want to flag before you paste the prompt. We're being strict about one rule that came from lecture five. When the harness creates a helper, it creates it with persist set to false. If we forget that, the helpers write their own session files, and the next time you resume, you wake up inside a helper's job. That's the bug from last time, and the build prompt has it written in.

Okay. Open up Claude Code inside your Zill folder, and paste in this prompt.

[DO: paste the prompt below into Claude Code. It's also saved as `zill-lecture6-build-prompt.md`.]

```
You are building the last part of Zill (lecture 6 of the series): the class
that wires everything together, a fleet runner, and a command-line front door.
The parts are cumulative. Your repo already contains the package zill/ with
provider.py, loop.py (run_loop(model, system, messages, tools, on_event,
max_turns=80, before_turn=None)), tools.py (Tool, the @tool decorator,
core_tools(workdir, ops)), operations.py (ops_from_env), security.py (Policy),
context.py (compact), memory.py, skills.py, session.py and subagent.py, plus
demos/ and tests/ from lectures 2 to 5.

Today adds FOUR new files: zill/harness.py, zill/fleet.py, zill/client.py and
zill/__main__.py. No existing file changes. Build exactly what this spec
describes and nothing else.

GROUND RULES
- Python 3.10+, standard library only. Must run on Windows, macOS and Linux.
- Same code standard as before: a module docstring on every file naming the
  concept it teaches and the design rules it embodies; a docstring on every
  public function; a short comment wherever behaviour is subtle.
- Size targets including documentation, within about 15%: harness.py 70
  lines, fleet.py 30, client.py 75, __main__.py 5.
- Commit after each file. Do not add features beyond this spec.
- Read loop.py, tools.py, security.py, context.py, session.py and subagent.py
  before you start and match their names and message shapes exactly. If
  anything below contradicts the code, stop and report it instead of guessing.

THE THREE IDEAS TO PRESERVE
1. A harness is an object. Creating a harness means creating an instance of
   the Harness class. It holds its own model, tools, gate, system prompt,
   messages list and session file. Two harnesses share nothing.
2. The class decides nothing. Construction plugs each existing file into the
   socket it already has. The messages list is the only state.
3. Orchestration is plain code. A fleet is a thread pool of independent
   harnesses; the worker limit protects the API, not the CPU.

------------------------------------------------------------------------------
1) zill/harness.py
------------------------------------------------------------------------------
class Harness(workdir=".", model=None, policy=None, extra_tools=(),
on_event=None, budget_tokens=600_000, max_turns=80, enable_subagents=True,
persist=True, depth=0)

Construction, in this order:
- workdir = realpath, created if missing. model defaults to the ZILL_MODEL
  environment variable, then provider.DEFAULT_MODEL. on_event defaults to a
  function that does nothing.
- tools = core_tools(workdir, ops_from_env(workdir)).
- policy defaults to Policy("safe"). When the policy has no backends yet,
  set policy.backends to {tool name: tool.backend for each core tool}.
- append memory.remember_tool(workdir). When skills.catalog(workdir) is not
  empty, append skills.use_skill_tool(workdir).
- When enable_subagents: define make_child(child_depth) returning a new
  Harness over the same workdir, model, policy and extra_tools, with
  on_event=None and persist=False (children are ephemeral: a child session log
  must never hijack resume), depth=child_depth; append
  subagent_tool(make_child, depth).
- self.tools = a name-keyed dict of every tool (including extra_tools), each
  wrapped by a gate: a new Tool with the same name, spec and backend whose run
  first calls policy.check({"name", "args"}); when that returns a reason, the
  wrapper returns "BLOCKED: <reason>" instead of running the tool.
- self.system = memory.build_system_prompt(workdir, skills.catalog_prompt(workdir)).

Methods:
- resume(path=None) -> bool: path defaults to session.latest(workdir); when
  there is none return False; otherwise set session_path and
  messages = session.load(path) (which repairs a crash) and return True when
  messages were loaded.
- run(task) -> str: when persist and there is no session_path, create one with
  session.new_session(workdir, task[:32]). Append the user message, record it,
  then call loop.run_loop with on_event set to a recorder and
  before_turn=lambda m: context.compact(model, m, budget_tokens), so the
  budget is checked at the top of every lap, right after the previous lap's
  tools. The recorder appends every message to the session file when persist
  is true, then calls on_event. Return the final text.

------------------------------------------------------------------------------
2) zill/fleet.py
------------------------------------------------------------------------------
- run_fleet(jobs, make_harness, max_workers=4): jobs are [{name, workdir,
  task}]. Use ThreadPoolExecutor. For each job, make_harness(workdir) then
  .run(task). Success gives {"name", "ok": True, "report": final text}; any
  exception gives {"name", "ok": False, "report": "<ExceptionType>: <message>"}
  and never propagates. Results come back sorted into the input order, because
  as_completed yields them in finish order. Comment why the limit exists:
  the ceiling is the provider's rate limit and your bill, not the CPU.

------------------------------------------------------------------------------
3) zill/client.py and zill/__main__.py
------------------------------------------------------------------------------
- show(message): an event printer. Assistant text plainly; each tool call as
  one line "  -> name(args)" with arguments clipped to 60 characters; the first
  line of each tool result, dimmed, clipped to 100 characters (an empty
  result must not crash).
- ask(call, reason): the approver. Print "approve name(args)? [y/N]" via
  input() and return True only for y or yes.
- main(argv=None) -> int: argparse with -p/--prompt (run one task headless),
  -d/--workdir (default "."), -m/--model, --mode in {safe, yolo, read-only},
  --resume, --max-turns (default 80). headless = prompt is not None. When
  headless, os.environ.setdefault("ZILL_BACKEND", "sandbox") BEFORE the
  harness is built, because Zill only allows yolo with bash off the local
  backend. mode defaults to "yolo" when headless and "safe" otherwise.
  policy = Policy(mode, approver=None if headless else ask).
- Build one Harness with on_event=show. If --resume, call resume().
- Headless: run the prompt, return 0.
- Interactive: print a banner naming the model, mode and jail directory, then
  loop on input(). Ctrl+D (EOFError) returns 0. Ctrl+C during a run prints that
  the session log is safe on disk and that --resume continues it, then goes
  back to the prompt.
- __main__.py: import main from zill.client and run sys.exit(main()), so
  python -m zill works.

------------------------------------------------------------------------------
4) Tests and demos
------------------------------------------------------------------------------
- tests/test_zill_harness.py (about 120 lines, unittest, no network): replace
  provider.complete with a fake model. Prove: safe mode with no approver
  returns a BLOCKED result and writes nothing; yolo mode writes the file;
  resume() after a run restores the messages; a sub-agent run leaves exactly
  one session file; run_fleet keeps input order and turns a failing job into
  ok False without stopping the others; client.main(["-p", ...]) returns 0.
- demos/fleet_demo.py: run_fleet over three small jobs in three fresh folders
  (a haiku in poem.txt; fizzbuzz.py written and run; a job that raises),
  max_workers=2, ZILL_BACKEND=sandbox, policy yolo. Print one line per
  result and PASS when the first two are ok and the third is not.
- demos/harness_demo.py: "start <workdir>" runs Harness(workdir) on "Create
  part1.txt through part5.txt one at a time, then SUMMARY.md describing each",
  printing its pid; "resume <workdir>" calls resume() then
  run("continue the task"); print PASS when all six files exist.

Verify before finishing: all tests pass, then run the three demos.
```

Let it finish. When it's done, run the tests first. They use a fake model, so they cost nothing and they don't need your API key.

[DO: python -m unittest discover tests]

Now the demos. These use the real model, so they do use your key.

First, the front door. In interactive mode, ask it to create a file.

[DO: python -m zill -d demo_interactive]
[DO: type: create hello.txt with a short greeting]

Watch what happens. It stops and asks, "approve write file, yes or no?" Say yes. That question is the gate we wrote in lecture three, now wired in.

Second, headless.

[DO: python -m zill -d demo_headless -p "create notes.md with three bullet points about harnesses"]

This time there was no question. It just ran, wrote the file, and exited. Same class. Different default mode.

Third, the fleet. Three jobs, two workers. One of them is built to fail.

[DO: python -m demos.fleet_demo]

You should see one line for each result. The first two are ok. The third one says failed, and the other two finished anyway. That's the try and except doing its job.

And last, the crash test. This is the one that brings the whole series together.

[DO: python -m demos.harness_demo start demo_crash]

It prints its process ID, and starts building part1.txt through part5.txt. Wait until you see two or three files get written, and then kill it. Hit Ctrl+C, or if you want to be cruel, use kill dash 9, or taskkill on Windows. Kill it while a tool line is printing.

Now look at the folder. Some of the files are there. And there's one session file inside the dot zill folder.

[DO: python -m demos.harness_demo resume demo_crash]

And watch. It loads the session, and you'll see the note, "Interrupted before this ran, process restarted." And then the model checks what's actually on disk, and finishes the job. All six files. It picked up exactly where it died.

Take a second to feel that. That's the permission gate from lecture three, the compaction from four, the memory and the session from five, and the loop from two, all sitting inside one object, and surviving a crash.

[PAUSE]

[PICTURE 16]

So, let's step back. This is the last lecture, so I want to give you the whole picture one more time.

Look at the tower. At the very bottom, in grey, the model. We don't build that. We rent it.

Lecture two gave Zill a voice. A provider to talk to the model, and a loop to keep the conversation going.

Lecture three gave it hands, and a conscience. Tools it can use, a gate that watches every call, and a place where those tools run.

Lecture four taught it to work past its window. Compaction.

Lecture five gave it memory that outlasts the session, skills it loads when needed, sessions that survive a crash, and helpers it can hand work to.

And today, one class that holds it all together, a fleet that runs many of them, and a front door for people and scripts.

The expensive part, the model, you rent for a few cents. The part that makes it yours is small enough to hold in your head. Every file is short. Every behavior traces back to a file you wrote.

So where do you go from here? Three things you can do this week.

One, run Zill on a real task from your own work, using the interactive door. Notice where the gate stops it, and where you'd want it to behave differently.

Two, add one thing. A tracing hook in harness.py, or an extra tool. Remember the table from picture eight. Most features touch one place.

Three, run five small jobs through the fleet, first with two workers, then with five, and compare the time. See for yourself where the rate limit starts to bite.

For homework, do the first and the third. And if you do just one thing after this series, make it the crash test. Kill Zill in the middle of a real task, and resume it.

Thank you so much for building this with me. You started with an empty folder, and you finished with a coding agent that you understand line by line. Go and build something with it.

I'll see you around.

---

## Notes for you (not spoken)

- **Numbering:** this is Zill lecture 6, because lecture 5 in this folder is the memory, sub-agents and durability one. The workshop transcript you sent covered the Odysseus harness, fleet and client, so this script teaches those three ideas on Zill. The loop-engineering part is left out, as you asked.
- **Pictures:** 16 pictures in `diagrams-lecture6/` (diagram-01.png to diagram-16.png). Each shows its number in the corner. Picture 16 is used twice, once when you start building and once for the closing summary. That's deliberate, because the tower works as both.
- **Code was tested, but not against the real model.** I wrote harness.py, fleet.py and client.py in a scratch copy of the Zill package and ran them with a fake model: the gate blocks in safe mode and writes in yolo mode, sessions resume, a sub-agent leaves exactly one session file, the fleet keeps input order and turns a crash into ok False, and headless `client.main` returns 0. Your repo is untouched. Claude Code builds the real files from the prompt.
- **Before recording:** run the build prompt once in Claude Code so the demos are real, and adjust the `python -m ...` lines to whatever it actually created. Kill the crash demo while a tool line is printing, or no "Interrupted" note appears.
- **Check these claims before publishing:** that Hermes and Codex check the budget once before the loop (this came from your workshop notes, not from their source), that Pi checks after the tools, and the cost ordering of the three web-app options (headless CLI, then the Agent SDK, then your own harness).
- **Not mentioned on purpose:** the live workshop, anyone who attended it, and CCAF (that was a separate topic at the end of the workshop).
