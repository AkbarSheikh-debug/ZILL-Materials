# Lecture 3 — build prompt

Paste this into your coding agent from inside the Zill repository.

---

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
