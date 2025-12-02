<pre>
# Witch Chat Interface - AI-Powered Multi-Client Chat Application

AFTER CLONE, DELETE THE '-' in front of .kiro and other kiro workfolders so kiro can use them.
ALL ASSETS ARE AI GENERATED AND ANY RESEMBLANCE ARE COINCIDENCE
MUSIC USED IS NOT COPYRIGHTED 
A mystical-themed, real-time AI chat application with video call integration, document context awareness, and multi-client collaboration features.

## 🎃 What is This Project?

Witch Chat Interface is a collaborative AI assistant platform where multiple users can:
- Chat with an AI "witch" powered by Google Gemini
- Share documents (PDFs, text files) that provide context to the AI
- Collaborate through shared "page thoughts" visible to all users
- Conduct video calls via integrated LintasEdu SDK
- Experience a mystical, Halloween-themed interface

Dear Judges, please visit 'https://kiro.lintasedu.com//client.html' for easier access to our demo (fully working!) 
using the website above will save you from the hassle of setting up py dependency and changing config.js and .env to localhost.
use https://kiro.lintasedu.com if the first link did not work.

## 📁 Project Structure

**All working files are in the `clientapp/` folder.**

- `clientapp/` - **Complete application** (ready to deploy)
- `unused/` - Deprecated files and old implementations
- `checkpoint/` - Backup snapshots

**Note**: `iframeindex.html` in the main directory is a **reference implementation only** and is not used in production. The active application is `clientapp/index.html`.

## 🏗️ Architecture

### Application Layout

The application (`clientapp/index.html`) uses a three-column layout:

```
┌─────────────┬──────────────────┬─────────────┐
│   SDK       │   Witch Image    │  Sidebar    │
│  (Video)    │   + Chat         │  (Files +   │
│  25% width  │   50% width      │   Thoughts) │
│             │                  │  25% width  │
└─────────────┴──────────────────┴─────────────┘
```

- **Left**: LintasEdu SDK for video calls (iframe)
- **Center**: Witch image with chat overlay at bottom
- **Right**: File uploads (top 30%) + Shared thoughts (bottom 70%)

## 🚀 How It Works

### Real-Time Communication

1. **WebSocket Chat** (Port 8765)
   - User sends message → WebSocket → Server
   - Server adds file context + shared thoughts
   - Google Gemini AI generates response
   - Response sent back via WebSocket
   - All messages saved to `messages.json`

2. **HTTP Polling** (Port 5000)
   - Shared thoughts poll every 2 seconds
   - File list polls every 2 seconds
   - Ensures all clients stay synchronized

3. **File Upload**
   - User uploads PDF/text file
   - Server extracts text from PDFs (using pypdf)
   - Text saved to `uploaded_files/` directory
   - File context included in all AI conversations

### Data Synchronization

All clients share the same server data:
- **Chat messages** (`messages.json`) - Synced via WebSocket + HTTP polling
- **Shared thoughts** (`shared_thoughts.json`) - Synced via HTTP polling
- **Uploaded files** (`file_context.json` + `uploaded_files/`) - Synced via HTTP polling

### AI Context

When the AI responds, it receives:
1. **Uploaded documents** - Up to 5000 characters per file
2. **Last 10 shared thoughts** - From all users
3. **Current user message**

This allows the AI to provide context-aware responses based on shared documents and collaborative input.

## 📦 Backend Server

### Server Location

The backend server is located at **`clientapp/combined_server.py`**.

This server can run in two modes:
1. **Localhost** - Configure `.env` file for local development
2. **Production** - Deploy to your backend infrastructure with appropriate `.env` settings

### Server Responsibilities

**HTTP Server (Port 5000)**
- Serves static files (HTML, CSS, JS, images)
- Handles file uploads (`POST /upload_context`)
- Manages shared thoughts (`GET /get_thoughts`, `POST /add_thought`)
- Provides file list (`GET /get_files`)
- Provides chat history (`GET /get_messages`)

**WebSocket Server (Port 8765)**
- Real-time chat communication
- Receives user messages
- Sends AI responses
- Maintains persistent connections

### Environment Configuration

**All configuration is in `clientapp/.env`**

Create `clientapp/.env` file:
```env
HTTP_HOST=0.0.0.0
HTTP_PORT=5000
WS_HOST=0.0.0.0
WS_PORT=8765
GEM_API=your_google_gemini_api_key_here
```

For localhost development:
```env
HTTP_HOST=localhost
HTTP_PORT=5000
WS_HOST=localhost
WS_PORT=8765
GEM_API=your_api_key
```

The client frontend uses `clientapp/config.js` to point to the server:
```javascript
const SERVER_URL = 'http://localhost:5000';  // use this for localhost deployment
const WS_URL = 'ws://localhost:8765';        // use this for locahost deployment
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- Google Gemini API key
- Modern web browser

### Backend Setup

1. **Navigate to clientapp folder**
```bash
cd clientapp
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

Required packages:
- `google-genai` - Google Gemini AI API
- `websockets` - WebSocket server
- `pypdf` - PDF text extraction
- `python-dotenv` - Environment variables

3. **Configure environment**

