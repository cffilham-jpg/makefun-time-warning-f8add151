"""Write the funniest time machine warning label to entry.txt."""

import hashlib
import os
import tempfile

LINE = "NOTICE: This machine is safe when operated exactly as instructed. You have already operated it incorrectly. Twice."
CHAR_LIMIT = 120
OUTPUT_FILENAME = "entry.txt"


def _resolve_output_dir():
    """Return the output directory.

    MAKEFUN_OUTPUT_DIR wins when set. Otherwise use ./out, falling back
    to a fresh temp dir when the working directory is read-only.
    """
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    try:
        os.makedirs("out", exist_ok=True)
        return "out"
    except OSError:
        return tempfile.mkdtemp(prefix="makefun-time-warning-")


def validate(path):
    """Re-read entry.txt and assert it holds exactly LINE, nothing else."""
    with open(path, "rb") as f:
        data = f.read()
    text = data.decode("utf-8")
    assert 1 <= len(text) <= CHAR_LIMIT, "line must be 1-120 characters"
    assert "\n" not in text, "must be a single line"
    assert "\r" not in text, "must not contain a carriage return"
    assert not data.endswith(b"\n"), "must not end with a newline"
    assert text == text.strip(), "must not have leading/trailing whitespace"
    assert text == LINE, "content must equal LINE"


def main():
    out_dir = _resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_FILENAME)
    with open(path, "wb") as f:
        f.write(LINE.encode("utf-8"))
    validate(path)
    print(hashlib.sha256(LINE.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
