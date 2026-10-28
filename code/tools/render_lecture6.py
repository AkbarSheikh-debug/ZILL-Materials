"""Render zill-lecture6-diagrams.html to diagrams-lecture6/diagram-NN.png.

    python render_lecture6.py            # render every sheet
    python render_lecture6.py 3 17       # render only these sheets
    python render_lecture6.py --audit    # list text that leaves its box or collides

Needs Chrome or Edge. Standard library only.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGE = ROOT / "zill-lecture6-diagrams.html"
OUT = ROOT / "diagrams-lecture6"
CANDIDATES = [
    os.environ.get("CHROME", ""),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    shutil.which("google-chrome") or "", shutil.which("chromium") or "",
]


def browser():
    for c in CANDIDATES:
        if c and Path(c).exists():
            return c
    sys.exit("No Chrome or Edge found. Set the CHROME environment variable to its path.")


def chrome(args, query):
    with tempfile.TemporaryDirectory() as profile:
        cmd = [browser(), "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
               "--force-device-scale-factor=1", "--window-size=1920,1080", "--virtual-time-budget=4000",
               f"--user-data-dir={profile}", *args, PAGE.as_uri() + "?" + query]
        return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)


def render(n):
    target = OUT / f"diagram-{n:02d}.png"
    chrome([f"--screenshot={target}"], f"s={n}")
    return n, target.exists() and target.stat().st_size


def count():
    return len(re.findall(r'<svg class="d"', PAGE.read_text(encoding="utf-8")))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--audit" in sys.argv:
        dom = chrome(["--dump-dom"], "audit=1").stdout
        m = re.search(r'<pre id="report">(.*?)</pre>', dom, flags=re.S)
        report = m.group(1) if m else "no report found; the page did not finish loading"
        print(report.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"'))
        sys.exit(0)
    wanted = [int(a) for a in sys.argv[1:] if a.isdigit()] or list(range(1, count() + 1))
    OUT.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for n, size in pool.map(render, wanted):
            print(f"{'ok  ' if size else 'FAIL'} diagram-{n:02d}.png  {size // 1024 if size else 0} KB")
