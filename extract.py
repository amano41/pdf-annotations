import json
import subprocess
import sys


def extract(pdf_path: str) -> None:
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
    extract(sys.argv[1])


if __name__ == "__main__":
    main()
