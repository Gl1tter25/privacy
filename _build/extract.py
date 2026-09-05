# -*- coding: utf-8 -*-
"""Extract per-app facts from the 30 legacy privacy pages into apps.json.

Sources:
  - 24 local pages: stage/<slug>-privacy/index.html
  - 6 remote pages fetched to stage/_tmpu/privsrc-<slug>.html

Facts are ported verbatim wherever the legacy page carries them; only the
boilerplate gaps documented in SUMMARY.md are synthesised from family-standard
text (recorded in each app's "_notes").
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]          # app_dev/
STAGE = ROOT / "stage"
OUT = Path(__file__).resolve().parent / "apps.json"

LOCAL_SLUGS = [
    "brewlog", "cleanloop", "coinvault", "expiryloop", "fuellog", "gamevault",
    "giftloop", "groceryloop", "homevault", "keydateloop", "labvault",
    "lendloop", "meterloop", "mileageloop", "movieloop", "packtrail",
    "petvault", "poop-loop", "quantvault", "seedvault", "stitchloop",
    "subvault", "teavault", "wrenchvault",
]
REMOTE_SLUGS = ["leaflog", "moodloop", "pacekeeper", "readtrail", "siplog", "vitalvault"]
ALL_SLUGS = LOCAL_SLUGS + REMOTE_SLUGS

STD_SECTIONS = [
    "scope", "data-you-provide", "local-processing", "advertising", "sharing",
    "permissions", "security", "retention", "children", "international",
    "rights", "changes", "contact",
]

CHANGES_STD = (
    "<p>We may update this Privacy Policy when the App, legal requirements, or "
    "third-party services change. The \u201cLast updated\u201d date above identifies the "
    "current version. Material changes will be reflected on this page and, where "
    "appropriate, communicated in the App or its store listing.</p>"
)

INTERNATIONAL_SYNTH = (
    "<p>Glitter is based in Hong Kong. User-entered records remain on your device "
    "unless you choose to export or share them. Google and its advertising partners "
    "may process advertising-related information in countries other than your own, "
    "subject to their privacy policies and applicable transfer safeguards.</p>"
)

RIGHTS_SYNTH = (
    "<p>Depending on where you live, you may have rights concerning personal "
    "information, including rights to access, correct, delete, restrict, object "
    "to, or withdraw consent for certain processing.</p>\n"
    "        <ul>\n"
    "          <li>Use the App's controls for local records, or uninstall the App.</li>\n"
    "          <li>Use privacy choices in the App's settings where displayed, or Android's advertising privacy controls.</li>\n"
    "          <li>Contact Google regarding information controlled by Google.</li>\n"
    "          <li>Contact Glitter using the email address below for questions or requests concerning this policy.</li>\n"
    "        </ul>\n"
    "        <p>Because Glitter does not receive your local records, we may be unable "
    "to identify or provide records that exist only on your device.</p>"
)

CONTACT_ADDR = (
    "<address>\n"
    "          <strong>Glitter</strong><br>\n"
    "          Hong Kong<br>\n"
    '          Email: <a href="mailto:williamfan12138@gmail.com">williamfan12138@gmail.com</a><br><br>\n'
    "          <strong>Ezra</strong><br>\n"
    '          Email: <a href="mailto:zjh020608@gmail.com">zjh020608@gmail.com</a>\n'
    "        </address>"
)

LEGACY_EMAIL_APPS = {"quantvault": "glitterfan27@gmail.com",
                     "vitalvault": "glitterfan27@gmail.com"}


def pkg_of(slug: str) -> str:
    # Console-proven: Poop Loop = com.gl1tt.poop (factory google-play-publish SKILL)
    if slug == "poop-loop":
        return "com.gl1tt.poop"
    return "com.glitterfan." + slug.replace("-", "")


def src_path(slug: str) -> Path:
    if slug in REMOTE_SLUGS:
        return STAGE / "_tmpu" / f"privsrc-{slug}.html"
    return STAGE / f"{slug}-privacy" / "index.html"


def one(pattern: str, text: str, what: str, slug: str, flags=re.S) -> str:
    m = re.search(pattern, text, flags)
    if not m:
        raise SystemExit(f"[{slug}] MISSING: {what}")
    return m.group(1).strip()


def section_body(html: str, sec_id: str) -> str | None:
    m = re.search(r'<section id="%s">(.*?)</section>' % re.escape(sec_id), html, re.S)
    if not m:
        return None
    body = m.group(1).strip()
    body = re.sub(r"^<h2>.*?</h2>\s*", "", body, flags=re.S)
    return body.strip()


def split_first_p(body: str) -> tuple[str, str]:
    m = re.match(r"\s*(<p>.*?</p>)\s*(.*)$", body, re.S)
    if not m:
        raise SystemExit("scope: no leading <p>")
    return m.group(1).strip(), m.group(2).strip()


def paragraphs_from(blob: str) -> list[str]:
    """Normalise a disclaimer block/section into a list of <p> units."""
    blob = re.sub(r"</?div[^>]*>", "\n", blob)          # unwrap shallow divs
    units = []
    buf = []
    for line in blob.split("\n"):
        line = line.strip()
        if not line:
            if buf:
                units.append(" ".join(buf)); buf = []
            continue
        if line.startswith("<p"):
            if buf:
                units.append(" ".join(buf)); buf = []
            units.append(line)
        else:
            buf.append(line)
    if buf:
        units.append(" ".join(buf))
    out = []
    for u in units:
        u = u.strip()
        if not u:
            continue
        out.append(u if u.startswith("<p") else f"<p>{u}</p>")
    return out


def eyebrow_color(html: str, slug: str) -> str:
    root = one(r":root\s*\{(.*?)\}", html, ":root vars", slug)
    vars_ = dict(re.findall(r"--([\w-]+)\s*:\s*([^;]+);", root))
    rule = one(r"\.eyebrow\s*\{(.*?)\}", html, ".eyebrow rule", slug)
    col = one(r"color:\s*([^;]+);", rule, ".eyebrow color", slug)
    m = re.fullmatch(r"var\(--([\w-]+)(?:\s*,\s*([^)]+))?\)", col)
    if m:
        col = vars_.get(m.group(1), "") or (m.group(2) or "")
    col = col.strip()
    if not re.fullmatch(r"#[0-9a-fA-F]{3,8}", col):
        raise SystemExit(f"[{slug}] eyebrow color unresolved: {col!r}")
    return col


def main() -> None:
    apps = []
    report = []
    for slug in ALL_SLUGS:
        html = src_path(slug).read_text(encoding="utf-8")
        notes: list[str] = []

        title = one(r"<title>(.*?)</title>", html, "title", slug, flags=0)
        app_name = re.sub(r"\s*Privacy Policy\s*$", "", title).strip()
        meta_desc = one(r'<meta name="description" content="([^"]*)"', html, "meta description", slug, flags=0)
        theme_color = one(r'<meta name="theme-color" content="([^"]*)"', html, "theme-color", slug, flags=0)
        og_title = one(r'<meta property="og:title" content="([^"]*)"', html, "og:title", slug, flags=0)
        og_desc = one(r'<meta property="og:description" content="([^"]*)"', html, "og:description", slug, flags=0)
        h1 = one(r"<h1>(.*?)</h1>", html, "h1", slug)
        lede = one(r'<p class="lede">(.*?)</p>', html, "lede", slug)
        badges = one(r'<div class="meta">(.*?)</div>', html, "badges", slug)
        summary = one(r'<div class="summary"[^>]*>(.*?)</div>\s*<main>', html, "summary", slug)
        summary = re.sub(r"\s*<main>$", "", summary).strip()
        footer = one(r"<footer>\s*<p>(.*?)</p>", html, "footer", slug)
        brow = eyebrow_color(html, slug)

        # ---- sections -----------------------------------------------------
        raw = {s: section_body(html, s) for s in STD_SECTIONS}
        disc = section_body(html, "disclaimer")
        purch = section_body(html, "purchase")
        chinese = section_body(html, "chinese")
        disc_div = None
        m = re.search(r'<div class="disclaimer">(.*?)</div>', html, re.S)
        if m:
            disc_div = m.group(1).strip()

        # 1. scope: regenerate para 1 (uniform + package sentence), keep the rest
        scope = raw["scope"]
        if scope is None:
            raise SystemExit(f"[{slug}] no scope section")
        _p1, scope_rest = split_first_p(scope)
        parts = []
        if scope_rest:
            parts.append(scope_rest)
        blob = disc or disc_div
        if blob:
            ps = paragraphs_from(blob)
            parts.extend(ps)
            notes.append(f"disclaimer {'section' if disc else 'div'} folded into scope ({len(ps)} paragraph(s))")
        scope_final = "\n        ".join(["{{SCOPE_P1}}"] + parts) if parts else "{{SCOPE_P1}}"

        # 4. advertising: fold purchase paragraph if present
        advert = raw["advertising"]
        if advert is None:
            raise SystemExit(f"[{slug}] no advertising section")
        if purch:
            advert = advert + "\n        " + purch
            notes.append("purchase section folded into advertising")

        # 10/11/12 gaps
        intl = raw["international"]
        if intl is None:
            intl = INTERNATIONAL_SYNTH
            notes.append("international SYNTHESISED (family-standard text)")
        rights = raw["rights"]
        if rights is None:
            rights = RIGHTS_SYNTH
            notes.append("rights SYNTHESISED (family-standard text)")
        if raw["changes"] is None:
            notes.append("changes MISSING in source; standard text used")
        elif "Material changes" not in raw["changes"]:
            notes.append("changes upgraded to standard wording (material-changes sentence added)")
        if chinese is not None:
            notes.append("dropped 'chinese' full-policy summary section (no facts beyond English text)")

        # 13. contact: standard dual card; legacy email preserved where present
        subject = f"Please include \u201c{app_name} Privacy\u201d in the subject line so we can identify your request."
        contact = CONTACT_ADDR + f"\n        <p>{subject}</p>"
        if slug in LEGACY_EMAIL_APPS:
            em = LEGACY_EMAIL_APPS[slug]
            contact += (f'\n        <p>Earlier versions of this policy listed '
                        f'<a href="mailto:{em}">{em}</a> as the contact address; '
                        f'it remains a valid way to reach Glitter about {app_name}.</p>')
            notes.append(f"legacy contact {em} preserved alongside standard dual card")

        missing = [s for s in STD_SECTIONS if raw[s] is None and s not in
                   ("international", "rights", "changes")]
        if missing:
            raise SystemExit(f"[{slug}] unexpected missing sections: {missing}")

        apps.append({
            "slug": slug,
            "app_name": app_name,
            "package": pkg_of(slug),
            "meta_description": meta_desc,
            "theme_color": theme_color,
            "eyebrow_color": brow,
            "og_title": og_title,
            "og_description": og_desc,
            "title": title,
            "h1": h1,
            "lede": lede,
            "badges": badges,
            "summary": summary,
            "sections": {
                "scope": scope_final,
                "data-you-provide": raw["data-you-provide"],
                "local-processing": raw["local-processing"],
                "advertising": advert,
                "sharing": raw["sharing"],
                "permissions": raw["permissions"],
                "security": raw["security"],
                "retention": raw["retention"],
                "children": raw["children"],
                "international": intl,
                "rights": rights,
                "changes": CHANGES_STD,
                "contact": contact,
            },
            "footer": footer,
            "_source": str(src_path(slug).relative_to(ROOT)).replace("\\", "/"),
            "_notes": notes,
        })
        report.append((slug, app_name, notes))

    OUT.write_text(json.dumps({"apps": apps}, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print(f"wrote {OUT} ({len(apps)} apps, {OUT.stat().st_size} bytes)\n")
    for slug, name, notes in report:
        print(f"[{slug}] {name}")
        for n in notes:
            print(f"    - {n}")


if __name__ == "__main__":
    sys.exit(main())
