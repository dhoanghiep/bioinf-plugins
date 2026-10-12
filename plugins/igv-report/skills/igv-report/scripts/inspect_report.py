#!/usr/bin/env python3
"""Inspect, dump or patch the igv.js sessions inside an igv-reports HTML file.

An igv-reports page keeps one gzipped+base64 igv.js session per region-table row in a
`const sessionDictionary = {...}` literal. This reads that literal back so you can see
what tracks a report actually carries, and round-trip it when a small edit is cheaper
than regenerating the report from data that lives off this machine.

    inspect_report.py REPORT.html
        print each locus and its full track config (long data: URLs elided)

    inspect_report.py REPORT.html --sessions-out DIR
        write DIR/session_<id>.json, one decoded session per table row

    inspect_report.py REPORT.html --patch DIR --out NEW.html
        re-encode DIR/session_<id>.json back into a copy of the report
"""
import argparse
import base64
import gzip
import json
import pathlib
import re
import sys

SESSION_RE = re.compile(r"(const sessionDictionary = )(\{.*?\})(\s*\n)", re.S)
TABLE_RE = re.compile(r"const tableJson = (\{.*?\})\s*\n", re.S)
PREFIX = "data:application/gzip;base64,"


def read_sessions(html):
    m = SESSION_RE.search(html)
    if not m:
        sys.exit("no sessionDictionary found: is this an igv-reports page?")
    return {k: decode(v) for k, v in json.loads(m.group(2)).items()}


def decode(data_url):
    if not data_url.startswith(PREFIX):
        sys.exit(f"unexpected session encoding: {data_url[:40]}...")
    return json.loads(gzip.decompress(base64.b64decode(data_url[len(PREFIX):])))


def encode(session):
    raw = json.dumps(session, separators=(",", ":")).encode()
    # mtime=0 so re-encoding the same session twice gives the same bytes
    return PREFIX + base64.b64encode(gzip.compress(raw, mtime=0)).decode()


def elide(obj, limit=80):
    """Same structure, with any long string replaced by a length marker."""
    if isinstance(obj, dict):
        return {k: elide(v, limit) for k, v in obj.items()}
    if isinstance(obj, list):
        return [elide(v, limit) for v in obj]
    if isinstance(obj, str) and len(obj) > limit:
        return f"<{len(obj)} chars>"
    return obj


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("report", type=pathlib.Path)
    p.add_argument("--sessions-out", type=pathlib.Path, metavar="DIR",
                   help="dump each decoded session as DIR/session_<id>.json")
    p.add_argument("--patch", type=pathlib.Path, metavar="DIR",
                   help="re-encode sessions from DIR back into the report")
    p.add_argument("--out", type=pathlib.Path, metavar="FILE",
                   help="where to write the patched report (required with --patch)")
    args = p.parse_args()

    html = args.report.read_text()
    sessions = read_sessions(html)

    if args.patch:
        if not args.out:
            p.error("--patch needs --out")
        patched = {}
        for key in sessions:
            f = args.patch / f"session_{key}.json"
            if not f.exists():
                sys.exit(f"missing {f}: --patch needs one file per session")
            patched[key] = encode(json.loads(f.read_text()))
        new = SESSION_RE.sub(
            lambda m: m.group(1) + json.dumps(patched) + m.group(3), html, count=1)
        args.out.write_text(new)
        print(f"wrote {args.out} ({len(patched)} sessions, {args.out.stat().st_size} bytes)")
        return

    if args.sessions_out:
        args.sessions_out.mkdir(parents=True, exist_ok=True)
        for key, session in sessions.items():
            f = args.sessions_out / f"session_{key}.json"
            f.write_text(json.dumps(session, indent=1))
            print(f"wrote {f}")
        return

    table = TABLE_RE.search(html)
    if table:
        tj = json.loads(table.group(1))
        print(f"region table: {tj['headers']}")
        for row in tj["rows"]:
            print(f"  {row}")
        print()
    for key, session in sessions.items():
        print(f"--- session {key}: {session.get('locus')}")
        for track in session.get("tracks", []):
            print("    " + json.dumps(elide(track)))


if __name__ == "__main__":
    main()
