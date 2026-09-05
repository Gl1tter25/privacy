# -*- coding: utf-8 -*-
"""Build the hub page stage/privacy/index.html listing all 30 app policies.

Same single-file offline style as the Poop Loop template: the template's CSS
block is reused verbatim and a small card-grid block is grafted on.
"""
import html as htmlmod
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BUILD = Path(__file__).resolve().parent
TEMPLATE = BUILD / "template.html"
APPS_JSON = BUILD / "apps.json"
OUT = ROOT / "stage" / "privacy" / "index.html"

CARD_CSS = """
    .cards {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px;
      margin: 22px 0;
    }

    .card {
      display: flex;
      flex-direction: column;
      gap: 6px;
      padding: 20px;
      border: 1px solid var(--line);
      border-radius: 20px;
      background: rgba(255, 253, 248, .9);
    }

    .card h2 { margin: 0; font-size: 1.15rem; letter-spacing: -.01em; }
    .card .pkg { color: var(--accent-dark); font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: .8rem; }
    .card p { margin: 0; color: var(--muted); font-size: .91rem; }
    .card a { margin-top: auto; padding-top: 8px; font-weight: 700; text-decoration: none; }
    .card a:hover { text-decoration: underline; }
"""


def main() -> None:
    t = TEMPLATE.read_bytes().decode("utf-8")
    css_block = t.split("<style>", 1)[1].split("</style>", 1)[0]

    # reuse the template CSS verbatim; graft card styles before the media query
    css = css_block.replace("    @media (max-width: 720px) {",
                            CARD_CSS + "\n    @media (max-width: 720px) {")
    css = css.replace("      .summary { grid-template-columns: 1fr; }",
                      "      .summary, .cards { grid-template-columns: 1fr; }")

    apps = json.loads(APPS_JSON.read_text(encoding="utf-8"))["apps"]
    apps = sorted(apps, key=lambda a: (a["slug"] != "poop-loop", a["app_name"].lower()))

    cards = []
    for a in apps:
        name = htmlmod.escape(a["app_name"])
        desc = htmlmod.escape(a["og_description"])
        cards.append(
            f'      <article class="card">\n'
            f"        <h2>{name}</h2>\n"
            f'        <span class="pkg">{htmlmod.escape(a["package"])}</span>\n'
            f"        <p>{desc}</p>\n"
            f'        <a href="./{a["slug"]}/">Privacy policy &rarr;</a>\n'
            f"      </article>")
    cards_html = "\n".join(cards)

    page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Unified privacy policies for all Android applications published by Glitter.">
  <meta name="author" content="Glitter, Ezra">
  <meta name="theme-color" content="#5a3b28">
  <meta property="og:title" content="Glitter App Privacy Policies">
  <meta property="og:description" content="One hub for the privacy policies of every Android app published by Glitter.">
  <meta property="og:type" content="website">
  <title>Glitter App Privacy Policies</title>
  <style>{css}</style>
</head>
<body>
  <div class="shell">
    <header class="hero">
      <p class="eyebrow">Glitter · Hong Kong</p>
      <h1>App Privacy Policies</h1>
      <p class="lede">Every Android app published by Glitter keeps the records you enter on your own device. This hub links to the full privacy policy of each app — same promises, same layout, one address per app.</p>
      <div class="meta">
        <span class="badge">{len(apps)} apps</span>
        <span class="badge">On-device first</span>
        <span class="badge">No account required</span>
        <span class="badge">Authors: Glitter &amp; Ezra</span>
      </div>
    </header>

    <div class="summary" aria-label="How these policies work">
      <article><strong>One layout</strong><span>All policies follow the same 13-section structure, so every answer is in the same place for every app.</span></article>
      <article><strong>On-device first</strong><span>User-entered records stay in the app's private storage; Glitter runs no collection server for them.</span></article>
      <article><strong>Same contacts</strong><span>Every policy ends with the same Glitter (Hong Kong) and Ezra contact cards.</span></article>
    </div>

    <main>
      <section id="apps">
        <h2>All apps</h2>
        <p>Pick an app to read its full privacy policy. Each policy also lives at <strong>gl1tter25.github.io/privacy/&lt;app&gt;/</strong> — the address used in the app's Google Play listing.</p>
      </section>
    </main>

    <div class="cards" aria-label="App privacy policies">
{cards_html}
    </div>

    <footer>
      <p>© 2026 Glitter · App Privacy Policies</p>
    </footer>
  </div>
</body>
</html>
"""
    OUT.write_bytes(page.replace("\n", "\r\n").encode("utf-8"))
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes, {len(apps)} cards)")


if __name__ == "__main__":
    sys.exit(main())
