"""Builds the CapExplorer support site: index.html, privacy/index.html, terms/index.html.

    python3 build.py

The legal pages come from src/privacy.md and src/terms.md, copies of the app's
App/Resources/Legal/*.md (keep them in step). Plain static output: GitHub Pages
serves it as is (.nojekyll).
"""
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

# The app's $1,000 split (datacenter.json `thousand`) and its colours (Theme.swift pieceColors).
# Names only on the page: the figures stay in the app.
PIECES = [
    ("Compute tray", 485, "#5fd39a", True), ("Top-of-rack switch", 115, "#6aa8ff", True),
    ("NVLink switch tray", 20, "#b28cff", True), ("Power shelf", 9, "#f0b44c", True),
    ("NVLink spine", 11, "#e8845a", True), ("AI rack", 23, "#8fa39a", True),
    ("Coolant units", 35, "#3f8f8a", False), ("Electrical equipment", 93, "#d98b3a", False),
    ("Chillers", 17, "#4fb3b0", False), ("Fibre, controls and security", 12, "#c9d25a", False),
    ("Building shell", 75, "#5d6a66", False), ("Installers", 75, "#4a5652", False),
    ("Grid hookup", 15, "#3d4845", False), ("Land and site work", 10, "#323b39", False),
    ("Permits and the rest", 5, "#2a3230", False),
]

EMAIL = "lgangaramaney@gmail.com"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;600;700;800&display=swap" rel="stylesheet">')


def page(title, description, body, root, current):
    def link(href, label, key):
        aria = ' aria-current="page"' if key == current else ""
        return f'<a href="{root}{href}"{aria}>{label}</a>'
    nav = link("#support" if current == "home" else "./#support", "Support", "support") \
        + link("privacy/", "Privacy", "privacy") + link("terms/", "Terms", "terms")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta name="theme-color" content="#07090c">
<link rel="icon" type="image/png" sizes="32x32" href="{root}assets/favicon-32.png">
<link rel="icon" type="image/png" sizes="64x64" href="{root}assets/favicon-64.png">
<link rel="apple-touch-icon" href="{root}assets/apple-touch-icon.png">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:image" content="https://lokesh234.github.io/capexplorer-site/assets/og-icon.jpg">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary">
{FONTS}
<link rel="stylesheet" href="{root}assets/site.css">
</head>
<body>
<div class="wrap">
<header class="top">
  <a class="mark" href="{root}"><img src="{root}assets/icon-96.png" alt="" width="32" height="32">CapExplorer</a>
  <nav class="nav" aria-label="Site">{nav}</nav>
</header>
{body}
<footer class="foot">
  <span>© 2026 Lokesh Gangaramaney. For information and education only; not investment advice.</span>
  <nav aria-label="Legal"><a href="{root}privacy/">Privacy Policy</a><a href="{root}terms/">Terms of Use</a></nav>
</footer>
</div>
</body>
</html>
"""


def home():
    bar = "".join(f'<span style="--w:{w};--c:{c};--i:{i}" title="{html.escape(n)}"></span>'
                  for i, (n, w, c, _) in enumerate(PIECES))
    legend = "".join(f'<li style="--c:{c}"{" class=\"rack\"" if rack else ""}>{html.escape(n)}</li>'
                     for n, _, c, rack in PIECES)
    body = f"""
<main>
<section class="hero">
  <h1>Take an AI data center apart.</h1>
  <p class="lede">CapExplorer shows where every $1,000 spent on AI infrastructure goes, part by part, and which companies get paid for each.</p>
  <p class="status"><strong>For iPad and iPhone.</strong> Coming soon to the App Store.</p>
  <figure class="split">
    <figcaption>Every $1,000, split by what it buys <span>(the app has the figures and their sources)</span></figcaption>
    <div class="bar" role="img" aria-label="A bar split into the parts of $1,000 of AI data center spending, from the compute tray, the largest, to permits and fees">{bar}</div>
    <ul class="legend">{legend}</ul>
  </figure>
</section>

<section class="section" id="support">
  <div>
    <h2>Support</h2>
    <p>Questions about the app, or something not working? Email us and include your device and what you were looking at.</p>
    <p>Every figure in CapExplorer cites a public source. If you think a figure, a supplier or a source is wrong, tell us and we'll check it.</p>
  </div>
  <div class="contact">
    <a class="email" href="mailto:{EMAIL}?subject=CapExplorer">{EMAIL}</a>
    <dl>
      <dt>Replies</dt><dd>Usually within a few days</dd>
      <dt>Account</dt><dd>None needed; the app works offline</dd>
      <dt>Your data</dt><dd>The app collects none. <a href="privacy/">Privacy Policy</a></dd>
    </dl>
  </div>
</section>
</main>
"""
    return page("CapExplorer: take an AI data center apart",
                "See where every $1,000 of AI data center spending goes, part by part, and which companies get paid.",
                body, "", "home")


def inline(text):
    text = html.escape(text)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


def markdown(md):
    """The small subset the legal documents use: # and ## headings, paragraphs, - lists, **bold**."""
    out, para, items = [], [], []

    def flush():
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
            para.clear()
        if items:
            out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>")
            items.clear()
    first_para = True
    for line in md.splitlines():
        s = line.strip()
        if not s:
            flush()
            continue
        if s.startswith("## "):
            flush(); out.append(f"<h2>{inline(s[3:])}</h2>")
        elif s.startswith("# "):
            flush(); out.append(f"<h1>{inline(s[2:])}</h1>")
        elif s.startswith("- "):
            if para: flush()
            items.append(s[2:])
        else:
            if items: flush()
            para.append(s)
            # The version line right under the title.
            if first_para and s.startswith("**Version"):
                out.append(f'<p class="version">{inline(s)}</p>'); para.clear()
            first_para = False
    flush()
    return "\n".join(out)


def legal(name, title, description):
    md = open(os.path.join(HERE, "src", f"{name}.md"), encoding="utf-8").read()
    body = f'<main class="doc">\n{markdown(md)}\n</main>'
    return page(f"{title} · CapExplorer", description, body, "../", name)


def write(path, text):
    full = os.path.join(HERE, path)
    os.makedirs(os.path.dirname(full) or HERE, exist_ok=True)
    open(full, "w", encoding="utf-8").write(text)


if __name__ == "__main__":
    write("index.html", home())
    write("privacy/index.html", legal("privacy", "Privacy Policy", "How CapExplorer handles information: it collects none."))
    write("terms/index.html", legal("terms", "Terms of Use", "The terms for using the CapExplorer app."))
    write(".nojekyll", "")
    print("built index.html, privacy/, terms/")
