// Configuration

const serverUrl = SERVER_URL;
const wsUrl = WS_URL;

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const chatSendBtn = document.getElementById('chatSendBtn');

const thoughtsMessages = document.getElementById('thoughtsMessages');
const thoughtInput = document.getElementById('thoughtInput');
const thoughtSendBtn = document.getElementById('thoughtSendBtn');

const fileList = document.getElementById('fileList');
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');

// State
let ws = null;
let uploadedFiles = [];
let pollInterval = null;

// ===== WEBSOCKET CHAT =====
async function loadChatHistory() {
    try {
        const response = await fetch(`${SERVER_URL}/get_messages`);
        const data = await response.json();
        
        if (!chatMessages) return;
        chatMessages.innerHTML = '';
        
        data.messages.forEach(msg => {
            const bubble = document.createElement('div');
            bubble.className = `chat-bubble ${msg.type}-bubble`;
            bubble.innerHTML = `<strong>${msg.type === 'user' ? 'You' : 'Witch'}:</strong><p>${msg.message}</p>`;
            chatMessages.appendChild(bubble);
        });
        
        chatMessages.scrollTop = chatMessages.scrollHeight;
        console.log(`Loaded ${data.messages.length} chat messages`);
    } catch (error) {
        console.error('Failed to load chat history:', error);
    }
}

function connectWebSocket() {
    ws = new WebSocket(WS_URL);
    
    ws.onopen = () => {
        console.log('WebSocket connected');
        loadChatHistory(); // Load history when connected
    };
    
    ws.onmessage = (event) => {
        console.log('WebSocket message received:', event.data);
        const data = JSON.parse(event.data);
        if (data.ai_response) {
            addChatBubble('ai', data.ai_response);
        }
    };
    
    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };
    
    ws.onclose = () => {
        console.log('WebSocket closed, reconnecting...');
        setTimeout(connectWebSocket, 1000);
    };
}

