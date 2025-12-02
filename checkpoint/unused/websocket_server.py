import asyncio
import websockets
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

async def handle_message(websocket):
    """Handle WebSocket messages"""
    async for message in websocket:
        try:
            data = json.loads(message)
            user_message = data.get('message', '')
            
            if not user_message:
                await websocket.send(json.dumps({'error': 'Message is required'}))
                continue
            
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
            
            # Send response back
            await websocket.send(json.dumps({
                'success': True,
                'user_message': user_message,
                'ai_response': ai_response
            }))
            
        except Exception as e:
            await websocket.send(json.dumps({'error': str(e)}))

async def main():
    async with websockets.serve(handle_message, "localhost", 8765):
        print("WebSocket server running on ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())
