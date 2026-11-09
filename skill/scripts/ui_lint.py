#!/usr/bin/env python3
"""Flag UI source candidates for manual review; never claim rendered conformance."""

import argparse
import re
from pathlib import Path

EXTENSIONS = {".html", ".css", ".scss", ".jsx", ".tsx"}
HEX = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
BLOCK = re.compile(r"([^{}]+)\{([^{}]+)\}", re.S)
DECL = re.compile(r"([\w-]+)\s*:\s*([^;]+)")
FIELD = re.compile(r"<(input|textarea)\b[^>]*\bplaceholder\s*=\s*(['\"])[^'\"]*\2[^>]*>", re.I | re.S)


def line_number(source: str, offset: int) -> int:
    return source.count("\n", 0, offset) + 1


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


def inspect(path: Path):
    source = path.read_text(encoding="utf-8")
    findings = []

    def flag(offset, kind, detail):
        findings.append((line_number(source, offset), kind, detail))

    for pattern, kind, detail in (
        (r"\b(?:linear|radial|conic)-gradient\s*\(", "gradient", "check brand purpose and text contrast across the gradient"),
        (r"\btransition-all\b|transition\s*:\s*all\b", "transition-all", "limit animation to intended properties and respect reduced motion"),
        (r"\boutline\s*:\s*(?:none|0(?:px)?)\b|\boutline-none\b", "outline-removed", "check a visible keyboard-focus replacement"),
    ):
        for match in re.finditer(pattern, source, re.I):
            flag(match.start(), kind, detail)

    if path.suffix.lower() in {".html", ".jsx", ".tsx"}:
        labelled_ids = set(re.findall(r"<label\b[^>]*\b(?:for|htmlFor)\s*=\s*['\"]([^'\"]+)['\"]", source, re.I))
        for match in FIELD.finditer(source):
            tag = match.group(0)
            field_id = re.search(r"\bid\s*=\s*['\"]([^'\"]+)['\"]", tag)
            if re.search(r"\baria-(?:label|labelledby)\s*=", tag, re.I):
                continue
            if field_id and field_id.group(1) in labelled_ids:
                continue
            # A wrapping label or dynamic component may still provide the name.
            flag(match.start(), "placeholder-label", "verify the field has a persistent accessible name")

    if path.suffix.lower() in {".css", ".scss", ".html", ".jsx", ".tsx"}:
        for block in BLOCK.finditer(source):
            declarations = {key.lower(): value.strip() for key, value in DECL.findall(block.group(2))}
            foreground = rgb(declarations.get("color", ""))
            background = rgb(declarations.get("background-color", ""))
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="UI files or directories")
    parser.add_argument("--strict", action="store_true", help="exit 1 when review candidates are found")
    args = parser.parse_args()
    files = sorted({file for path in args.paths for file in (path.rglob("*") if path.is_dir() else [path])
                    if file.is_file() and file.suffix.lower() in EXTENSIONS})
    count = 0
    for file in files:
        for line, kind, detail in inspect(file):
            print(f"{file}:{line}: {kind}: {detail}")
            count += 1
    print(f"{count} review candidate(s) in {len(files)} file(s). Static checks are partial evidence.")
    return 1 if args.strict and count else 0


if __name__ == "__main__":
    raise SystemExit(main())
