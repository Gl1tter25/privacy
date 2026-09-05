# -*- coding: utf-8 -*-
"""Render all app privacy pages from template.html + apps.json.

Usage:
  python -X utf8 render.py            # render every app into stage/privacy/<slug>/index.html
  python -X utf8 render.py poop-loop  # render one app (prints path)

Output files are CRLF (byte convention of the Poop Loop original).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BUILD = Path(__file__).resolve().parent
TEMPLATE = BUILD / "template.html"
APPS_JSON = BUILD / "apps.json"
OUT_ROOT = ROOT / "stage" / "privacy"

SCOPE_P1 = (
    "<p>This Privacy Policy applies to the {app} Android application (the \u201cApp\u201d), "
    "published by <strong>Glitter</strong>, based in Hong Kong (\u201cGlitter,\u201d \u201cwe,\u201d "
    "\u201cus,\u201d or \u201cour\u201d). It explains how information is accessed, used, stored, "
    "disclosed, retained, and deleted when you use the App. "
    "The App's package name is {pkg}.</p>"
)


def render_app(template: str, app: dict) -> str:
    values = {
        "META_DESCRIPTION": app["meta_description"],
        "THEME_COLOR": app["theme_color"],
        "OG_TITLE": app["og_title"],
        "OG_DESCRIPTION": app["og_description"],
        "TITLE": app["title"],
        "EYEBROW_COLOR": app["eyebrow_color"],
        "H1": app["h1"],
        "LEDE": app["lede"],
        "BADGES": app["badges"],
        "SUMMARY": app["summary"],
        "FOOTER": app["footer"],
    }
    for sec_id, body in app["sections"].items():
        token = "SEC_" + sec_id.replace("-", "_").upper()
        if "{{SCOPE_P1}}" in body:
            body = body.replace(
                "{{SCOPE_P1}}",
                SCOPE_P1.format(app=app["app_name"], pkg=app["package"]))
        values[token] = body

    out = template
    for token, value in values.items():
        needle = "{{" + token + "}}"
        if needle not in out:
            raise SystemExit(f"[{app['slug']}] token not found in template: {needle}")
        out = out.replace(needle, value)
    stray = re.findall(r"\{\{[^}]*\}\}", out)
    if stray:
        raise SystemExit(f"[{app['slug']}] unreplaced tokens: {stray}")
    return out


def main() -> None:
    template = TEMPLATE.read_bytes().decode("utf-8")
    apps = json.loads(APPS_JSON.read_text(encoding="utf-8"))["apps"]
    only = sys.argv[1] if len(sys.argv) > 1 else None

    done = 0
    for app in apps:
        if only and app["slug"] != only:
            continue
        html = render_app(template, app)
        html = html.replace("\n", "\r\n")            # Poop Loop byte convention
        dest = OUT_ROOT / app["slug"] / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(html.encode("utf-8"))
        print(f"[{app['slug']}] -> {dest.relative_to(ROOT)} ({dest.stat().st_size} bytes)")
        done += 1
    if only and done == 0:
        raise SystemExit(f"unknown slug: {only}")
    print(f"rendered {done} page(s)")


if __name__ == "__main__":
    sys.exit(main())
