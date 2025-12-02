from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
from datetime import datetime
import os
from google import genai

# Configure Google Gemini API
client = genai.Client(api_key='AIzaSyA-hvrLKoYItByTN3-SAsrftMLZvdkP7LA')

# File to store messages
MESSAGES_FILE = 'messages.json'

def load_messages():
    """Load messages from JSON file"""
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_messages(messages):
    """Save messages to JSON file"""
    with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

class RequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.path = '/iframeindex.html'
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/save_message':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                user_message = data.get('message', '')

                
                if not user_message:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Message is required'}).encode())
                    return
                
                # Get AI response from Google Gemini
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=user_message
                )
                ai_response = response.text
                
                # Load existing messages
                messages = load_messages()
                
                # Add user message
                messages.append({
                    'type': 'user',
                    'message': user_message,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Add AI response
                messages.append({
                    'type': 'ai',
                    'message': ai_response,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Save to file
                save_messages(messages)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response_data = {
                    'success': True,
                    'user_message': user_message,
                    'ai_response': ai_response
                }
                self.wfile.write(json.dumps(response_data).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 5000), RequestHandler)
    print('Server running on http://localhost:5000')
    server.serve_forever()
