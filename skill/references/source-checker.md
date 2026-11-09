# Source checker coverage

Run the script by absolute path, resolved from the installed `SKILL.md`. Pass application files or directories. It scans `.html`, `.css`, `.scss`, `.jsx`, and `.tsx`; recursive directory scans skip `.git`, `.next`, `build`, `coverage`, `dist`, `node_modules`, and `vendor`. A missing path, unsupported file, or directory with no supported files is an error. `--allow-empty` permits an existing empty input; `--strict` returns exit 1 when candidates are found.

| Check | Recognizes | Does not establish |
|---|---|---|
| Gradient | CSS `linear/radial/conic-gradient(...)` and Tailwind `bg-gradient-to-*` or `bg-linear-to-*` | Whether the gradient is appropriate or legible |
| Motion and focus | `transition-all`, `transition: all`, `outline: none/0`, `outline-none` | Computed focus styles or reduced-motion behavior |
| Field names | Literal or JSX-expression `placeholder`, nonempty static label `for`/`htmlFor`, wrapping label text, static `aria-label` and `aria-labelledby` IDs in the same file | Names supplied by components, runtime IDs, or the accessibility tree; dynamic ARIA names are flagged unresolved |
| Contrast | Same-rule solid 3/6-digit hex `color` and `background`/`background-color`, with px/pt font size and literal weight | Variables, inheritance, gradients, Tailwind utility colors, RGB/HSL/named colors, overlays, or rendered contrast |

CSS/SCSS block and `//` comments and HTML comments are ignored. A candidate can be suppressed with a reason on its line or the preceding line: `/* ui-lint: ok gradient -- approved brand hero */`. Supported kinds are `gradient`, `transition-all`, `outline-removed`, `placeholder-label`, `label-unresolved`, and `contrast`. A suppression records a reviewed decision; it does not turn the source scan into accessibility evidence.
