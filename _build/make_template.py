# -*- coding: utf-8 -*-
"""Turn stage/poop-loop-privacy/index.html into _build/template.html.

Every replacement is anchored on surrounding markup and asserted to occur
exactly once, so the template is provably the Poop Loop page with only the
variable regions swapped for {{TOKENS}}.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "stage" / "poop-loop-privacy" / "index.html"
OUT = Path(__file__).resolve().parent / "template.html"

SECTIONS = [
    "scope", "data-you-provide", "local-processing", "advertising", "sharing",
    "permissions", "security", "retention", "children", "international",
    "rights", "changes", "contact",
]


def rep1(text: str, pattern: str, repl: str, what: str, flags=0) -> str:
    new, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"template: pattern for {what} did not match exactly once")
    return new


def lit1(text: str, old: str, new: str, what: str) -> str:
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"template: literal for {what} occurs {n} times")
    return text.replace(old, new)


def main() -> None:
    raw = SRC.read_bytes().decode("utf-8")
    t = raw.replace("\r\n", "\n")          # work in LF; render.py writes CRLF back

    t = lit1(t, '<meta name="description" content="Privacy Policy for the Poop Loop Android application, published by Glitter.">',
             '<meta name="description" content="{{META_DESCRIPTION}}">', "meta description")
    t = lit1(t, '<meta name="theme-color" content="#5a3b28">',
             '<meta name="theme-color" content="{{THEME_COLOR}}">', "theme-color")
    t = lit1(t, '<meta property="og:title" content="Poop Loop Privacy Policy">',
             '<meta property="og:title" content="{{OG_TITLE}}">', "og:title")
    t = lit1(t, '<meta property="og:description" content="How Poop Loop stores health records on-device and how advertising data is handled.">',
             '<meta property="og:description" content="{{OG_DESCRIPTION}}">', "og:description")
    t = lit1(t, "<title>Poop Loop Privacy Policy</title>", "<title>{{TITLE}}</title>", "title")
    t = lit1(t, "      --green: #35684a;", "      --green: {{EYEBROW_COLOR}};", "eyebrow color var")
    t = lit1(t, "<h1>Poop Loop Privacy Policy</h1>", "<h1>{{H1}}</h1>", "h1")
    t = rep1(t, r'<p class="lede">.*?</p>', '<p class="lede">{{LEDE}}</p>', "lede", flags=re.S)
    t = rep1(t, r'<div class="meta">.*?</div>',
             '<div class="meta">\n        {{BADGES}}\n      </div>', "badges", flags=re.S)
    t = rep1(t, r'<div class="summary" aria-label="Privacy summary">.*?</div>',
             '<div class="summary" aria-label="Privacy summary">\n      {{SUMMARY}}\n    </div>',
             "summary", flags=re.S)

    for sec in SECTIONS:
        token = "{{SEC_" + sec.replace("-", "_").upper() + "}}"
        t = rep1(t,
                 r'(<section id="%s">\s*<h2>.*?</h2>).*?</section>' % re.escape(sec),
                 lambda m, tok=token: m.group(1) + "\n        " + tok + "\n      </section>",
                 f"section {sec}", flags=re.S)

    t = lit1(t, "<p>© 2026 Glitter · Poop Loop</p>", "<p>{{FOOTER}}</p>", "footer")

    leftover = re.findall(r"Poop Loop", t)
    if leftover:
        raise SystemExit(f"template: {len(leftover)} untokenised 'Poop Loop' occurrence(s)")

    OUT.write_bytes(t.encode("utf-8"))
    tokens = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", t)))
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
    print(f"{len(tokens)} tokens: {', '.join(tokens)}")


if __name__ == "__main__":
    sys.exit(main())
