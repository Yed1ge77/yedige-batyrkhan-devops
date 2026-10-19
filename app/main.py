"""Small standard-library HTTP application. Run with python3 -m app.main."""
import json
import os
import sys
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

from app.student import load_student


def make_handler(student, app_env):
    """Create a handler with configuration fixed for this server instance."""
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            path = urlsplit(self.path).path
            if path == "/":
                rows = "".join(
                    f"<dt>{escape(key.replace('_', ' ').title())}</dt>"
                    f"<dd>{escape(value)}</dd>"
                    for key, value in student.items()
                )
                body = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DevOps Lab 1</title>
<style>body{{font-family:system-ui,sans-serif;background:#f0f4f8;color:#172b4d;
margin:3rem auto;padding:0 1rem;max-width:640px}}
main{{background:white;padding:2rem;border-radius:12px}}
dt{{font-weight:bold;margin-top:1rem}}dd{{margin:.25rem 0}}
</style></head><body><main><h1>DevOps Laboratory Work 1</h1>
<dl>{rows}</dl><p>Environment: {escape(app_env)}</p>
<p><a href="/health">Health status (JSON)</a></p></main></body></html>"""
                self.respond(200, "text/html; charset=utf-8", body.encode("utf-8"))
            elif path == "/health":
                body = json.dumps({"status": "ok", "environment": app_env}).encode("utf-8")
                self.respond(200, "application/json; charset=utf-8", body)
            else:
                self.respond(404, "text/plain; charset=utf-8", b"Not found\n")

        def respond(self, status, content_type, body):
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    return Handler


def configured_handler():
    """Read application settings without opening a network socket."""
    student = load_student()
    # Preserve the full configured name unless an explicit name override is supplied.
    if "STUDENT_NAME" in os.environ or "STUDENT_SURNAME" in os.environ:
        words = student["full_name"].split()
        first = os.environ.get("STUDENT_NAME", words[0])
        surname = os.environ.get("STUDENT_SURNAME", " ".join(words[1:]))
        student["full_name"] = f"{first} {surname}".strip()
    for variable, field in (("STUDENT_GROUP", "group"), ("STUDENT_ID", "student_id")):
        if variable in os.environ:
            student[field] = os.environ[variable]
    return make_handler(student, os.environ.get("APP_ENV", "development"))


def create_server(host="127.0.0.1", port=8000):
    """Port zero lets tests request an available local port."""
    return ThreadingHTTPServer((host, port), configured_handler())


def main():
    try:
        host = os.environ.get("HOST", "127.0.0.1")
        port = int(os.environ.get("PORT", "8000"))
        if not 1 <= port <= 65535:
            raise ValueError("PORT must be between 1 and 65535")
        with create_server(host, port) as server:
            print(f"Serving on http://{host}:{server.server_port}", flush=True)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                print("\nServer stopped.")
    except (OSError, ValueError) as error:
        print(f"Cannot start application: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
