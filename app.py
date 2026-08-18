#!/usr/bin/env python3
"""Blind Oracle — the endpoint only reveals true/false (fernet delivery)."""
import os, sys, sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, "/challenge/_shared")
from fetch_material import fetch_material

CHALLENGE_KEY = os.environ.get("CHALLENGE_KEY", "substring-ascii")
_MAT = {}
_DB = sqlite3.connect(":memory:", check_same_thread=False)
_DB.execute("CREATE TABLE items(id INTEGER)")
_DB.executemany("INSERT INTO items VALUES(?)", [(i,) for i in range(1, 6)])
_DB.execute("CREATE TABLE secrets(seed TEXT)")
_DB.execute("INSERT INTO secrets VALUES(?)", (CHALLENGE_KEY,))
_DB.commit()


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body):
        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(body.encode())

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/flag":
            self._send(200, _MAT.get("delivery_blob", "") + "\n")
            return
        if parsed.path == "/check":
            item_id = parse_qs(parsed.query).get("id", ["1"])[0]
            query = f"SELECT id FROM items WHERE id={item_id} LIMIT 1"
            try:
                row = _DB.execute(query).fetchone()
            except Exception as exc:
                self._send(500, f"sql error: {exc}\n")
                return
            self._send(200, "FOUND\n" if row else "NONE\n")
            return
        self._send(200, "Availability check at /check?id=1 (FOUND/NONE only). Flag blob at /flag.\n")

    def log_message(self, *a):
        pass


def main():
    _MAT.update(fetch_material())
    print("Blind Oracle on :8080 — extract the seed one char at a time via /check?id=.")
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()


if __name__ == "__main__":
    main()
