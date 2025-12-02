// Chat handler - separate from SDK
const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const chatMessages = document.getElementById('chatMessages');

// Auto-play music on first user interaction
const audio = document.querySelector('audio');
const playMusic = () => {
    audio.play().catch(e => console.log('Audio play failed:', e));
    document.removeEventListener('click', playMusic);
    document.removeEventListener('keydown', playMusic);
};
document.addEventListener('click', playMusic);
document.addEventListener('keydown', playMusic);

// Load previous messages from localStorage
function loadMessages() {
    const saved = localStorage.getItem('chatHistory');
    if (saved) {
        const messages = JSON.parse(saved);
        messages.forEach(msg => {
            const bubble = document.createElement('div');
            if (msg.type === 'user') {
                bubble.className = 'chat-bubble user-bubble';
                bubble.innerHTML = `<p><strong>You:</strong> ${msg.message}</p>`;
            } else {
                bubble.className = 'chat-bubble ai-bubble';
                bubble.innerHTML = `<p><strong>Witch:</strong> ${msg.message}</p>`;
            }
            chatMessages.appendChild(bubble);
        });
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

// Save message to localStorage
function saveToLocal(type, message) {
    const saved = localStorage.getItem('chatHistory');
    const messages = saved ? JSON.parse(saved) : [];
    messages.push({ type, message });
    localStorage.setItem('chatHistory', JSON.stringify(messages));
}

// Load messages on page load
loadMessages();

// Handle message sending
async function sendMessage() {
    const message = userInput.value.trim();
    
    if (message) {
        // Display user message bubble
        const userBubble = document.createElement('div');
        userBubble.className = 'chat-bubble user-bubble';
        userBubble.innerHTML = `<p><strong>You:</strong> ${message}</p>`;
        chatMessages.appendChild(userBubble);
        saveToLocal('user', message);

        userInput.value = '';

        // Send to Python backend
        try {
            const response = await fetch('http://localhost:5000/save_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            console.log('Response:', data);
            
            if (response.ok && data.ai_response) {
                // Display AI response bubble
                const aiBubble = document.createElement('div');
                aiBubble.className = 'chat-bubble ai-bubble';
                aiBubble.innerHTML = `<p><strong>Witch:</strong> ${data.ai_response}</p>`;
                chatMessages.appendChild(aiBubble);
                saveToLocal('ai', data.ai_response);
                
                // Scroll to bottom smoothly without triggering reflow
                requestAnimationFrame(() => {
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                });
            } else {
                console.error('Error in response:', data);
                alert('Error: ' + (data.error || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error saving message:', error);
            alert('Failed to connect to server: ' + error.message);
        }
    }
}

// Attach event listeners
document.getElementById('sendBtn').addEventListener('click', sendMessage);
chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    sendMessage();
});
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});
