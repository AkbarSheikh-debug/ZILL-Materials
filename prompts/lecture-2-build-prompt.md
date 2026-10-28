# Lecture 2 — build prompt

Paste this into your coding agent from inside the Zill repository.

---

```text
You are building lecture 2 of Zill, a minimal agentic harness in Python.
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
- Read the key from the environment variable ZILL_API_KEY="". A .env file at
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
