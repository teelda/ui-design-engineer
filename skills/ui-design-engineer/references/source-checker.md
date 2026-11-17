# Source checker coverage

Run the script by absolute path, resolved from the installed `SKILL.md`. Pass application files or directories. It scans `.html`, `.css`, `.scss`, `.jsx`, and `.tsx`; recursive directory scans skip `.git`, `.next`, `build`, `coverage`, `dist`, `node_modules`, and `vendor`. A missing path, unsupported file, or directory with no supported files is an error. `--allow-empty` permits an existing empty input; `--strict` returns exit 1 when candidates are found.

| Check | Recognizes | Does not establish |
|---|---|---|
| Gradient | CSS `linear/radial/conic-gradient(...)` and Tailwind `bg-gradient-to-*` or `bg-linear-to-*` | Whether the gradient is appropriate or legible |
| Motion and focus | `transition-all`, `transition: all`, `outline: none/0`, `outline-none` | Computed focus styles or reduced-motion behavior |
| Field names | Literal or JSX-expression `placeholder`, nonempty static label `for`/`htmlFor`, wrapping label text, static `aria-label` and `aria-labelledby` IDs in the same file | Names supplied by components, runtime IDs, or the accessibility tree; dynamic ARIA names are flagged unresolved |
| Contrast | Same-rule solid 3/6-digit hex `color` and `background`/`background-color`, with px/pt font size and literal weight | Variables, inheritance, gradients, Tailwind utility colors, RGB/HSL/named colors, overlays, or rendered contrast |

## House profile (opt-in)

`--profile house` adds the mechanical part of the [house bar](house-bar.md). Use it only when the user opts into that preference profile; its candidates are style choices, not usability or accessibility defects. Pass one project at a time, because palette tokens are collected across every scanned file. Spacing and colour candidates are grouped: each distinct off-scale value or off-palette colour is reported once per file, at its first use, with a use count. A reasoned suppression on that first use covers the group.

| Check | Recognizes | Does not establish |
|---|---|---|
| `radius-mix` | A pill radius (≥999px or Tailwind `rounded-full`) in the same file as smaller radii, or more than three distinct small radii. `50%` circles are ignored. | Whether the radii belong to different component roles in the design system |
| `uppercase` | `text-transform: uppercase` and the Tailwind `uppercase` class | Acronyms or uppercase text typed in the copy itself |
| `off-scale-spacing` | `margin`, `padding` and `gap` lengths off the 4px grid, or off `--spacing-scale 4,8,16,24,48`. `rem`/`em` count as 16px; `var()` and `calc()` are skipped. | Spacing set through components, utilities or inline styles |
| `off-token-color` | Hex colours outside custom-property definitions that match no `--name: #hex` token in the scanned files, including literal fallbacks such as `var(--brand, #f00)`. `url(#id)` fragments are ignored. Skipped, with a note, when no tokens exist. | Tokens defined in JS, Tailwind config or non-hex formats |
| `glow` | Any `text-shadow`, a `box-shadow` blur of 24px or more, and `drop-shadow()` filters | Whether the live product already uses the effect |

CSS/SCSS block and `//` comments and HTML comments are ignored. A candidate can be suppressed with a reason on its line or the preceding line: `/* ui-lint: ok gradient -- approved brand hero */`. Supported kinds are `gradient`, `transition-all`, `outline-removed`, `placeholder-label`, `label-unresolved`, `contrast`, and the house-profile kinds `radius-mix`, `uppercase`, `off-scale-spacing`, `off-token-color` and `glow`. A suppression records a reviewed decision; it does not turn the source scan into accessibility evidence.
