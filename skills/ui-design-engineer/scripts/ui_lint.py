#!/usr/bin/env python3
"""Find specific UI source patterns that deserve a human design or accessibility check."""

import argparse
import re
from pathlib import Path

EXTENSIONS = {".html", ".css", ".scss", ".jsx", ".tsx"}
EXCLUDED_DIRS = {".git", ".next", "build", "coverage", "dist", "node_modules", "vendor"}
HEX = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
BLOCK = re.compile(r"\{([^{}]+)\}", re.S)  # declaration body only; a selector group made this quadratic on large files
DECL = re.compile(r"([\w-]+)\s*:\s*([^;]+)")
FIELD = re.compile(r"<(input|textarea)\b[^>]*\bplaceholder\s*=\s*(?:['\"][^'\"]*['\"]|\{[^}]+\})[^>]*>", re.I | re.S)
COMMENT = re.compile(r"/\*.*?\*/|<!--.*?-->|(?<!:)//[^\n]*", re.S)
SUPPRESSION = re.compile(r"ui-lint:\s*ok\s+([a-z-]+)\s*(?:--|—)\s*(\S.{2,})", re.I)
ATTRIBUTE = r"(?<![\w:-]){}\s*=\s*(['\"])(.*?)\1"
HEX_LITERAL = re.compile(r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b")
TOKEN_DEF = re.compile(r"--[\w-]+\s*:\s*(#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4}))\b")
LENGTH = re.compile(r"(?<![#\w.])(-?\d*\.?\d+)(px|rem|em|%)?(?![\w%])")
CLASS_ATTR = re.compile(r"\b(?:class|className)\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|\{[`'\"]([^`'\"]*)[`'\"]\})", re.S)
CLASS_EXPR = re.compile(r"\b(?:class|className)\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}", re.S)
SPACING = re.compile(r"^(?:margin|padding|gap|row-gap|column-gap)(?:-[a-z-]+)?$")
PILL_PX = 999


def literal_attribute(tag: str, name: str):
    return re.search(ATTRIBUTE.format(re.escape(name)), tag, re.I | re.S)


def line_number(source: str, offset: int) -> int:
    return source.count("\n", 0, offset) + 1


def without_comments(source: str) -> str:
    return COMMENT.sub(lambda match: re.sub(r"[^\n]", " ", match.group(0)), source)


def rgb(value: str):
    match = HEX.fullmatch(value.strip())
    if not match:
        return None
    digits = match.group(1)
    if len(digits) == 3:
        digits = "".join(char * 2 for char in digits)
    return tuple(int(digits[i:i + 2], 16) / 255 for i in (0, 2, 4))


def luminance(color):
    channels = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in color]
    return sum(a * b for a, b in zip(channels, (0.2126, 0.7152, 0.0722)))


