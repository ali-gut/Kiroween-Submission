import asyncio
import websockets
import json
from datetime import datetime
import os
import base64
from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from google import genai

try:
    from pypdf import PdfReader
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    print("Warning: pypdf not installed. PDF reading will be limited.")

# Configure Google Gemini API
client = genai.Client(api_key='inserAPIiguess')

# File to store messages and context
MESSAGES_FILE = 'messages.json'
CONTEXT_FILE = 'file_context.json'
THOUGHTS_FILE = 'shared_thoughts.json'
UPLOADS_DIR = 'uploaded_files'

# Create uploads directory if it doesn't exist
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

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

def load_file_context():
    """Load uploaded file context"""
    if os.path.exists(CONTEXT_FILE):
        with open(CONTEXT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_file_context(files):
    """Save uploaded file context"""
    with open(CONTEXT_FILE, 'w', encoding='utf-8') as f:
        json.dump(files, f, ensure_ascii=False, indent=2)

def load_thoughts():
    """Load shared thoughts from JSON file"""
    if os.path.exists(THOUGHTS_FILE):
        with open(THOUGHTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_thoughts(thoughts):
    """Save shared thoughts to JSON file"""
    with open(THOUGHTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(thoughts, f, ensure_ascii=False, indent=2)

def extract_pdf_text(pdf_content):
    """Extract text from PDF content"""
    if not PDF_SUPPORT:
        return "[PDF content - pypdf not installed]"
    
    try:
        from io import BytesIO
        pdf_file = BytesIO(pdf_content)
        pdf_reader = PdfReader(pdf_file)
        
        text = ""
        for page_num, page in enumerate(pdf_reader.pages):
            text += f"\n--- Page {page_num + 1} ---\n"
            text += page.extract_text()
        
        return text
    except Exception as e:
        return f"[Error reading PDF: {str(e)}]"

def save_uploaded_file(filename, content, file_type):
    """Save uploaded file and extract text if PDF"""
    # Create safe filename
    safe_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_', '-'))
    base_name = os.path.splitext(safe_filename)[0]
    
    # Save original file
    file_path = os.path.join(UPLOADS_DIR, safe_filename)
    
    extracted_text = content
    
    # If PDF, extract text and save as .txt
    if file_type == 'application/pdf' or filename.lower().endswith('.pdf'):
        try:
            # Decode base64 if needed
            if content.startswith('data:'):
                content = content.split(',')[1]
            
            pdf_bytes = base64.b64decode(content)
            
            # Save original PDF
            with open(file_path, 'wb') as f:
                f.write(pdf_bytes)
            
            # Extract text
            extracted_text = extract_pdf_text(pdf_bytes)
            
            # Save extracted text
            text_path = os.path.join(UPLOADS_DIR, f"{base_name}.txt")
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(extracted_text)
            
            print(f"Saved PDF and extracted text: {text_path}")
            
        except Exception as e:
            print(f"Error processing PDF: {e}")
            extracted_text = f"[Error processing PDF: {str(e)}]"
    else:
        # Save text file as-is
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return extracted_text

# HTTP Server Handler
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
        elif self.path == '/get_thoughts':
            try:
                thoughts = load_thoughts()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'thoughts': thoughts}).encode())
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
                return
        elif self.path == '/get_files':
            try:
                files = load_file_context()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'files': files}).encode())
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
                return
        elif self.path == '/get_messages':
            try:
                messages = load_messages()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'messages': messages}).encode())
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
                return
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/add_thought':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                message = data.get('message', '')
                if message:
                    thoughts = load_thoughts()
                    thoughts.append({
                        'message': message,
                        'timestamp': datetime.now().isoformat()
                    })
                    save_thoughts(thoughts)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True}).encode())
                
            except Exception as e:
                print(f"Add thought error: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        
        elif self.path == '/upload_context':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                files = data.get('files', [])
                
                # Process each file and extract text if PDF
                processed_files = []
                for file in files:
                    filename = file.get('name', 'unknown')
                    content = file.get('content', '')
                    file_type = file.get('type', '')
                    
                    # Save file and extract text
                    extracted_text = save_uploaded_file(filename, content, file_type)
                    
                    # Store processed file info
                    processed_files.append({
                        'name': filename,
                        'content': extracted_text[:5000],  # Limit to 5000 chars for context
                        'type': file_type,
                        'size': file.get('size', 0)
                    })
                
                save_file_context(processed_files)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True}).encode())
                
            except Exception as e:
                print(f"Upload error: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())

# WebSocket Handler
async def handle_websocket(websocket):
    """Handle WebSocket messages with proper error handling"""
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                user_message = data.get('message', '')
                
                if not user_message:
                    await websocket.send(json.dumps({'error': 'Message is required'}))
                    continue
                
                print(f"Received message: {user_message}")
                
                # Load uploaded files from file
                file_context = load_file_context()
                
                # Load shared thoughts
                shared_thoughts = load_thoughts()
                
                # Build context from uploaded files
                context = ""
                if file_context:
                    context = "\n\nSystem Context (from uploaded documents):\n"
                    for file in file_context:
                        context += f"\n--- {file['name']} ---\n{file['content'][:2000]}\n"
                
                # Add shared thoughts context
                if shared_thoughts:
                    context += "\n\nShared Page Thoughts (from all users):\n"
                    for thought in shared_thoughts[-10:]:  # Last 10 thoughts
                        context += f"- {thought['message']}\n"
                
                # Combine user message with file context
                full_message = context + "\n\nUser: " + user_message if context else user_message
                
                # Get AI response with retry logic
                max_retries = 5
                retry_count = 0
                ai_response = None
                
                while retry_count < max_retries:
                    try:
                        response = client.models.generate_content(
                            model='gemini-2.5-flash-lite',
                            contents=full_message
                        )
                        ai_response = response.text
                        break
                    except Exception as e:
                        error_msg = str(e).lower()
                        if 'resource exhausted' in error_msg or 'quota' in error_msg:
                            retry_count += 1
                            wait_time = 2 ** retry_count  # Exponential backoff
                            print(f"Resource exhausted, retrying in {wait_time}s... (attempt {retry_count}/{max_retries})")
                            await asyncio.sleep(wait_time)
                        else:
                            raise e
                
                if ai_response is None:
                    ai_response = "Sorry, the AI service is currently overloaded. Please try again in a moment."
                
                print(f"AI response: {ai_response[:100]}...")
                
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
                
                # Send response back
                await websocket.send(json.dumps({
                    'success': True,
                    'user_message': user_message,
                    'ai_response': ai_response
                }))
                
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
            except Exception as e:
                print(f"Error processing message: {e}")
                try:
                    await websocket.send(json.dumps({'error': str(e)}))
                except:
                    pass
                    
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    except Exception as e:
        print(f"Connection error: {e}")

# Run HTTP server in separate thread
def run_http_server():
    http_server = HTTPServer(('0.0.0.0', 5000), RequestHandler)
    print('HTTP server running on http://localhost:5000')
    http_server.serve_forever()

# Run WebSocket server
async def run_websocket_server():
    async with websockets.serve(handle_websocket, "localhost", 8765):
        print("WebSocket server running on ws://localhost:8765")
        await asyncio.Future()  # run forever

# Main function to run both servers
async def main():
    # Start HTTP server in background thread
    http_thread = Thread(target=run_http_server, daemon=True)
    http_thread.start()
    
    # Run WebSocket server
    await run_websocket_server()

if __name__ == '__main__':
    print("Starting combined server...")
    print("- HTTP on port 5000 (file uploads)")
    print("- WebSocket on port 8765 (chat)")
    asyncio.run(main())

