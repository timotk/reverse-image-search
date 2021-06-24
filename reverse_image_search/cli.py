import argparse
from pathlib import Path
from typing import List, Tuple

from tabulate import tabulate

from reverse_image_search import config
from reverse_image_search.search import search_similar_images
from reverse_image_search.spinner import Spinner


def print_matches(matches: List[Tuple[Path, float]]) -> None:
    if not matches:
        print("\rNo matches found :(")
        return

    matches = sorted(matches, key=lambda r: r[1], reverse=True)
    rows = [(filepath, f"{sim:.0%}") for filepath, sim in matches]

    print("\rMatches:")
    print(tabulate(rows, headers=["filepath", "similarity"]))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("src_path", type=Path, help="Path to image you want search for")
    parser.add_argument("search_path", type=Path, help="Path to search")
    parser.add_argument(
        "--filetypes",
        nargs="+",
        default=config.DEFAULT_ALLOWED_FILETYPES,
        help="Filetypes to search for",
    )
    parser.add_argument(
        "-t/--threshold",
        type=float,
        default=config.THRESHOLD,
        dest="threshold",
        help="Similarity should be higher than this threshold",
    )
    return parser.parse_args()


def cli():
    args = parse_args()
    print(
        f"Finding similar images...\n"
        f"- to: {args.src_path}\n"
        f"- in: {args.search_path}\n"
        f"- filetypes: {args.filetypes}\n"
        f"- threshold: {args.threshold}\n"
    )

    with Spinner():
        matches = search_similar_images(
            src_path=args.src_path,
            search_path=args.search_path,
            threshold=args.threshold,
            allowed_filetypes=args.filetypes,
        )

    print_matches(matches)


if __name__ == "__main__":
    cli()