function addChatBubble(type, message) {
    console.log('Adding chat bubble:', type, message);
    if (!chatMessages) {
        console.error('chatMessages element not found!');
        return;
    }
    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${type}-bubble`;
    bubble.innerHTML = `<strong>${type === 'user' ? 'You' : 'Witch'}:</strong><p>${message}</p>`;
    chatMessages.appendChild(bubble);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    console.log('Chat bubble added, total bubbles:', chatMessages.children.length);
}

function sendChatMessage() {
    const message = chatInput.textContent.trim();
    console.log('Sending message:', message);
    chatInput.textContent = '';
    
    if (message && ws && ws.readyState === WebSocket.OPEN) {
        addChatBubble('user', message);
        ws.send(JSON.stringify({ message }));
        console.log('Message sent to WebSocket');
    } else {
        console.error('Cannot send message. WS state:', ws?.readyState, 'Message:', message);
    }
}

if (chatSendBtn) {
    chatSendBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        sendChatMessage();
    });
}

if (chatInput) {
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            e.stopPropagation();
            sendChatMessage();
        }
    });
}

// ===== SHARED THOUGHTS =====
async function loadThoughts() {
    try {
        const response = await fetch(`${SERVER_URL}/get_thoughts`);
        const data = await response.json();
        
        thoughtsMessages.innerHTML = '';
        data.thoughts.forEach(thought => {
            const bubble = document.createElement('div');
            bubble.className = 'thought-bubble';
            bubble.innerHTML = `<strong>Mortals thought:</strong> ${thought.message}`;
            thoughtsMessages.appendChild(bubble);
        });
        
        thoughtsMessages.scrollTop = thoughtsMessages.scrollHeight;
    } catch (error) {
        console.error('Failed to load thoughts:', error);
    }
}

async function sendThought() {
    const message = thoughtInput.textContent.trim();
    thoughtInput.textContent = '';
    
    if (message) {
        try {
            await fetch(`${SERVER_URL}/add_thought`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });
            
            loadThoughts();
        } catch (error) {
            console.error('Failed to send thought:', error);
        }
    }
}

if (thoughtSendBtn) {
    thoughtSendBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        sendThought();
    });
}

if (thoughtInput) {
    thoughtInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            e.stopPropagation();
            sendThought();
        }
    });
}

// ===== FILE UPLOAD =====
async function loadFiles() {
    try {
        const response = await fetch(`${SERVER_URL}/get_files`);
        const data = await response.json();
        uploadedFiles = data.files || [];
        displayFiles();
    } catch (error) {
        console.error('Failed to load files:', error);
        displayFiles(); // Display empty list
    }
}

function displayFiles() {
    if (!fileList) return;
    fileList.innerHTML = uploadedFiles.map((file, index) => `
        <div class="file-item">
            <span class="file-name">${file.name}</span>
            <button class="delete-icon" onclick="deleteFile(${index})" title="Delete" aria-label="Delete file"></button>
        </div>
    `).join('');
}

window.deleteFile = async function(index) {
    const fileItem = document.querySelector(`.file-item:nth-child(${index + 1})`);
    if (!fileItem) return;
    
    // Get file item position relative to viewport
    const rect = fileItem.getBoundingClientRect();
    
    // Create hand element as overlay
    const hand = document.createElement('img');
    hand.src = 'hand.png';
    hand.className = 'grabbing-hand-overlay';
    hand.style.top = `${rect.top + rect.height/2}px`;
    document.body.appendChild(hand);
    
    // Start file animation
    fileItem.classList.add('deleting');
    
    // Delete when hand grabs (at 50% of animation = 1 second)
    setTimeout(async () => {
        uploadedFiles.splice(index, 1);
        
        try {
            await fetch(`${SERVER_URL}/upload_context`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ files: uploadedFiles })
            });
        } catch (error) {
            console.error('Failed to update context:', error);
        }
        
        displayFiles();
    }, 1000);
    
    // Clean up hand after full animation
    setTimeout(() => {
        if (document.body.contains(hand)) {
            document.body.removeChild(hand);
        }
    }, 2000);
};

if (uploadBtn && fileInput) {
    uploadBtn.addEventListener('click', () => {
        fileInput.click();
    });
}

fileInput.addEventListener('change', async (e) => {
    const files = Array.from(e.target.files);
    
    for (const file of files) {
        const reader = new FileReader();
        reader.onload = async (event) => {
            const content = event.target.result;
            const fileData = {
                name: file.name,
                content: content,
                type: file.type,
                size: file.size
            };
            
            uploadedFiles.push(fileData);
            
            try {
                await fetch(`${SERVER_URL}/upload_context`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ files: uploadedFiles })
                });
                console.log(`Uploaded: ${file.name}`);
            } catch (error) {
                console.error('Failed to save context:', error);
            }
            
            displayFiles();
        };
        
        // Read PDF as base64, text files as text
        if (file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')) {
            reader.readAsDataURL(file);
        } else {
            reader.readAsText(file);
        }
    }
    
    fileInput.value = '';
});

// ===== INITIALIZATION =====
console.log('Initializing client app...');
console.log('DOM Elements:', {
    chatMessages: !!chatMessages,
    chatInput: !!chatInput,
    chatSendBtn: !!chatSendBtn,
    thoughtsMessages: !!thoughtsMessages,
    thoughtInput: !!thoughtInput,
    thoughtSendBtn: !!thoughtSendBtn,
    fileList: !!fileList,
    fileInput: !!fileInput,
    uploadBtn: !!uploadBtn
});

connectWebSocket();
loadThoughts();
loadFiles();

// Poll for new thoughts, files, and chat messages every 2 seconds
pollInterval = setInterval(() => {
    loadThoughts();
    loadFiles();
    if (ws && ws.readyState !== WebSocket.OPEN) {
        loadChatHistory(); // Sync chat if WebSocket is disconnected
    }
}, 2000);

console.log('Client app initialized');
