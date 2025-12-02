import asyncio
import websockets
import json
from datetime import datetime
import os
from google import genai

# Configure Google Gemini API
client = genai.Client(api_key='AIzaSyA-hvrLKoYItByTN3-SAsrftMLZvdkP7LA')

# File to store messages and context
MESSAGES_FILE = 'messages.json'
CONTEXT_FILE = 'file_context.json'

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

async def handle_message(websocket):
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
                
                # Build context from uploaded files
                context = ""
                if file_context:
                    context = "\n\nSystem Context (from uploaded documents):\n"
                    for file in file_context:
                        context += f"\n--- {file['name']} ---\n{file['content'][:2000]}\n"
                
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

async def main():
    async with websockets.serve(handle_message, "localhost", 8765):
        print("WebSocket server running on ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())
