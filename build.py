#!/usr/bin/env python3
"""Build evaldriven.org: README.md + stargazers → static HTML site."""

import json
import re
import subprocess
import sys
import html as html_mod
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
OUTPUT = ROOT / "output"
README = ROOT / "README.md"

# Site metadata (not in README so GitHub renders it clean)
SITE = {
    "title": "Eval-Driven Development",
    "description": "A manifesto for evaluation-driven AI development. Why every AI system needs deterministic, automated evaluation as a first-class engineering practice.",
    "author": "Grey Newell",
    "base_url": "https://evaldriven.org",
    "repo": "greynewell/evaldriven.org",
    "keywords": [
        "eval-driven development", "AI evaluation", "LLM evaluation",
        "model evaluation", "evaluation engineering", "CI/CD for LLMs",
        "deterministic testing", "AI quality assurance",
    ],
}


def md_to_html(md):
    """Convert markdown to HTML."""
    lines = md.split("\n")
    out = []
    in_ul = False
    in_ol = False
    in_code = False
    code_lines = []

    for line in lines:
        if line.startswith("```"):
            if in_code:
                out.append("<pre><code>" + html_mod.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines = []
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue

        # Close lists if needed
        if in_ul and not re.match(r"^[-*] ", line):
            out.append("</ul>")
            in_ul = False
        if in_ol and not re.match(r"^\d+\. ", line):
            out.append("</ol>")
            in_ol = False

        # Headings
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            level = len(m.group(1))
            text = m.group(2)
            slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
            out.append(f'<h{level} id="{slug}">{inline(text)}</h{level}>')
            continue

        # Horizontal rule
        if re.match(r"^---+\s*$", line):
            out.append("<hr>")
            continue

        # Unordered list items
        m = re.match(r"^[-*] (.*)", line)
        if m:
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline(m.group(1))}</li>")
            continue

        # Ordered list items
        m = re.match(r"^\d+\. (.*)", line)
        if m:
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{inline(m.group(1))}</li>")
            continue

        # Blockquote
        if line.startswith("> "):
            out.append(f"<blockquote><p>{inline(line[2:])}</p></blockquote>")
            continue

        # Empty line
        if not line.strip():
            out.append("")
            continue

        # Paragraph
        out.append(f"<p>{inline(line)}</p>")

    if in_ul:
        out.append("</ul>")
    if in_ol:
        out.append("</ol>")

    return "\n".join(out)


def inline(text):
    """Process inline markdown formatting."""
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def fetch_stargazers():
    """Fetch all stargazers via gh CLI."""
    users = []
    page = 1
    while True:
        try:
            result = subprocess.run(
                ["gh", "api",
                 f"repos/{SITE['repo']}/stargazers?per_page=100&page={page}",
                 "--jq", ".[].login"],
                capture_output=True, text=True, timeout=30
            )
            batch = result.stdout.strip()
            if not batch:
                break
            users.extend(batch.split("\n"))
            page += 1
        except Exception:
            break
    return users


def build_signatories_html(users):
    """Build the signatories section."""
    repo_url = f"https://github.com/{SITE['repo']}"
    h = '<h2 id="signatories">Signatories</h2>\n'
    h += f'<p><a href="{repo_url}">Star this repo</a> to sign the manifesto.</p>\n'
    if users:
        h += "<ul>\n"
        for login in users:
            if login.strip():
                h += f'<li><a href="https://github.com/{login}">{login}</a></li>\n'
        h += "</ul>\n"
    else:
        h += "<p><em>Be the first to sign.</em></p>\n"
    return h


