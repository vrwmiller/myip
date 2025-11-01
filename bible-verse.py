#!/usr/bin/env python3
"""
bible-verse.py - Get a random Bible verse using bible-api.com

Usage:
  python bible-verse.py

Options:
  --translation TRANSLATION  Specify translation (default: KJV)
  --output-file FILE         Write verse to file instead of STDOUT
  --format FORMAT            Output format: text (default) or json

API: https://bible-api.com
"""

import argparse
import json
import random
import sys
import requests
from typing import Optional, IO

# List of books and chapters for random selection (abbreviated for brevity)
BOOKS = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
    "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
    "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel",
    "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi",
    "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
    "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon",
    "Hebrews", "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation"
]

# For simplicity, use Psalms for random verse (API supports book:chapter:verse)

def get_verse(reference: Optional[str], translation: str = "KJV") -> dict:
    if reference:
        url = f"https://bible-api.com/{reference.replace(' ', '+')}?translation={translation}"
    else:
        chapter = random.randint(1, 150)
        verse = random.randint(1, 6)
        url = f"https://bible-api.com/Psalms+{chapter}:{verse}?translation={translation}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()

def write_text(verse: dict, fp: IO[str]) -> None:
    fp.write(f"{verse.get('reference')}: {verse.get('text').strip()}\n")

def write_json(verse: dict, fp: IO[str]) -> None:
    json.dump(verse, fp, ensure_ascii=False, indent=2)
    fp.write("\n")

def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Get a Bible verse using bible-api.com")
    p.add_argument("--translation", default="KJV", help="Translation (default: KJV)")
    p.add_argument("--verse", help="Specify verse reference (e.g. 'Psalms 23:1')")
    p.add_argument("--output-file", help="Write verse to file instead of STDOUT")
    p.add_argument("--format", choices=["text", "json"], default="text", help="Output format: text (default) or json")
    return p.parse_args(argv)

def main(argv=None) -> int:
    args = parse_args(argv)
    try:
        verse = get_verse(args.verse, args.translation)
    except Exception as e:
        print(f"Error fetching verse: {e}", file=sys.stderr)
        return 2
    output_fp: Optional[IO[str]] = None
    try:
        if args.output_file:
            output_fp = open(args.output_file, "w", encoding="utf-8")
            target_fp = output_fp
        else:
            target_fp = sys.stdout
        if args.format == "text":
            write_text(verse, target_fp)
        else:
            write_json(verse, target_fp)
    except Exception as e:
        print(f"Error writing output: {e}", file=sys.stderr)
        return 3
    finally:
        if output_fp:
            output_fp.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
