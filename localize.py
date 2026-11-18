#!/usr/bin/env python3
"""Download MAP's photos from Wix into img/ so the site no longer depends on Wix.

Run once from the site folder (needs internet):
    python3 tools/localize.py && python3 tools/build.py
After that every page loads its photos from img/.
"""
import urllib.request
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / "tools" / "build.py").read_text()
IMG = {}
exec(src[src.index("IMG = {"):src.index("}\n", src.index("IMG = {")) + 2], {}, ns := {})
IMG = ns["IMG"]

out = ROOT / "img"
out.mkdir(exist_ok=True)
for key, (mid, w, h) in IMG.items():
    ext = "png" if mid.endswith(".png") else "jpg"
    s = min(1.0, 2000 / max(w, h))
    url = f"https://static.wixstatic.com/media/{mid}/v1/fit/w_{int(w*s)},h_{int(h*s)},q_85/{key}.{ext}"
    dest = out / f"{key}.{ext}"
    print("downloading", key, "...", end=" ", flush=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        dest.write_bytes(r.read())
    print(f"{dest.stat().st_size // 1024} KB")
print("Done. Now run: python3 tools/build.py")
