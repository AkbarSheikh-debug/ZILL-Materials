# Lecture 5 — build prompt

Paste this into your coding agent from inside the Zill repository.

---

```text
You are building the next part of Zill (lecture 5 of the series): long-term
memory, skills, durable sessions, and sub-agents. The parts are cumulative.
Your repo already contains the package zill/ with provider.py, loop.py
(run_loop(model, system, messages, tools, on_event, max_turns=80,
before_turn=None)), tools.py (Tool, the @tool decorator, core_tools),
operations.py, security.py and context.py (compact), plus demos/ and tests/
from lectures 2 to 4.

Today adds FOUR new files: zill/memory.py, zill/skills.py, zill/session.py and
zill/subagent.py. No existing file changes. The class that wires everything
together (harness.py) comes in the next lecture, so today's demos wire the
pieces by hand. Build exactly what this spec describes and nothing else.

GROUND RULES
- Python 3.10+, standard library only, no third-party packages.
- Must run on Windows, macOS and Linux.
- Same code standard as before: a module docstring on every file naming the
  concept it teaches and the design rules it embodies; a docstring on every
  public function; a short comment wherever behaviour is subtle (the torn
  tail, the repair, the depth cap, why children do not persist).
- Size targets including documentation, within about 15%: memory.py 60 lines,
  skills.py 60, session.py 70, subagent.py 35, tests 200, demos 60 each.
- Commit after each milestone: memory, skills, session, subagent, tests, demos.
- Do not add features beyond this spec. Where the spec is ambiguous, pick the
  simpler option and note it in a one-line comment at the top of the file.
- Read loop.py, tools.py and context.py before you start, and match their
  names and message shapes exactly: {"role": "user"|"assistant"|"tool",
  "text": ...}, assistant messages carry "tool_calls": [{"name", "args", ...}],
  tool messages carry "name". Tools are built with @tool(description, **params)
  and every parameter is a string. If anything below contradicts the code,
  stop and report it instead of guessing.

THE THREE IDEAS TO PRESERVE
1. Two clocks. The tape (the messages list) grows during a session. The
   system prompt is rebuilt between sessions. remember() writes to a file on
   disk; the fact reaches the prompt at the next session.
2. Append is remember. Every message is written to disk the moment it exists,
   one JSON line per message, never rewritten. A crash can damage at most the
   last line.
3. The harness inside the harness. A sub-agent is the same loop, run again
   with an empty tape, exposed to the parent as one tool. The parent sees one
   call going out and one report coming back.

------------------------------------------------------------------------------
1) zill/memory.py: the system prompt and the notebook beside the desk
------------------------------------------------------------------------------
- MEMORY_FILE = "ZILL.md".
- BASE_PROMPT: states that the agent is Zill, a small, sharp coding agent
  working inside one directory with the tools provided; then these rules:
  act, don't narrate; inspect before assuming; prefer edit_file for small
  changes; after building something, verify it by running it or reading it
  back; if a tool call fails, read the error and fix the cause, never repeat
  a failing call unchanged; when the task is complete, reply with a short
  plain-text summary and stop calling tools.
- build_system_prompt(workdir, extra="") -> str: BASE_PROMPT, then one line
  "Environment: <platform.system()>, working directory: <realpath(workdir)>",
  then, when workdir/ZILL.md exists, a section
  "Project memory (ZILL.md):\n<its contents, stripped>", then extra when it
  is non-empty. Sections are joined by one blank line.
- remember(workdir, note) -> str: append "- <note stripped>\n" to ZILL.md
  (create it if missing), return "Remembered in ZILL.md".
- remember_tool(workdir) -> Tool: a @tool named remember whose description
  tells the model to save a durable project fact that a new colleague would
  need, never a transcript or a one-off detail. One parameter, note.

------------------------------------------------------------------------------
2) zill/skills.py: expertise as folders
------------------------------------------------------------------------------
- SKILLS_DIR = "skills".
- catalog(workdir) -> dict: {name: {"description", "path"}} for every
  workdir/skills/<name>/SKILL.md. The description comes from a
  "description:" line in the file's front matter; when there is none, use the
  first non-empty line of the body. Sorted by name.
- catalog_prompt(workdir) -> str: "" when there are no skills; otherwise
  "Skills available (load one with the use_skill tool when relevant):"
  followed by one "- name: description" line per skill.
- read_skill(workdir, name) -> str: the full SKILL.md text, or
  "ERROR: no skill named <name>. Available: <comma-separated names>".
- use_skill_tool(workdir) -> Tool: a @tool named use_skill that returns
  read_skill(workdir, name). One parameter, name.

------------------------------------------------------------------------------
3) zill/session.py: the spine
------------------------------------------------------------------------------
- SESSION_DIR = ".zill/sessions".
- new_session(workdir, label="session") -> str: create the directory; slugify
  the label to letters, digits and dashes, clipped to 40 chars; return
  <workdir>/.zill/sessions/<unix-timestamp>-<slug>.jsonl.
- append(path, message): write json.dumps(message, ensure_ascii=False) plus
  "\n", open in append mode, flush, then os.fsync.
- latest(workdir) -> str | None: the newest .jsonl in the session dir by
  modification time, or None.
- load(path) -> list: parse line by line. A line that fails to parse is a torn
  tail: stop there and keep everything before it. Then return _repair(list).
- _repair(messages) -> list: find the last assistant message; count the tool
  messages after it; for each of its tool_calls beyond that count, append
  {"role": "tool", "name": <call name>,
   "text": "Interrupted before this ran (process restarted)."}.
  Never pretend a tool ran, and never delete the request. The result must
  always satisfy the rule that every tool call gets exactly one result.

------------------------------------------------------------------------------
4) zill/subagent.py: the harness inside the harness
------------------------------------------------------------------------------
- subagent_tool(make_child, depth=0, max_depth=2) -> Tool, built with @tool:
  name spawn_agent; description: "Delegate a self-contained task to a fresh
  sub-agent with its own clean context. Give it a complete brief: it cannot
  see this conversation. Returns the sub-agent's final report." One
  parameter, task, described as complete, self-contained instructions.
- When depth >= max_depth, return
  "ERROR: sub-agent depth limit reached; do this task yourself".
- Otherwise child = make_child(depth + 1) and return child.run(task).
  make_child is supplied by the caller and returns any object with
  run(task) -> str. Children never write session logs: only the top-level
  caller persists (say so in a comment; the next lecture's harness.py enforces
  it with persist=False).

------------------------------------------------------------------------------
5) tests/test_zill_memory_session.py: stdlib unittest, no network
------------------------------------------------------------------------------
a) build_system_prompt without ZILL.md has no "Project memory" section; after
   remember() it contains the note, and after two remember() calls with
   different notes, each note appears exactly once.
b) catalog and catalog_prompt with two skill folders; read_skill for a
   missing name returns the ERROR text listing the available names.
c) append then load round-trips three messages exactly.
d) A file whose last line is cut in half loads the complete lines and drops
   the torn one.
e) _repair: an assistant message with two tool_calls followed by one tool
   message gets exactly one appended "Interrupted" tool message, named after
   the second call. A conversation with no open calls is unchanged.
f) latest() returns the newest file; None when the directory is missing.
g) spawn_agent at max_depth returns the ERROR text and never calls
   make_child; below max_depth it calls make_child(depth + 1) once and
   returns the child's run() result (use a fake child).

------------------------------------------------------------------------------
6) demos: wire the pieces by hand (harness.py arrives next lecture)
------------------------------------------------------------------------------
Use the same tool setup as demos/context_demo.py (sandbox backend, a fresh
working folder). Each demo builds tools as a name-keyed dict and calls
run_loop directly.

demos/memory_demo.py <workdir>
  The demo first writes a Makefile with a test target that runs
  python -m unittest. Run 1: system = build_system_prompt(workdir,
  catalog_prompt(workdir)); tools = core tools + remember + use_skill.
  Task: "Find out how this project runs its tests, then remember it."
  Run 2, with a fresh messages list and a freshly built system prompt:
  "How do I run the tests here? Answer in one line without using any tools."
  Print both answers, and PASS when run 2 mentions make test.

demos/resume_demo.py start|resume <workdir>
  start: path = session.new_session(workdir, task[:32]); the on_event
  callback calls session.append(path, msg); the user message is appended
  before run_loop starts. Task: "Create part1.txt through part5.txt one at
  a time, then SUMMARY.md describing each."
  resume: messages = session.load(session.latest(workdir)); print the last
  three messages; append {"role": "user", "text": "continue the task"} and
  run again with the same on_event. At the end, print PASS when all six
  files exist.
  At start, print the pid and how to kill it: Ctrl+C, or kill -9 <pid> on
  macOS and Linux, or taskkill /F /PID <pid> on Windows.

demos/subagent_demo.py <workdir>
  make_child(depth) returns a small Child object whose run(task) calls
  run_loop with a fresh messages list, the same core tools, and its own
  spawn_agent tool built with subagent_tool(make_child, depth). Children do
  not write sessions. The parent persists the way resume_demo does. Task:
  "Use spawn_agent twice: delegate writing utils.py with a slugify(text)
  function to one child, and test_utils.py with five asserts to another;
  then run python test_utils.py yourself and report." Print PASS when the
  tests pass and .zill/sessions contains exactly one file.

------------------------------------------------------------------------------
VERIFY BEFORE FINISHING: report each one honestly, with the output
------------------------------------------------------------------------------
(a) All tests pass, including the tests from lectures 2 to 4.
(b) memory_demo prints PASS, and run 2 answered without calling a tool.
(c) resume_demo: start it, kill it partway, run resume; the transcript shows
    the "Interrupted before this ran" note when the kill landed mid-tool,
    and all six files exist at the end. Paste the last two lines of the
    session file from before the resume.
(d) subagent_demo prints PASS with exactly one session file.
(e) git log shows today's commits.
If something cannot be verified (for example, no API key, or the kill landed
between turns so no repair was needed), say so plainly instead of claiming
success.
```
