# Build prompts

At the end of each lecture the instructor pastes one long prompt into a coding agent, and the agent writes that lecture's part of Zill.
These are those prompts, exactly as used. They are cumulative: each one assumes the files from the earlier lectures already exist.

| Lecture | Prompt | What it builds |
|---|---|---|
| 2 | [lecture-2-build-prompt.md](lecture-2-build-prompt.md) | `provider.py`, `loop.py`, the dice demo |
| 3 | [lecture-3-build-prompt.md](lecture-3-build-prompt.md) | tools, execution backends, permission gate, sandbox |
| 4 | [lecture-4-build-prompt.md](lecture-4-build-prompt.md) | `context.py` and the compaction fold |
| 5 | [lecture-5-build-prompt.md](lecture-5-build-prompt.md) | memory, skills, durable sessions, sub-agents |
| 6 | [lecture-6-build-prompt.md](lecture-6-build-prompt.md) | `harness.py`, `fleet.py`, `client.py`, `__main__.py` |

Lecture 1 is concepts only, so it has no build prompt.

Paste a prompt into your coding agent from inside the project folder. Fill in the placeholders (`<YOUR PROVIDER>`, `<YOUR MODEL ID>`, the path to your `.env`) in the Lecture 2 prompt first.
