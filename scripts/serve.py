"""Local preview server: http://localhost:8795/

Serves the site with no caching (so edits show on refresh) and answers /api/espn the
same way api/espn.js does on Vercel. Run from the repo root: python scripts/serve.py
"""
import functools
import http.server
import os
import re
import urllib.parse
import urllib.request

PORT = 8795
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED = re.compile(r"^apis/(site/)?v2/sports/(football/nfl|basketball/nba)/(scoreboard|standings)(\?[\w=&.-]*)?$")
UA = "sports-calendar/1.0"


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        if url.path != "/api/espn":
            return super().do_GET()
        path = urllib.parse.parse_qs(url.query).get("path", [""])[0]
        if not ALLOWED.match(path):
            return self.send_error(400, "path not allowed")
        try:
            req = urllib.request.Request(f"https://site.api.espn.com/{path}", headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as r:
                body = r.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except Exception:
            self.send_error(502, "ESPN unreachable")

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), functools.partial(Handler, directory=ROOT)).serve_forever()
