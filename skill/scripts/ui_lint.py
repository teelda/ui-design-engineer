#!/usr/bin/env python3
"""Find specific UI source patterns that deserve a human design or accessibility check."""

import argparse
import re
from pathlib import Path

EXTENSIONS = {".html", ".css", ".scss", ".jsx", ".tsx"}
EXCLUDED_DIRS = {".git", ".next", "build", "coverage", "dist", "node_modules", "vendor"}
HEX = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
BLOCK = re.compile(r"([^{}]+)\{([^{}]+)\}", re.S)
DECL = re.compile(r"([\w-]+)\s*:\s*([^;]+)")
FIELD = re.compile(r"<(input|textarea)\b[^>]*\bplaceholder\s*=\s*(?:['\"][^'\"]*['\"]|\{[^}]+\})[^>]*>", re.I | re.S)
COMMENT = re.compile(r"/\*.*?\*/|^[ \t]*//[^\n]*", re.S | re.M)
SUPPRESSION = re.compile(r"ui-lint:\s*ok\s+([a-z-]+)\s*(?:--|—)\s*(\S.{2,})", re.I)


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


def suppressed(lines, line, kind):
    # A reasoned comment on the finding's line or the preceding line records the design decision.
    for candidate in (line - 1, line - 2):
        if candidate < 0:
            continue
        match = SUPPRESSION.search(lines[candidate])
        if match and match.group(1).lower() == kind and ("/*" in lines[candidate] or "//" in lines[candidate]):
            return True
    return False


def inspect(path: Path):
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
        labelled_ids = set(re.findall(r"<label\b[^>]*\b(?:for|htmlFor)\s*=\s*['\"]([^'\"]+)['\"]", clean, re.I))
        element_ids = set(re.findall(r"\bid\s*=\s*['\"]([^'\"]+)['\"]", clean))
        wrapping_labels = [match.span() for match in re.finditer(r"<label\b[^>]*>.*?</label\s*>", clean, re.I | re.S)]
        for match in FIELD.finditer(clean):
            tag = match.group(0)
            if any(start <= match.start() < end for start, end in wrapping_labels):
                continue
            field_id = re.search(r"\bid\s*=\s*['\"]([^'\"]+)['\"]", tag)
            if field_id and field_id.group(1) in labelled_ids:
                continue
            aria_label = re.search(r"\baria-label\s*=\s*(['\"])(.*?)\1", tag, re.I | re.S)
            if aria_label and aria_label.group(2).strip():
                continue
            labelledby = re.search(r"\baria-labelledby\s*=\s*(['\"])(.*?)\1", tag, re.I | re.S)
            if labelledby:
                refs = labelledby.group(2).split()
                if refs and all(ref in element_ids for ref in refs):
                    continue
                flag(match.start(), "label-unresolved", "aria-labelledby references an ID not found in this file")
                continue
            if re.search(r"\baria-(?:label|labelledby)\s*=\s*\{", tag, re.I):
                flag(match.start(), "label-unresolved", "dynamic ARIA name needs a rendered check")
                continue
            flag(match.start(), "placeholder-label", "verify a persistent label; placeholder alone is insufficient")

    for block in BLOCK.finditer(clean):
        declarations = {key.lower(): value.strip() for key, value in DECL.findall(block.group(2))}
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
            flag(block.start(), "contrast", f"same-rule solid colors {ratio:.2f}:1 below {threshold}:1; verify rendered text")
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
    args = parser.parse_args()
    try:
        files = collect_files(args.paths, args.allow_empty)
    except ValueError as error:
        parser.error(str(error))
    count = 0
    for file in files:
        for line, kind, detail in inspect(file):
            print(f"{file}:{line}: {kind}: {detail}")
            count += 1
    print(f"{count} review candidate(s) in {len(files)} file(s). Check rendered behavior separately.")
    return 1 if args.strict and count else 0


if __name__ == "__main__":
    raise SystemExit(main())
