import json
import subprocess
import sys
from os import PathLike
from pathlib import Path
from typing import Union


def extract(pdf_path: Union[str, PathLike]) -> None:
    # fmt: off
    proc = subprocess.run(
        ["pdfannots", pdf_path, "-f", "json"],
        stdout=subprocess.PIPE,
        stderr=sys.stderr,
        cwd=Path(__file__).parent
    )
    # fmt: on

    json_text = proc.stdout.replace(b"\r", b"").decode("utf-8")
    json_data = json.loads(json_text)

    annots = {}
    for entry in json_data:
        if "contents" in entry:
            section = "Note"
        else:
            section = entry["type"]
        section_data = annots.setdefault(section, {})
        page_data = section_data.setdefault(entry["page"], [])
        if "contents" in entry:
            page_data.append(entry["contents"])
        elif "text" in entry:
            page_data.append(entry["text"])

    SECTIONS = ("Note", "Highlight", "Underline")
    for section in sorted(annots.keys(), key=lambda x: SECTIONS.index(x) if x in SECTIONS else 99):
        print(f"## {section}s")
        curr_page = 0
        for page in annots[section].keys():
            if page != curr_page:
                print(f"\np.{page}\n")
                curr_page = page
            for text in annots[section][page]:
                if text:
                    print(f"- {text}")
        print("")


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: python annots.py INFILE")
        sys.exit(1)
    extract(Path(sys.argv[1]).resolve())


if __name__ == "__main__":
    main()