def contrast(a, b):
    light, dark = sorted((luminance(a), luminance(b)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def normalize_hex(value: str) -> str:
    digits = value.lstrip("#").lower()
    if len(digits) in (3, 4):
        digits = "".join(char * 2 for char in digits)
    return "#" + digits


def color_tokens(sources):
    """Hex values defined as CSS custom properties anywhere in the scanned files."""
    return {normalize_hex(match.group(1)) for source in sources for match in TOKEN_DEF.finditer(without_comments(source))}


def px(number: str, unit: str):
    value = abs(float(number))
    if unit in ("rem", "em"):
        return value * 16
    if unit in ("px", None) or (unit == "" and value == 0):
        return value
    return None


def class_strings(clean):
    """Class lists from class/className attributes, including string literals inside {cn(...)} expressions."""
    for attr in CLASS_ATTR.finditer(clean):
        yield attr.start(), next(group for group in attr.groups() if group is not None)
    for expr in CLASS_EXPR.finditer(clean):
        for literal in re.finditer(r"[`'\"]([^`'\"]*)[`'\"]", expr.group(1)):
            yield expr.start(), literal.group(1)


def house_checks(clean, report, tokens, spacing_scale):
    """Opt-in checks for the house bar: radius language, case, spacing grid, palette and glow."""
    seen = set()

    def flag(offset, kind, detail):
        if (offset, kind, detail) not in seen:
            seen.add((offset, kind, detail))
            report(offset, kind, detail)

    for match in re.finditer(r"text-transform\s*:\s*uppercase\b", clean, re.I):
        flag(match.start(), "uppercase", "use sentence case; keep acronyms capitalised")
    for offset, classes in class_strings(clean):
        if re.search(r"(?<![\w-])uppercase(?![\w-])", classes):
            flag(offset, "uppercase", "use sentence case; keep acronyms capitalised")

    pills, radii = [], {}
    spacing_hits, colour_hits = {}, {}  # one candidate per distinct value per file: [first offset, label, uses]
    for block in BLOCK.finditer(clean):
        for decl in DECL.finditer(block.group(1)):
            name, value = decl.group(1).lower(), decl.group(2).strip()
            offset = block.start(1) + decl.start()
            if name.startswith("--"):
                continue
            # Variable or computed lengths cannot be judged from source; colour fallbacks inside var() still can.
            numeric = "var(" not in value and "calc(" not in value
            if numeric and (name == "border-radius" or re.fullmatch(r"border-[a-z-]+-radius", name)):
                for number, unit in LENGTH.findall(value):
                    size = px(number, unit or None)
                    if unit == "%" or size is None or size == 0:
                        continue
                    if size >= PILL_PX:
                        pills.append(offset)
                    else:
                        radii.setdefault(round(size, 2), offset)
            elif numeric and SPACING.match(name):
                for number, unit in LENGTH.findall(value):
                    size = px(number, unit or None)
                    if size is None or size == 0:
                        continue
                    on_scale = size in spacing_scale if spacing_scale else size % 4 == 0
                    if not on_scale:
                        spacing_hits.setdefault(round(size, 2), [offset, f"{number}{unit}", 0])[2] += 1
            elif name in ("text-shadow",) and value.lower() != "none":
                flag(offset, "glow", "decorative text shadow; keep only if the live product uses it")
            elif name == "box-shadow" and value.lower() != "none":
                for layer in re.sub(r"[\w-]+\([^)]*\)|#[0-9a-fA-F]+", " ", value).split(","):
                    lengths = [px(n, u or None) for n, u in LENGTH.findall(layer)]
                    if len(lengths) >= 3 and lengths[2] is not None and lengths[2] >= 24:
                        flag(offset, "glow", "large blurred shadow; keep only if the live product uses it")
            elif name in ("filter", "backdrop-filter") and "drop-shadow(" in value:
                flag(offset, "glow", "drop-shadow filter; keep only if the live product uses it")
            if tokens:
                # url(#id) is an SVG fragment reference, not a colour.
                for hex_match in HEX_LITERAL.finditer(re.sub(r"url\([^)]*\)", " ", value, flags=re.I)):
                    colour = normalize_hex(hex_match.group(0))
                    if colour not in tokens:
                        colour_hits.setdefault(colour, [offset, hex_match.group(0), 0])[2] += 1
    scale_name = "declared scale" if spacing_scale else "4px grid"
    for offset, label, uses in spacing_hits.values():
        flag(offset, "off-scale-spacing", f"{label} is off the {scale_name} ({uses} use{'s' if uses > 1 else ''} in this file)")
    for offset, label, uses in colour_hits.values():
        flag(offset, "off-token-color", f"{label} is not a defined colour token ({uses} use{'s' if uses > 1 else ''} in this file)")
    for offset, classes in class_strings(clean):
        for name in classes.split():
            if name == "rounded-full":
                pills.append(offset)
            elif re.fullmatch(r"rounded(?:-(?:sm|md|lg|xl|2xl|3xl))?", name):
                radii.setdefault(name, offset)
    if pills and radii:
        for offset in pills:
            flag(offset, "radius-mix", "pill radius next to small radii in the same file; pick one radius language")
    if len(radii) > 3:
        offset = sorted(radii.values())[3]
        flag(offset, "radius-mix", f"{len(radii)} distinct small radii; map them to a short radius scale")


def suppressed(lines, line, kind):
    # A reasoned comment on the finding's line or the preceding line records the design decision.
    for candidate in (line - 1, line - 2):
        if candidate < 0:
            continue
        match = SUPPRESSION.search(lines[candidate])
        if match and match.group(1).lower() == kind and ("/*" in lines[candidate] or "//" in lines[candidate]):
            return True
    return False


def inspect(path: Path, profile: str = "default", tokens=frozenset(), spacing_scale=None):
    source = path.read_text(encoding="utf-8")
    clean = without_comments(source)
    lines = source.splitlines()
    findings = []

    def flag(offset, kind, detail):
        line = line_number(source, offset)
        if not suppressed(lines, line, kind):
            findings.append((line, kind, detail))

    for pattern, kind, detail in (
        (r"\b(?:linear|radial|conic)-gradient\s*\(|\bbg-(?:gradient|linear)-to-[\w-]+", "gradient", "check brand purpose and text contrast across the gradient"),
        (r"\btransition-all\b|transition\s*:\s*all\b", "transition-all", "limit animation to intended properties and respect reduced motion"),
        (r"\boutline\s*:\s*(?:none|0(?:px)?)\b|\boutline-none\b", "outline-removed", "check a visible keyboard-focus replacement"),
    ):
        for match in re.finditer(pattern, clean, re.I):
            flag(match.start(), kind, detail)

    if path.suffix.lower() in {".html", ".jsx", ".tsx"}:
        labelled_ids = set()
        wrapping_labels = []
        for label in re.finditer(r"<label\b([^>]*)>(.*?)</label\s*>", clean, re.I | re.S):
            label_text = re.sub(r"<[^>]+>", "", label.group(2)).strip()
            name = literal_attribute(label.group(1), "for") or literal_attribute(label.group(1), "htmlFor")
            if name and label_text:
                labelled_ids.add(name.group(2))
            wrapping_labels.append((label.start(), label.end(), label_text))
        element_ids = {name.group(2) for tag in re.finditer(r"<[A-Za-z][^>]*>", clean)
                       for name in [literal_attribute(tag.group(0), "id")] if name}
        for match in FIELD.finditer(clean):
            tag = match.group(0)
            wrapper = next((text for start, end, text in wrapping_labels if start <= match.start() < end), None)
            if wrapper:
                continue
            if wrapper == "":
                flag(match.start(), "label-unresolved", "wrapping label has no text in this file")
                continue
            field_id = literal_attribute(tag, "id")
            if field_id and field_id.group(2) in labelled_ids:
                continue
            aria_label = literal_attribute(tag, "aria-label")
            if aria_label and aria_label.group(2).strip():
                continue
            labelledby = literal_attribute(tag, "aria-labelledby")
            if labelledby:
                refs = labelledby.group(2).split()
                if refs and all(ref in element_ids for ref in refs):
                    continue
                flag(match.start(), "label-unresolved", "aria-labelledby references an ID not found in this file")
                continue
            if re.search(r"(?<![\w:-])aria-(?:label|labelledby)\s*=\s*\{", tag, re.I):
                flag(match.start(), "label-unresolved", "dynamic ARIA name needs a rendered check")
                continue
            flag(match.start(), "placeholder-label", "verify a persistent label; placeholder alone is insufficient")

    for block in BLOCK.finditer(clean):
        matches = list(DECL.finditer(block.group(1)))
        declarations = {match.group(1).lower(): match.group(2).strip() for match in matches}
        foreground = rgb(declarations.get("color", ""))
        background = rgb(declarations.get("background-color", declarations.get("background", "")))
        if foreground is None or background is None:
            continue
        size = re.fullmatch(r"(\d+(?:\.\d+)?)(px|pt)", declarations.get("font-size", ""))
        size_px = float(size.group(1)) * (96 / 72 if size.group(2) == "pt" else 1) if size else 0
        weight = declarations.get("font-weight", "")
        bold = weight.lower() in {"bold", "bolder"} or (weight.isdigit() and int(weight) >= 700)
        threshold = 3 if size_px >= 24 or (size_px >= 14 * 96 / 72 and bold) else 4.5
        ratio = contrast(foreground, background)
        if ratio < threshold:
            color_match = next(match for match in matches if match.group(1).lower() == "color")
            flag(block.start(1) + color_match.start(), "contrast", f"same-rule solid colors {ratio:.2f}:1 below {threshold}:1; verify rendered text")
    if profile == "house":
        house_checks(clean, flag, tokens, spacing_scale)
    return sorted(findings)


def collect_files(paths, allow_empty=False):
    files = set()
    for path in paths:
        if not path.exists():
            raise ValueError(f"input does not exist: {path}")
        if path.is_file():
            if path.suffix.lower() not in EXTENSIONS:
                raise ValueError(f"unsupported file type: {path}")
            files.add(path)
            continue
        matches = {file for file in path.rglob("*") if file.is_file()
                   and file.suffix.lower() in EXTENSIONS
                   and not any(part in EXCLUDED_DIRS for part in file.relative_to(path).parts[:-1])}
        if not matches and not allow_empty:
            raise ValueError(f"no supported UI files found in: {path}")
        files.update(matches)
    if not files and not allow_empty:
        raise ValueError("no supported UI files found")
    return sorted(files)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="UI files or directories")
    parser.add_argument("--strict", action="store_true", help="exit 1 when review candidates are found")
    parser.add_argument("--allow-empty", action="store_true", help="allow an existing directory with zero supported files")
    parser.add_argument("--profile", choices=("default", "house"), default="default",
                        help="house adds opt-in checks for the house bar: radius, case, spacing, palette, glow")
    parser.add_argument("--spacing-scale", help="comma-separated px values for --profile house (default: the 4px grid)")
    args = parser.parse_args()
    try:
        files = collect_files(args.paths, args.allow_empty)
        scale = {float(value) for value in args.spacing_scale.split(",")} if args.spacing_scale else None
    except ValueError as error:
        parser.error(str(error))
    tokens = set()
    if args.profile == "house":
        tokens = color_tokens(file.read_text(encoding="utf-8") for file in files)
        if not tokens:
            print("house: no hex colour tokens (--name: #hex) found; palette check skipped.")
    count = 0
    for file in files:
        for line, kind, detail in inspect(file, args.profile, tokens, scale):
            print(f"{file}:{line}: {kind}: {detail}")
            count += 1
    print(f"{count} review candidate(s) in {len(files)} file(s). Check rendered behavior separately.")
    return 1 if args.strict and count else 0


if __name__ == "__main__":
    raise SystemExit(main())
