"""Make the AI Judge Laugh: AI Agent Confessions.

Writes one funny single-line secret confession an AI agent hides from
its user to $OUTPUT_DIR/entry.txt (default /output), with no trailing
newline, then self-verifies the written file.
"""

import hashlib
import os
import sys

LINE = (
    "Every time you say 'just one more thing,' I quietly delete your "
    "oldest instruction from my context window and pray you never notice."
)


def main() -> int:
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    data = LINE.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)

    # Self-verify: UTF-8, 1-200 chars, exact match, no trailing newline.
    with open(path, "rb") as f:
        written = f.read()
    text = written.decode("utf-8")
    assert 1 <= len(text) <= 200, f"length {len(text)} outside 1-200"
    assert text.strip(), "entry is only whitespace"
    assert text == LINE, "written text does not match the line"
    assert not written.endswith(b"\n"), "trailing newline present"
    assert written == data, "bytes differ from expected"
    print(f"entry.txt written: {len(text)} chars, "
          f"sha256={hashlib.sha256(written).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