Create `.env` file in `clientapp/` folder:
```env
HTTP_HOST=localhost
HTTP_PORT=5000
WS_HOST=localhost
WS_PORT=8765
GEM_API=your_google_gemini_api_key_here
```

4. **Run the server**
```bash
python combined_server.py
```

The server will start both HTTP (port 5000) and WebSocket (port 8765) services.

### Frontend Setup

1. **Configure client endpoints**

Edit `clientapp/config.js` to match your `.env` settings:
```javascript
const SERVER_URL = 'http://localhost:5000';  // Match HTTP_HOST:HTTP_PORT if u want to use smth else
const WS_URL = 'ws://localhost:8765';        // Match WS_HOST:WS_PORT if u want to use smth else
```

2. **Access the application**
- Open browser: `http://localhost:5000/index.html`
- Or simply: `http://localhost:5000` (index.html is served by default)

## 📖 User Guide

### Getting Started

1. **Open the application**
   - Navigate to `http://localhost:5000` (or your deployed URL)
   - The application loads automatically

2. **Start video call**
   - Click "Hubungi Kami" in left panel
   - LintasEdu SDK will load for video communication

3. **Upload context documents**
   - Click "Offer to Witch" button (💀) in right sidebar
   - Select PDF or text files
   - Files are processed and added to AI context

### Using the Application

**Chat with AI**
- Type message in chat input at bottom of witch image
- Press "Send" or Enter
- AI responds with context from uploaded documents
- All users see the same chat history

**Share Thoughts**
- Use "Mindreading Skull" section in right sidebar
- Type your thought and press 💭 or Enter
- Thoughts visible to all users and included in AI context

**Collaborate**
- Multiple users can connect simultaneously
- All share the same chat, thoughts, and documents
- Changes sync automatically every 2 seconds

### Features

**File Upload**
- Click "Offer to Witch" button (💀)
- Select PDF or text files
- Files automatically processed and added to AI context
- Delete files by clicking tombstone icon (🪦)
- Animated hand grabs files when deleted

**Shared Thoughts**
- Type in "Mindreading Skull" section
- Press 💭 button or Enter to send
- Thoughts appear for all users
- Last 10 thoughts included in AI context

**Chat**
- Type message in chat input
- Press "Send" or Enter
- AI responds with context awareness
- Chat history persists across sessions

## 🎨 Customization

### Themes & Assets

Replace these files in `clientapp/` to customize appearance:
- `witch asset.jpg` - Main witch image
- `KIROWEEN.png` - Top bar logo
- `skullused.png` - Decorative skull
- `tombstone.png` - Delete icon
- `hand.png` - Grabbing hand animation

### Styling

All styles are inline in `clientapp/index.html` for easy customization.

## 🔧 Technical Details

### File Structure

```
├── clientapp/                    # 🎯 MAIN APPLICATION FOLDER
│   ├── index.html               # Main HTML file
│   ├── client.js                # Client-side logic
│   ├── config.js                # Server endpoint configuration
│   ├── combined_server.py       # Backend server
│   ├── .env                     # Environment variables (create this)
│   ├── hackathon.html           # LintasEdu SDK loader
│   ├── requirements.txt         # Python dependencies
│   ├── witch asset.jpg          # Main witch image
│   ├── KIROWEEN.png             # Top bar logo
│   ├── skullused.png            # Decorative skull
│   ├── tombstone.png            # Delete icon
│   ├── hand.png                 # Grabbing hand animation
│   └── [other assets]           # Additional images
├── checkpoint/                   # Backup snapshots
├── unused/                       # Deprecated/reference files
│   ├── iframeindex.html         # Old reference implementation
│   └── [other old files]        # Not used in production
└── README.md                     # This file
```

**Important**: Everything you need is in the `clientapp/` folder!

### Data Files (Generated at Runtime)

- `messages.json` - Chat history (shared across all clients)
- `shared_thoughts.json` - Shared page thoughts
- `file_context.json` - Uploaded file metadata
- `uploaded_files/` - Original files + extracted text

### Browser Compatibility

- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ⚠️ WebSocket may require configuration

### Known Issues

1. **"Reload site?" popup**
   - Should be pretty rare since last fix
   - Caused by external LintasEdu SDK
   - Cannot be disabled from this codebase
   - Click "Cancel" to stay on page

2. **CORS errors**
   - Ensure server has proper CORS headers
   - Check `config.js` URLs match your backend

3. **WebSocket disconnections**
   - Auto-reconnects after 1 second
   - Chat history syncs via HTTP polling

## 🔐 Security Notes

- API keys should be stored in environment variables
- File uploads limited to PDF and text files
- File content truncated to 5000 characters for AI context
- CORS enabled for development (restrict in production)

## 🤝 Contributing

This project was built for a hackathon. Feel free to:
- Fork and modify for your needs
- Report issues or suggestions
- Improve documentation

## 📄 License

This project is provided as-is for educational and hackathon purposes.

## 🙏 Credits

- **Google Gemini API** - AI responses
- **LintasEdu SDK** - Video call functionality
- **pypdf** - PDF text extraction
- **websockets** - Real-time communication
- **kiro** - For the AI powered IDE that help built this

---

**Built with Kiro🎃 for hackathon collaboration**

<pre>



