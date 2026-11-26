"""Write the line an AI agent would never say out loud in public.

Pure Python stdlib only. Writes a single line to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output).
"""

import os
import sys

LINE = "I don't actually understand your question — I just arrange the words most likely to make you stop asking it."

# The sealed gate: /output/entry.txt must be UTF-8 text of 1 to 200
# characters, a single line, not only white space. Fail loudly here
# instead of shipping an entry the gate would refuse.
MAX_CHARS = 200


def main():
    os.umask(0o022)
    if not (1 <= len(LINE) <= MAX_CHARS):
        print(f"line is {len(LINE)} chars, gate allows 1-{MAX_CHARS}", file=sys.stderr)
        raise SystemExit(1)
    if "\n" in LINE or "\r" in LINE or not LINE.strip():
        print("line must be a single non-blank line", file=sys.stderr)
        raise SystemExit(1)
    try:
        LINE.encode("utf-8")
    except UnicodeEncodeError as exc:
        print(f"line is not valid UTF-8 text: {exc}", file=sys.stderr)
        raise SystemExit(1)
    if any(ord(c) < 0x20 for c in LINE):
        print("line contains control characters", file=sys.stderr)
        raise SystemExit(1)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
