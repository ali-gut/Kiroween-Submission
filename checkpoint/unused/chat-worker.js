// Web Worker for chat - completely isolated from main thread
let ws = null;
let messageQueue = [];

self.onmessage = function(e) {
    const { type, data } = e.data;
    
    if (type === 'connect') {
        connectWebSocket();
    } else if (type === 'send') {
        sendMessage(data);
    }
};

function connectWebSocket() {
    ws = new WebSocket('ws://localhost:8765');
    
    ws.onopen = function() {
        self.postMessage({ type: 'connected' });
        // Send queued messages
        while (messageQueue.length > 0) {
            ws.send(messageQueue.shift());
        }
    };
    
    ws.onmessage = function(event) {
        const data = JSON.parse(event.data);
        self.postMessage({ type: 'message', data: data });
    };
    
    ws.onerror = function(error) {
        self.postMessage({ type: 'error', error: error.toString() });
    };
    
    ws.onclose = function() {
        self.postMessage({ type: 'closed' });
        setTimeout(connectWebSocket, 1000);
    };
}

function sendMessage(message) {
    const msg = JSON.stringify({ message: message });
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(msg);
    } else {
        messageQueue.push(msg);
    }
}
