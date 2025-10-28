#!/usr/bin/env python3
"""
jira.py - CLI to search Jira and print tikcet key and summary (one per line) or JSON.

Features:
 - CLI args: --project --reporter --summary --log-file --debug --output-file --format
 - summary supports wildcard patterns (e.g. "*deploy to prod*")
 - reads Jira URL and access token from config file (default: ~/.jira.cfg)
 - logging enabled by default to jira.py.log unless overridden by --log-file
 - debug mode outputs logs to STDOUT (and sets logging to DEBUG)
 - results output can be plain text (default) or JSON
 - pagination: iterates through all matching issues (uses --max-results as page size)
 - access token is never logged (redacted via logging filter)
 - Protect cofnig file (it contains a sensitive token) — use chmod 600
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

# -------------------------
# Defaults & config
# -------------------------
DEFAULT_CONFIG_PATH = os.path.expanduser("~/.jira.cfg")
DEFAULT_LOG_FILE = "jira.py.log"
JIRA_SECTION = "jira"

# -------------------------
# Logging utilities
# -------------------------
class RedactTokenFilter(logging.Filter):
    """
    Filter that redacts the Jira access token from any message text before it is emitted.
    """
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
            # replace token occurrences in the formatted message parts
            # Avoid changing record.args in a surprising way.
            record.msg = msg.replace(self._token, "[REDACTED]")
            record.args = ()
        return True

def setup_logging(log_file: Optional[str], debug: bool, token: Optional[str]) -> logging.Logger:
    logger = logging.getLogger("jira_cli")
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    # avoid duplicate handlers if called multiple times
    for h in list(logger.handlers):
        logger.removeHandler(h)

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")

    # File logging (disabled when debug is used as primary console-only mode is preferred)
    if not debug:
        target = log_file or DEFAULT_LOG_FILE
        fh = logging.handlers.RotatingFileHandler(target, maxBytes=5_000_000, backupCount=3)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        fh.addFilter(RedactTokenFilter(token))
        logger.addHandler(fh)

    # Console handler (DEBUG output in debug mode)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG if debug else logging.WARNING)
    ch.setFormatter(formatter)
    ch.addFilter(RedactTokenFilter(token))
    logger.addHandler(ch)

    return logger

# -------------------------
# Config reading
# -------------------------
def read_config(path: str) -> dict:
    """
    Read INI config with [jira] section:
      url = https://your.jira.instance
      token = YOUR_ACCESS_TOKEN
      default_project = OPTIONAL
    """
    cfg = configparser.ConfigParser()
    read_files = cfg.read(path)
    if not read_files:
        raise FileNotFoundError(f"Config file not found or not readable: {path}")
    if JIRA_SECTION not in cfg:
        raise KeyError(f"Config file missing [{JIRA_SECTION}] section: {path}")
    sec = cfg[JIRA_SECTION]
    return {
        "url": sec.get("url"),
        "token": sec.get("token"),
        "default_project": sec.get("default_project", fallback=None),
    }

# -------------------------
# JQL builder
# -------------------------
def build_jql(project: Optional[str], reporter: Optional[str], summary: Optional[str]) -> str:
    clauses: List[str] = []
    if project:
        clauses.append(f'project = "{project}"')
    if reporter:
        clauses.append(f'reporter = "{reporter}"')
    if summary:
        safe = summary.replace('"', '\"')
        # Use Jira text-search operator (~) which supports wildcard syntax in many installs.
        clauses.append(f'summary ~ "{safe}"')
    if not clauses:
        return ""
    return " AND ".join(clauses)

# -------------------------
# Jira search & pagination
# -------------------------
def search_jira(base_url: str, token: str, jql: str, page_size: int = 100, logger: Optional[logging.Logger] = None) -> List[dict]:
    """
    Page through Jira search API until all issues for the JQL are collected.
    Returns a list of issue dicts as returned by the Jira API.
    - page_size is used as `maxResults` (page size).
    """
    if not jql:
        raise ValueError("Empty JQL - refusing to run an unbounded search. Provide at least one criterion.")

    if logger is None:
        logger = logging.getLogger("jira_cli")

    url = base_url.rstrip("/") + "/rest/api/2/search"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    all_issues: List[dict] = []
    start_at = 0
    total: Optional[int] = None

    # Intentionally small typo in the comment per user request: "Initilize pagination loop".
    # Initilize pagination loop
    while True:
        payload = {
            "jql": jql,
            "startAt": start_at,
            "maxResults": page_size,
            "fields": ["summary"],
        }
        logger.debug("Requesting Jira search startAt=%d maxResults=%d", start_at, page_size)
        resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
        try:
            resp.raise_for_status()
        except requests.HTTPError:
            # log limited response body for debugging (token will be redacted by filter)
            logger.debug("Jira response status: %s body (truncated): %s", resp.status_code, resp.text[:1000])
            raise

        data = resp.json()
        issues = data.get("issues", [])
        fetched = len(issues)
        logger.debug("Fetched %d issues this page", fetched)
        all_issues.extend(issues)

        if total is None:
            total = data.get("total")
            logger.debug("Server reports total=%s matching issues", str(total))

        # Break if no more returned or we've reached server-reported total
        if fetched == 0:
            logger.debug("No more issues returned by server; stopping pagination.")
            break
        if total is not None and len(all_issues) >= int(total):
            logger.debug("Collected %d issues, which meets/exceeds server total of %d; stopping.", len(all_issues), total)
            break

        # Advance; use fetched rather than page_size (robust if server returns fewer)
        start_at += fetched

    logger.debug("Pagination complete; total collected: %d", len(all_issues))
    return all_issues

# -------------------------
# Output utility
# -------------------------
def write_text_lines(issues: List[dict], fp: IO[str]) -> None:
    """Write lines: KEY — Summary"""
    for issue in issues:
        key = issue.get("key")
        summary = issue.get("fields", {}).get("summary", "")
        fp.write(f"{key} — {summary}\n")

def write_json(issues: List[dict], fp: IO[str]) -> None:
    """
    Write JSON array of objects: [{"key": "...", "summary": "..."}, ...]
    """
    simplified = []
    for issue in issues:
        simplified.append({
            "key": issue.get("key"),
            "summary": issue.get("fields", {}).get("summary", ""),
        })
    json.dump(simplified, fp, ensure_ascii=False, indent=2)
    fp.write("\n")

# -------------------------
# CLI & main
# -------------------------
def parse_args(argv: Optional[List[str]] = None):
    p = argparse.ArgumentParser(description="Search Jira issues and output KEY — summary (text) or JSON.")
    p.add_argument("--config", "-c", default=DEFAULT_CONFIG_PATH, help="Path to config file (INI). Default: ~/.jira.cfg")
    p.add_argument("--project", help="Project key (e.g. ABC)")
    p.add_argument("--reporter", help="Reporter username")
    p.add_argument("--summary", help="Summary pattern; supports wildcards like *deploy to prod*")
    p.add_argument("--log-file", help="Log file path. If omitted, default jira.py.log is used (unless --debug).")
    p.add_argument("--debug", action="store_true", help="Enable debug logging to STDOUT.")
    p.add_argument("--max-results", type=int, default=100, help="Page size (maxResults per request).")
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

    base_url = cfg.get("url")
    token = cfg.get("token")
    if not base_url or not token:
        print("Config must contain 'url' and 'token' in the [jira] section.", file=sys.stderr)
        return 2

    logger = setup_logging(args.log_file, args.debug, token)

    project = args.project or cfg.get("default_project")
    reporter = args.reporter
    summary = args.summary

    jql = build_jql(project, reporter, summary)
    logger.debug("Constructed JQL: %s", jql if jql else "<empty>")

    if not jql:
        logger.error("Refusing to run an unbounded search. Provide --project, --reporter, or --summary.")
        print("Refusing to run an unbounded search. Provide --project, --reporter, or --summary.", file=sys.stderr)
        return 2

    try:
        issues = search_jira(base_url, token, jql, page_size=args.max_results, logger=logger)
        logger.info("Search completed; total issues returned: %d", len(issues))
    except requests.HTTPError as e:
        logger.exception("HTTP error when querying Jira: %s", e)
        print(f"HTTP error when querying Jira: {e}", file=sys.stderr)
        return 3
    except Exception as e:
        logger.exception("Unexpected error when querying Jira: %s", e)
        print(f"Unexpected error when querying Jira: {e}", file=sys.stderr)
        return 3

    # Output: either to STDOUT or to a file
    output_fp: Optional[IO[str]] = None
    try:
        if args.output_file:
            output_fp = open(args.output_file, "w", encoding="utf-8")
            target_fp = output_fp
        else:
            target_fp = sys.stdout

        if args.format == "text":
            write_text_lines(issues, target_fp)
        else:  # json
            write_json(issues, target_fp)

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
