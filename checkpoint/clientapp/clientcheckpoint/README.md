# Witch Chat - Client App

This is a standalone client application that connects to the Witch Chat server.

## Features

- **Shared Witch Chat**: All clients see the same AI responses
- **Page Thoughts**: Shared chat visible to all users and included in AI context
- **File Offerings**: Upload documents that become context for the AI

## How to Use

1. Make sure the server is running:
   ```bash
   python combined_server.py
   ```

2. Open `client.html` in a web browser:
   - You can open it directly (file://)
   - Or serve it via the server at: `http://localhost:5000/clientapp/client.html`

3. Multiple clients can connect simultaneously and share:
   - Chat messages with the witch
   - Thoughts in the shared section
   - Uploaded documents

## Architecture

- **client.html**: UI layout and styling
- **client.js**: Client-side logic
- Connects to:
  - HTTP server on port 5000 (file uploads, thoughts)
  - WebSocket server on port 8765 (real-time chat)

## Shared Data

All data is synchronized across clients:
- Chat messages stored in `messages.json`
- Shared thoughts stored in `shared_thoughts.json`
- Uploaded files stored in `file_context.json` and `uploaded_files/`
