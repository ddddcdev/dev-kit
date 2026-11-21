"""Build the sample site: content/**/*.md -> dist/**/*.html with Python-Markdown and Jinja.

Top-level directories under content/ become tabs; the pages in a tab make the left navigation.
Links are relative, so dist/ also opens from the file system. A relative link to a .md
(`[x](guide/writing.md#tables)`) is rewritten to .html, so the sources link correctly in an editor too.
This holds when the page is not in this build (a warning says so); links above content/ are left as is.
"""

import shutil
import tomllib
import xml.etree.ElementTree as etree
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlsplit, urlunsplit

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from pymdownx.superfences import fence_code_format

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
DIST = ROOT / "dist"

# The same set and options as the Zensical site's mkdocs.yml, plus pymdownx.details.
EXTENSIONS = [
    "admonition",
    "attr_list",
    "md_in_html",
    "tables",
    "toc",
    "pymdownx.details",
    "pymdownx.highlight",
    "pymdownx.superfences",
]
EXTENSION_CONFIGS: dict[str, dict[str, Any]] = {
    "toc": {"permalink": True},
    "pymdownx.superfences": {
        "custom_fences": [{"name": "mermaid", "class": "mermaid", "format": fence_code_format}],
    },
}


@dataclass
class Page:
    src: Path
    url: PurePosixPath  # site-relative output path, e.g. guide/setup.html
    title: str = ""
    body: str = ""
    toc: list[dict[str, Any]] = field(default_factory=list)

    @property
    def section(self) -> str:
        return self.url.parts[0] if len(self.url.parts) > 1 else ""


class MdLinks(Treeprocessor):
    """Point relative .md links at the .html built from them."""

    def __init__(self, md: markdown.Markdown, page: Page, sources: set[PurePosixPath]) -> None:
        super().__init__(md)
        self.page = page
        self.sources = sources

    def run(self, root: etree.Element) -> None:
        for a in root.iter("a"):
            href = a.get("href", "")
            parts = urlsplit(href)
            if parts.scheme or parts.netloc or href.startswith("/") or not parts.path.endswith(".md"):
                continue
            target = resolve(self.page.url.parent, parts.path)
            where = self.page.src.relative_to(ROOT)
            if target is None:
                print(f"warning: {where}: link {href} points outside content/, left as is")
                continue
            if target not in self.sources:
                # Still rewritten: another build may put the page at the same relative path.
                print(f"warning: {where}: link {href} has no page in this build, rewritten to .html")
            a.set("href", urlunsplit(parts._replace(path=parts.path[: -len(".md")] + ".html")))


class MdLinksExtension(Extension):
    def __init__(self, page: Page, sources: set[PurePosixPath]) -> None:
        super().__init__()
        self.page = page
        self.sources = sources

    def extendMarkdown(self, md: markdown.Markdown) -> None:  # noqa: N802 (Python-Markdown API)
        md.treeprocessors.register(MdLinks(md, self.page, self.sources), "md_links", 0)


def resolve(base: PurePosixPath, path: str) -> PurePosixPath | None:
    """Normalise base/path (site-relative); None if it climbs above content/."""
    parts: list[str] = []
    for part in (base / path).parts:
        if part == "..":
            if not parts:
                return None
            parts.pop()
        elif part != ".":
            parts.append(part)
    return PurePosixPath(*parts)


def render_markdown(page: Page, sources: set[PurePosixPath]) -> None:
    md = markdown.Markdown(
        extensions=[*EXTENSIONS, MdLinksExtension(page, sources)], extension_configs=EXTENSION_CONFIGS
    )
    page.body = md.convert(page.src.read_text(encoding="utf-8"))
    tokens: list[dict[str, Any]] = getattr(md, "toc_tokens", [])
    # The page title is the h1; "On this page" lists what sits under it.
    if len(tokens) == 1 and tokens[0]["level"] == 1:
        page.title = tokens[0]["name"]
        page.toc = tokens[0]["children"]
    else:
        page.title = page.src.stem.replace("-", " ").capitalize()
        page.toc = tokens


def relative(from_url: PurePosixPath, to: str) -> str:
    depth = len(from_url.parts) - 1
    return "../" * depth + to


def collect_pages() -> list[Page]:
    pages = []
    for src in sorted(CONTENT.rglob("*.md")):
        rel = src.relative_to(CONTENT).with_suffix(".html")
        pages.append(Page(src=src, url=PurePosixPath(rel.as_posix())))
    # index first within each section
    pages.sort(key=lambda p: (p.section, p.url.name != "index.html", str(p.url)))
    return pages


def main() -> None:
    site = tomllib.loads((ROOT / "site.toml").read_text(encoding="utf-8"))
    pages = collect_pages()
    sources = {PurePosixPath(p.src.relative_to(CONTENT).as_posix()) for p in pages}
    for page in pages:
        render_markdown(page, sources)

    sections = sorted({p.section for p in pages}, key=lambda s: (s != "", s))
    titles = site.get("sections", {})
    env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=select_autoescape())

    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(ROOT / "static", DIST / "static")

    for page in pages:
        first = {s: next(p for p in pages if p.section == s) for s in sections}
        tabs = [
            {
                "title": titles.get(s, "Home") if s else "Home",
                "href": relative(page.url, str(first[s].url)),
                "active": s == page.section,
            }
            for s in sections
        ]
        nav = [
            {"title": p.title, "href": relative(page.url, str(p.url)), "active": p is page}
            for p in pages
            if p.section == page.section
        ]
        crumbs = [{"title": "Home", "href": relative(page.url, "index.html")}]
        if page.section:
            crumbs.append(
                {"title": titles.get(page.section, page.section), "href": tabs[sections.index(page.section)]["href"]}
            )
        html = env.get_template("page.html").render(
            site=site,
            page=page,
            tabs=tabs,
            nav=nav,
            nav_title=next(t["title"] for t in tabs if t["active"]),
            crumbs=crumbs,
            static=relative(page.url, "static"),
            home=relative(page.url, "index.html"),
        )
        out = DIST / page.url
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        print(f"built {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
