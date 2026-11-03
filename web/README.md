# Web UI standard

React single-page app with a derived dark theme. One gate: **`npm run check`** (prettier check,
oxlint, `tsc -b`, `vite build`).

## Stack

| purpose | tool |
|---|---|
| build, dev server | Vite |
| UI | React, TypeScript |
| styling | Tailwind CSS v4 |
| components | shadcn/ui on Base UI (style `base-nova`), icons lucide |
| lint / format | oxlint (`--deny-warnings`) / prettier (+ tailwind class sorting) |
| fonts | self-hosted fontsource: Inter (text), Geist (headings), Geist Mono (navigation, keywords), JetBrains Mono (code), BIZ UDPGothic (Japanese fallback for all) |
| agent gate on edit | Claude Code `PostToolUse` hook: prettier on every edited file, oxlint on `.ts`/`.tsx`; leftover errors go back to the agent |

The UI talks to a separate API. Use Next.js only when static export or server rendering is required.
Add vitest when there is logic worth unit-testing; verify UI in a headless browser (Playwright).

## Template

`template/` is a working app (`sample-web`) with one sample page that shows every building block
on the theme. It passes `npm run check` as is.

```bash
NAME=my-app
cp -R ~/repo/dev-kit/web/template ~/repo/$NAME
cp ~/repo/dev-kit/agent/templates/AGENTS.md ~/repo/dev-kit/agent/templates/CLAUDE.md ~/repo/$NAME/
cd ~/repo/$NAME
sed -i.bak "s/sample-web/$NAME/g" package.json index.html README.md && rm -f *.bak
git init && npm install && npm run check
npm run dev        # http://localhost:5173
```

Then replace `src/App.tsx` with the real app, fill in `AGENTS.md`, and raise dependencies to the
latest releases (`npx npm-check-updates -u && npm install`) before the first commit.

More components: `npx shadcn@latest add <name>`. After adding, check the component against the
theme rules below; keep the changes noted under "Components".

## Theme (`src/theme.css`)

Every shadcn token is derived from five parameters on `:root`:

| parameter | meaning | default |
|---|---|---|
| `--theme-hue` | background hue (OKLCH) | 255 (slate) |
| `--theme-chroma` | background chroma multiplier (0 = grey) | 0.5 |
| `--theme-accent-hue` | accent hue (OKLCH) | 70 (amber, the complement) |
| `--theme-accent-strength` | 0–1, text white mixed toward the vivid accent | 0.9 |
| `--radius` | corner radius | 0.5rem |

Keep the accent roughly opposite the background hue (about 180° apart), or set `--theme-chroma: 0`
for a grey background with one accent. Change the parameters, not the tokens. Dark only (`<html class="dark">`).

Rules carried by the theme:

- Buttons never move on press; a press is the accent fill. `default` is a light fill with dark text,
  `secondary` barely lifts from the background, `outline` is link-coloured, `ghost` is text only.
- Text fields are recessed: the field colour as fill and border, a 1px accent border on focus, no
  outer ring. Invalid fields turn border and text to `--destructive`.
- Selected toggles: accent border and text over a 10% accent fill.
- Code: fixed neutral dark (`#1a1c24`), mono font.
- Text selection: accent fill, dark text.

Font roles: plain text is the sans, `h1`–`h4` take the heading face, `code` / `pre` the mono,
`text-keyword` (Geist Mono) for navigation / commands / IDs, `text-label` for small uppercase section kickers.

## Components

Changes from the shadcn originals (keep them when re-adding):

- `button.tsx`: no `active:translate-y-px`; adds `data-button` and `data-variant` (overlay triggers
  rendered as a Button overwrite `data-slot`, so the theme targets `data-button`).
- `select.tsx`: the list opens below the trigger, right-aligned (`align = "end"`,
  `alignItemWithTrigger = false`).

The theme, fonts and component rules are personal preferences (see the dev-kit README).
