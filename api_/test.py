from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        message = json.dumps({
            'status': 'ok',
            'message': 'Vercel serverless function working',
            'path': self.path
        })
        self.wfile.write(message.encode())
        return
    
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        message = json.dumps({
            'status': 'ok',
            'message': 'POST working',
            'path': self.path
        })
        self.wfile.write(message.encode())
        return
