# Lecture 6 — build prompt

Paste this into your coding agent from inside the Zill repository.

---

```text
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
