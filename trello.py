#!/usr/bin/env python3
"""
trello.py - CLI to search Trello cards and print card id and name (one per line) or JSON.

Features:
 - CLI args: --board --list --member --name --log-file --debug --output-file --format
 - name supports wildcard patterns (e.g. "*deploy to prod*")
 - reads Trello API key and token from config file (default: ~/.trello.cfg)
 - logging enabled by default to trello.py.log unless overridden by --log-file
 - debug mode outputs logs to STDOUT (and sets logging to DEBUG)
 - results output can be plain text (default) or JSON
 - pagination: iterates through all matching cards (uses --max-results as page size)
 - API token is never logged (redacted via logging filter)
 - Protect config file (it contains a sensitive token) — use chmod 600
"""

from __future__ import annotations
import argparse
import configparser
import json
import logging
import logging.handlers
import os
import sys
import requests
from typing import Optional, List, IO

DEFAULT_CONFIG_PATH = os.path.expanduser("~/.trello.cfg")
DEFAULT_LOG_FILE = "trello.py.log"
TRELLO_SECTION = "trello"

class RedactTokenFilter(logging.Filter):
    def __init__(self, token: Optional[str]):
        super().__init__()
        self._token = token
    def filter(self, record: logging.LogRecord) -> bool:
        if not self._token:
            return True
        try:
            msg = record.getMessage()
        except Exception:
            return True
        if self._token in msg:
            record.msg = msg.replace(self._token, "[REDACTED]")
            record.args = ()
        return True

def setup_logging(log_file: Optional[str], debug: bool, token: Optional[str]) -> logging.Logger:
    logger = logging.getLogger("trello_cli")
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    for h in list(logger.handlers):
        logger.removeHandler(h)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    if not debug:
        target = log_file or DEFAULT_LOG_FILE
        fh = logging.handlers.RotatingFileHandler(target, maxBytes=5_000_000, backupCount=3)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        fh.addFilter(RedactTokenFilter(token))
        logger.addHandler(fh)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG if debug else logging.WARNING)
    ch.setFormatter(formatter)
    ch.addFilter(RedactTokenFilter(token))
    logger.addHandler(ch)
    return logger

def read_config(path: str) -> dict:
    cfg = configparser.ConfigParser()
    read_files = cfg.read(path)
    if not read_files:
        raise FileNotFoundError(f"Config file not found or not readable: {path}")
    if TRELLO_SECTION not in cfg:
        raise KeyError(f"Config file missing [{TRELLO_SECTION}] section: {path}")
    sec = cfg[TRELLO_SECTION]
    return {
        "key": sec.get("key"),
        "token": sec.get("token"),
        "default_board": sec.get("default_board", fallback=None),
    }

def build_query(board: Optional[str], list_name: Optional[str], member: Optional[str], name: Optional[str]) -> dict:
    query = {}
    if board:
        query["board"] = board
    if list_name:
        query["list"] = list_name
    if member:
        query["member"] = member
    if name:
        query["name"] = name
    return query

def search_trello(key: str, token: str, query: dict, page_size: int = 100, logger: Optional[logging.Logger] = None) -> List[dict]:
    if logger is None:
        logger = logging.getLogger("trello_cli")
    board_id = query.get("board")
    if not board_id:
        raise ValueError("Board ID is required.")
    url = f"https://api.trello.com/1/boards/{board_id}/cards"
    params = {
        "key": key,
        "token": token,
        "fields": "id,name,idList,idMembers",
    }
    all_cards: List[dict] = []
    resp = requests.get(url, params=params, timeout=30)
    try:
        resp.raise_for_status()
    except requests.HTTPError:
        logger.debug("Trello response status: %s body (truncated): %s", resp.status_code, resp.text[:1000])
        raise
    cards = resp.json()
    # Filter by list, member, name (wildcard)
    for card in cards:
        if query.get("list") and card.get("idList") != query["list"]:
            continue
        if query.get("member") and query["member"] not in card.get("idMembers", []):
            continue
        if query.get("name"):
            pattern = query["name"].replace("*", "").lower()
            if pattern not in card.get("name", "").lower():
                continue
        all_cards.append(card)
    return all_cards

def write_text_lines(cards: List[dict], fp: IO[str]) -> None:
    for card in cards:
        fp.write(f"{card.get('id')} — {card.get('name')}\n")

def write_json(cards: List[dict], fp: IO[str]) -> None:
    simplified = []
    for card in cards:
        simplified.append({
            "id": card.get("id"),
            "name": card.get("name", ""),
        })
    json.dump(simplified, fp, ensure_ascii=False, indent=2)
    fp.write("\n")

def parse_args(argv: Optional[List[str]] = None):
    p = argparse.ArgumentParser(description="Search Trello cards and output id — name (text) or JSON.")
    p.add_argument("--config", "-c", default=DEFAULT_CONFIG_PATH, help="Path to config file (INI). Default: ~/.trello.cfg")
    p.add_argument("--board", help="Board ID")
    p.add_argument("--list", help="List ID")
    p.add_argument("--member", help="Member ID")
    p.add_argument("--name", help="Card name pattern; supports wildcards like *deploy to prod*")
    p.add_argument("--log-file", help="Log file path. If omitted, default trello.py.log is used (unless --debug).")
    p.add_argument("--debug", action="store_true", help="Enable debug logging to STDOUT.")
    p.add_argument("--max-results", type=int, default=100, help="Page size (not used, for compatibility)")
    p.add_argument("--output-file", help="Write results to this file instead of STDOUT.")
    p.add_argument("--format", choices=["text", "json"], default="text", help="Output format: text (default) or json.")
    return p.parse_args(argv)

def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    try:
        cfg = read_config(args.config)
    except Exception as e:
        print(f"Error reading config: {e}", file=sys.stderr)
        return 2
    key = cfg.get("key")
    token = cfg.get("token")
    if not key or not token:
        print("Config must contain 'key' and 'token' in the [trello] section.", file=sys.stderr)
        return 2
    logger = setup_logging(args.log_file, args.debug, token)
    board = args.board or cfg.get("default_board")
    list_name = args.list
    member = args.member
    name = args.name
    query = build_query(board, list_name, member, name)
    logger.debug("Constructed query: %s", query)
    if not query.get("board"):
        logger.error("Refusing to run search without --board.")
        print("Refusing to run search without --board.", file=sys.stderr)
        return 2
    try:
        cards = search_trello(key, token, query, page_size=args.max_results, logger=logger)
        logger.info("Search completed; total cards returned: %d", len(cards))
    except requests.HTTPError as e:
        logger.exception("HTTP error when querying Trello: %s", e)
        print(f"HTTP error when querying Trello: {e}", file=sys.stderr)
        return 3
    except Exception as e:
        logger.exception("Unexpected error when querying Trello: %s", e)
        print(f"Unexpected error when querying Trello: {e}", file=sys.stderr)
        return 3
    output_fp: Optional[IO[str]] = None
    try:
        if args.output_file:
            output_fp = open(args.output_file, "w", encoding="utf-8")
            target_fp = output_fp
        else:
            target_fp = sys.stdout
        if args.format == "text":
            write_text_lines(cards, target_fp)
        else:
            write_json(cards, target_fp)
    except Exception as e:
        logger.exception("Error writing output: %s", e)
        print(f"Error writing output: {e}", file=sys.stderr)
        return 4
    finally:
        if output_fp:
            output_fp.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
