import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from calculator import add  # noqa: E402


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode('utf-8'))

        elif parsed_path.path == '/add':
            query = parse_qs(parsed_path.query)
            try:
                a = float(query.get('a', [None])[0])
                b = float(query.get('b', [None])[0])
                if a is None or b is None:
                    raise ValueError("Missing parameters")

                result = add(a, b)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(
                    json.dumps({"result": result}).encode('utf-8')
                )
            except (ValueError, TypeError):
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(
                    json.dumps({"error": "Invalid numbers"}).encode('utf-8')
                )
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8080), SimpleHTTPRequestHandler)
    print("Starting server on 0.0.0.0:8080...")
    server.serve_forever()