def build_page(body_html, signatories_html):
    """Generate the full HTML page."""
    title = SITE["title"]
    desc = SITE["description"]
    author = SITE["author"]
    base = SITE["base_url"]
    now = datetime.now().strftime("%Y-%m-%d")

    json_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc,
        "author": {"@type": "Person", "name": author, "url": "https://greynewell.com"},
        "publisher": {"@type": "Person", "name": author, "url": "https://greynewell.com"},
        "url": base,
        "datePublished": "2026-02-15",
        "dateModified": now,
        "mainEntityOfPage": {"@type": "WebPage", "@id": base},
        "keywords": SITE["keywords"],
    })

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="{author}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{base}/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{title}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<link rel="canonical" href="{base}/">
<meta name="robots" content="index, follow">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ctext x='4' y='26' font-size='28' font-family='monospace'%3E%E2%9C%93%3C/text%3E%3C/svg%3E">
<script type="application/ld+json">{json_ld}</script>
<style>
*, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'Courier New', Courier, monospace; max-width: 650px; margin: 40px auto; padding: 0 20px; line-height: 1.6; background: #fff; color: #111; font-size: 16px; }}
h1, h2, h3 {{ font-family: 'Courier New', Courier, monospace; font-weight: 700; color: #000; }}
h1 {{ font-size: 1.5rem; margin: 0 0 1rem; text-transform: uppercase; letter-spacing: 0.05em; }}
h2 {{ font-size: 1.125rem; margin: 2rem 0 0.75rem; text-transform: uppercase; letter-spacing: 0.03em; border-bottom: 1px solid #000; padding-bottom: 0.25rem; }}
h3 {{ font-size: 1rem; margin: 1.5rem 0 0.5rem; }}
p {{ margin: 0.75rem 0; }}
ul, ol {{ padding-left: 1.5rem; margin: 0.75rem 0; }}
li {{ margin: 0.3rem 0; }}
a {{ color: #111; text-decoration: underline; }}
a:hover {{ color: #555; }}
code {{ font-family: 'Courier New', Courier, monospace; font-size: 0.9em; background: #f5f5f5; padding: 0.1em 0.3em; }}
pre {{ background: #f5f5f5; border: 1px solid #ddd; padding: 1rem; overflow-x: auto; margin: 1rem 0; line-height: 1.4; }}
pre code {{ background: none; padding: 0; font-size: 0.875rem; }}
blockquote {{ border-left: 3px solid #111; padding: 0.5rem 1rem; margin: 1rem 0; color: #333; }}
hr {{ border: none; border-top: 1px solid #111; margin: 2rem 0; }}
header {{ display: flex; align-items: baseline; justify-content: space-between; padding: 0 0 1rem; border-bottom: 2px solid #000; margin-bottom: 2rem; }}
header .brand {{ font-weight: 700; font-size: 0.875rem; color: #000; text-decoration: none; text-transform: uppercase; letter-spacing: 0.08em; }}
header nav {{ display: flex; gap: 1rem; }}
header nav a {{ font-size: 0.8125rem; color: #555; text-decoration: none; text-transform: uppercase; letter-spacing: 0.05em; }}
header nav a:hover {{ color: #000; }}
footer {{ margin-top: 3rem; padding-top: 1rem; border-top: 2px solid #000; text-align: center; font-size: 0.75rem; color: #777; }}
footer a {{ color: #555; text-decoration: none; text-transform: uppercase; letter-spacing: 0.05em; }}
footer a:hover {{ color: #000; }}
@media (max-width: 640px) {{ body {{ margin: 20px auto; padding: 0 15px; }} header {{ flex-direction: column; gap: 0.5rem; }} footer {{ flex-direction: column; }} }}
</style>
</head>
<body>
<header>
  <a href="/" class="brand">evaldriven.org</a>
  <nav>
    <a href="https://github.com/{SITE['repo']}">source</a>
  </nav>
</header>
<main>
  <article>
    {body_html}
    {signatories_html}
  </article>
</main>
<footer>
  <a href="https://creativecommons.org/publicdomain/zero/1.0/">CC0</a> · <a href="/sitemap.xml">sitemap</a> · <a href="/llms.txt">llms.txt</a> · <a href="https://github.com/{SITE['repo']}">source</a>
</footer>
</body>
</html>"""


def main():
    readme_text = README.read_text()

    # Strip frontmatter if present (for backwards compat)
    if readme_text.startswith("---"):
        end = readme_text.index("---", 3)
        readme_text = readme_text[end + 3:].strip()

    print("Fetching stargazers...", file=sys.stderr)
    users = fetch_stargazers()
    print(f"  Found {len(users)} stargazers", file=sys.stderr)

    body_html = md_to_html(readme_text)
    signatories_html = build_signatories_html(users)

    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "index.html").write_text(build_page(body_html, signatories_html))
    (OUTPUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'<url><loc>{SITE["base_url"]}/</loc><priority>1.0</priority>'
        f'<changefreq>weekly</changefreq></url>\n</urlset>'
    )
    (OUTPUT / "robots.txt").write_text(
        f'User-agent: *\nAllow: /\n\n'
        f'User-agent: GPTBot\nAllow: /\n\n'
        f'User-agent: ClaudeBot\nAllow: /\n\n'
        f'User-agent: PerplexityBot\nAllow: /\n\n'
        f'Sitemap: {SITE["base_url"]}/sitemap.xml\n'
    )
    (OUTPUT / "llms.txt").write_text(
        f'# {SITE["title"]}\n\n'
        f'> {SITE["description"]}\n\n'
        f'## Author\n- [{SITE["author"]}](https://greynewell.com)\n\n'
        f'## Source\n- [GitHub](https://github.com/{SITE["repo"]})\n'
    )
    (OUTPUT / "CNAME").write_text("evaldriven.org\n")

    print("Build complete!", file=sys.stderr)
    for f in sorted(OUTPUT.iterdir()):
        if f.is_file():
            print(f"  {f.name} ({f.stat().st_size} bytes)", file=sys.stderr)


if __name__ == "__main__":
    main()
