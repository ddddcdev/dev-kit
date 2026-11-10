// The few behaviours of the theme that need script. Everything else (drawer,
// floating "On this page", details) is CSS only. Search is not reproduced.

const header = document.querySelector(".site-header");
const toTop = document.querySelector(".to-top");

// Header shadow and the back-to-top button follow the scroll position.
let lastY = window.scrollY;
const onScroll = () => {
  const y = window.scrollY;
  header?.classList.toggle("is-scrolled", y > 0);
  // Shown while scrolling up, past the first screen (as Zensical's navigation.top).
  toTop?.classList.toggle("is-visible", y < lastY && y > window.innerHeight);
  lastY = y;
};
window.addEventListener("scroll", onScroll, { passive: true });
toTop?.addEventListener("click", () => window.scrollTo({ top: 0 }));

// Copy button on every highlighted code block.
const copyIcon =
  '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><rect width="14" height="14" x="8" y="8" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>';
for (const block of document.querySelectorAll(".prose .highlight")) {
  const code = block.querySelector("pre > code");
  if (!code) continue;
  const button = document.createElement("button");
  button.type = "button";
  button.className = "copy-button";
  button.title = "Copy to clipboard";
  button.innerHTML = copyIcon;
  button.addEventListener("click", async () => {
    await navigator.clipboard.writeText(code.innerText.replace(/\n$/, ""));
    button.classList.add("is-done");
    setTimeout(() => button.classList.remove("is-done"), 1500);
  });
  block.append(button);
}

// "On this page": mark the heading the reader is in.
const tocLinks = [...document.querySelectorAll(".toc a.nav__link")];
const headings = tocLinks
  .map((a) => document.getElementById(decodeURIComponent(a.hash.slice(1))))
  .filter((h) => h !== null);
const markActive = () => {
  const offset = (header?.offsetHeight ?? 0) + 16;
  let current = headings[0]?.id;
  for (const h of headings) {
    if (h.getBoundingClientRect().top - offset <= 0) current = h.id;
  }
  for (const a of tocLinks) {
    a.classList.toggle("is-active", decodeURIComponent(a.hash.slice(1)) === current);
  }
};
if (headings.length) {
  window.addEventListener("scroll", markActive, { passive: true });
  markActive();
}

// Close the drawer and the floating table of contents after a jump.
for (const a of document.querySelectorAll(".sidebar--primary a, .toc-float a")) {
  a.addEventListener("click", () => {
    const toggle = document.getElementById("drawer");
    if (toggle) toggle.checked = false;
    document.querySelector(".toc-float")?.removeAttribute("open");
  });
}
