import json
import subprocess
import sys
from os import PathLike
from pathlib import Path
from typing import Union


def extract(pdf_path: Union[str, PathLike]) -> None:
    # fmt: off
    proc = subprocess.run(
        [
            "pipenv", "run", "python",
            "./pdfannots/pdfannots.py",
            pdf_path,
            "-f", "json",
        ],
        stdout=subprocess.PIPE,
        stderr=sys.stderr,
        cwd=Path(__file__).parent
    )
    # fmt: on

    json_text = proc.stdout.replace(b"\r", b"").decode("utf-8")
    json_data = json.loads(json_text)

    print("[[Highlights]]")
    page = 0
    for entry in json_data:
        if entry["type"] != "Highlight":
            continue
        if page != entry["page"]:
            page = entry["page"]
            print(f"\np. {page}")
        print(f"\t{entry['text']}")


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: python extract.py INFILE")
        sys.exit(1)
    extract(Path(sys.argv[1]).resolve())


if __name__ == "__main__":
    main()
