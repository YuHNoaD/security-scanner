from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        if self.path == '/health':
            response = '{"status": "healthy"}'
        elif self.path == '/':
            response = '{"message": "Security Scanner API", "version": "1.0.0", "status": "running"}'
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = '{"error": "Not found"}'
        
        self.wfile.write(response.encode())