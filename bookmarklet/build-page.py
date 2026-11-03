"""Build index.html (drag-to-install page) from setup.md. Run after editing setup.md:
    python3 bookmarklet/build-page.py
"""

import html
import re
from pathlib import Path

here = Path(__file__).parent
md = (here / "setup.md").read_text()

items = []  # (section, name, description, code)
section = ""
for block in re.split(r"^### ", md, flags=re.M)[1:]:
    head, _, rest = block.partition("\n")
    before = md[: md.index("### " + block)]
    sections = re.findall(r"^## (.+)$", before, flags=re.M)
    section = sections[-1] if sections else ""
    code = re.search(r"```js\n(.*?)```", rest, re.S)
    desc = rest[: code.start()].strip() if code else ""
    if code and code.group(1).strip():
        items.append((section, head.strip(), desc, code.group(1).strip()))

rows = []
current = None
for section, name, desc, code in items:
    if section != current:
        rows.append(f"<h2>{html.escape(section)}</h2>")
        current = section
    rows.append(
        f'<div class="row"><a class="bm" href="{html.escape(code, quote=True)}">{html.escape(name)}</a>'
        f"<p>{html.escape(desc.replace(chr(96), ''))}</p></div>"
    )

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bookmarklets</title>
<!-- Generated from setup.md by build-page.py. Do not edit by hand. -->
<style>
:root {{ color-scheme: dark; --bg: #1e2430; --fg: #f0f0f0; --muted: #a6adbb; --accent: #f0a030; --chip: #2b3342; }}
body {{ margin: 0; background: var(--bg); color: var(--fg); font: 15px/1.6 system-ui, sans-serif; }}
main {{ max-width: 720px; margin: 0 auto; padding: 24px 16px; }}
h1 {{ font-size: 1.4rem; margin: 0 0 4px; }}
h2 {{ font-size: 1.05rem; margin: 28px 0 8px; color: var(--muted); }}
.row {{ display: flex; gap: 16px; align-items: baseline; padding: 8px 0; border-top: 1px solid #ffffff1a; }}
.bm {{ flex: none; min-width: 9em; padding: 4px 12px; border-radius: 6px; background: var(--chip);
      color: var(--accent); text-decoration: none; cursor: grab; border: 1px solid #ffffff2a; }}
.row p {{ margin: 0; color: var(--muted); font-size: 0.9rem; }}
.note {{ color: var(--muted); }}
</style>
</head>
<body>
<main>
<h1>Bookmarklets</h1>
<p class="note">Drag a button to the bookmarks bar (show it with Ctrl/Cmd+Shift+B). Code and notes: setup.md.</p>
{chr(10).join(rows)}
</main>
</body>
</html>
"""
(here / "index.html").write_text(page)
print(f"index.html: {len(items)} bookmarklets")
