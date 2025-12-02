# Witch Chat Interface - Multi-Client AI Chat System

A mystical-themed multi-client chat application with AI integration, document processing, and real-time synchronization.

## Quick Start

### For Deployers (Server Setup)

#### Option 1: One-Click Launch (Recommended)
- **Windows**: Double-click `start_server.bat` (starts on port 5500)
- **Mac/Linux**: Double-click `start_server.sh` (or run `chmod +x start_server.sh` first)

#### Option 2: Manual Setup
1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Start the combined server:**
```bash
python combined_server.py
```

3. **Server will start on:**
- **HTTP Server**: `http://localhost:5000` (file serving, uploads, API)
- **WebSocket Server**: `ws://localhost:8765` (real-time chat)

4. **Share the URL with users:**
- Give users: `http://localhost:5000/clientapp/client.html`

### For Users (Access Application)

1. **Open the application:**
- **🎯 RECOMMENDED**: `http://localhost:5000/clientapp/client.html` *(Complete version)*
- **Legacy**: `http://localhost:5000` *(Original main app)*

2. **No installation needed** - just open the URL in your browser!

> **⚠️ Important**: Use `clientapp/client.html` - this is the finished, polished version with all features!

## Features

### 🎭 Multi-Client System
- **Synchronized data** across all connected clients
- **Real-time updates** for chat, thoughts, and file uploads
- **Standalone client app** with identical functionality

### 🤖 AI Integration
- **Google Gemini API** for intelligent responses
- **Context-aware AI** using uploaded documents
- **Shared thoughts integration** - AI sees all user thoughts
- **PDF text extraction** for document context

### 🎨 User Interface
- **Dark mystical theme** with professional styling
- **Three-column layout**: SDK (25%) + Witch (50%) + Sidebar (25%)
- **Animated interactions** with grabbing hand effects
- **Custom KIROWEEN branding** in topbar

### 📁 File Management
- **PDF text extraction** using pypdf library
- **Document context** automatically added to AI conversations
- **Animated file deletion** with hand grabbing effect
- **Tombstone delete buttons** for thematic consistency

### 💭 Mindreading Skull
- **Shared thoughts system** visible to all clients
- **Speech bubble design** connecting to skull image
- **Real-time synchronization** across all users
- **AI context integration** - thoughts influence AI responses

### 🎥 Video Integration
- **LintasEdu SDK** for video calling functionality
- **Isolated iframe** prevents interference with main app
- **Session protection** (causes reload warnings - external SDK behavior)

## Architecture

### Server Components
- **Combined Server**: HTTP + WebSocket on ports 5000 & 8765
- **File Processing**: PDF text extraction and storage
- **Real-time Sync**: WebSocket for chat, HTTP polling for thoughts/files
- **Context Management**: Uploaded files and thoughts feed AI

### Client Applications
- **Main App**: Full-featured with iframe isolation
- **Client App**: Standalone version for multiple users
- **Synchronized Data**: All clients share same chat, thoughts, and files

### File Structure
```
├── Main Application
│   ├── iframeindex.html      # Main interface
│   ├── chat-iframe.html      # Isolated chat
│   ├── rightbar.html         # Sidebar (files + thoughts)
│   └── hackathon.html        # SDK loader
├── Client Application
│   ├── clientapp/client.html # Standalone client
│   ├── clientapp/client.js   # Client logic
│   └── clientapp/assets/     # Images (hand, skull, logo, etc.)
├── Server
│   ├── combined_server.py    # Main server
│   ├── messages.json         # Chat history
│   ├── shared_thoughts.json  # Shared thoughts
│   ├── file_context.json     # File metadata
│   └── uploaded_files/       # PDF storage + extracted text
└── Styling
    └── style.css             # Global styles
```

## Usage Guide

### 🎯 Recommended Usage (Client App)
1. **Open**: `http://localhost:5000/clientapp/client.html`
2. **Video Call**: Click "Hubungi Kami" in left panel
3. **Upload Files**: Use "Offer to Witch" section (animated deletion!)
4. **Share Thoughts**: Use "Mindreading Skull" for group chat
5. **Chat with AI**: AI sees all uploaded files and shared thoughts
6. **Multiple Users**: Open same URL in multiple browsers for collaboration

### Legacy Main App (Optional)
- Available at `http://localhost:5000`
- Uses iframe architecture
- Less polished than client app

### Multi-Client Features
- **Shared Chat**: All users see same AI conversation
- **Shared Thoughts**: "Mindreading Skull" visible to everyone
- **Shared Files**: Uploaded documents available to all
- **Real-time Sync**: Changes appear instantly on all clients

## Technical Details

### Dependencies
- `google-genai` - Google Gemini AI API
- `websockets` - Real-time chat communication
- `pypdf` - PDF text extraction

### Ports
- **5000**: HTTP server (file serving, uploads, thoughts API)
- **8765**: WebSocket server (real-time chat)

### Data Flow
1. **Chat**: WebSocket → AI → All clients
2. **Thoughts**: HTTP POST → Server → HTTP polling (all clients)
3. **Files**: HTTP upload → PDF extraction → AI context
4. **Sync**: 2-second polling for thoughts and files

## Known Issues

⚠️ **"Reload site?" popup** - Caused by LintasEdu SDK's session protection (external behavior, cannot be modified)

## Customization

- **Branding**: Replace `KIROWEEN.png` with your logo
- **Animations**: Modify CSS keyframes in client.html
- **AI Model**: Change model in combined_server.py
- **Styling**: Update colors and themes in CSS files
