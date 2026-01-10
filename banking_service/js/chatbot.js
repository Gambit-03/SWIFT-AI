document.addEventListener('DOMContentLoaded', () => {
    // Inject Styles
    const style = document.createElement('style');
    style.innerHTML = `
        .swift-chat-widget {
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 10000;
            font-family: 'Inter', sans-serif;
        }
        .chat-btn {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: white;
            border: none;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
            cursor: pointer;
            transition: transform 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }
        .chat-btn:hover { transform: scale(1.1); }
        
        .chat-window {
            position: absolute;
            bottom: 80px;
            right: 0;
            width: 350px;
            height: 500px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            display: none;
            flex-direction: column;
            overflow: hidden;
            border: 1px solid #e5e7eb;
        }
        .dark-mode .chat-window {
            background: #1f2937;
            border-color: #374151;
            color: white;
        }
        
        .chat-header {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: white;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .chat-body {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .chat-input-area {
            padding: 15px;
            border-top: 1px solid #eee;
            display: flex;
            gap: 10px;
        }
        .chat-input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 20px;
            outline: none;
        }
        .chat-send {
            background: #6366f1;
            color: white;
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            cursor: pointer;
        }
        
        .msg {
            max-width: 80%;
            padding: 10px 15px;
            border-radius: 15px;
            font-size: 14px;
            line-height: 1.4;
        }
        .msg.bot {
            background: #f3f4f6;
            align-self: flex-start;
            color: #1f2937;
            border-bottom-left-radius: 2px;
        }
        .msg.user {
            background: #6366f1;
            color: white;
            align-self: flex-end;
            border-bottom-right-radius: 2px;
        }
        .dark-mode .msg.bot {
            background: #374151;
            color: #e5e7eb;
        }
    `;
    document.head.appendChild(style);

    // Inject HTML
    const widget = document.createElement('div');
    widget.className = 'swift-chat-widget';
    widget.innerHTML = `
        <div class="chat-window" id="chatWindow">
            <div class="chat-header">
                <div>
                    <h6 class="mb-0 fw-bold">Swift Assist AI</h6>
                    <small style="opacity:0.8">Online • Ready to help</small>
                </div>
                <button style="background:none;border:none;color:white" onclick="toggleChat()"><i class="fas fa-times"></i></button>
            </div>
            <div class="chat-body" id="chatBody">
                <div class="msg bot">Hello! I'm your AI assistant. Ask me about fraud stats, alerts, or blocked transactions.</div>
            </div>
            <div class="chat-input-area">
                <input type="text" class="chat-input" id="chatInput" placeholder="Type a message...">
                <button class="chat-send" onclick="sendMessage()"><i class="fas fa-paper-plane"></i></button>
            </div>
        </div>
        <button class="chat-btn" onclick="toggleChat()">
            <i class="fas fa-robot"></i>
        </button>
    `;
    document.body.appendChild(widget);

    // Enter Key Support
    document.getElementById('chatInput').addEventListener('keypress', function (e) {
        if (e.key === 'Enter') sendMessage();
    });
});

window.toggleChat = function () {
    const window = document.getElementById('chatWindow');
    window.style.display = window.style.display === 'flex' ? 'none' : 'flex';
};

window.sendMessage = async function () {
    const input = document.getElementById('chatInput');
    const body = document.getElementById('chatBody');
    const text = input.value.trim();
    if (!text) return;

    // User Message
    body.innerHTML += `<div class="msg user">${text}</div>`;
    input.value = '';
    body.scrollTop = body.scrollHeight;

    // Loading
    const loadingId = 'loading-' + Date.now();
    body.innerHTML += `<div class="msg bot" id="${loadingId}"><i class="fas fa-ellipsis-h"></i></div>`;
    body.scrollTop = body.scrollHeight;

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        const result = await response.json();

        document.getElementById(loadingId).remove();
        body.innerHTML += `<div class="msg bot">${result.response}</div>`;
        body.scrollTop = body.scrollHeight;
    } catch (e) {
        document.getElementById(loadingId).remove();
        body.innerHTML += `<div class="msg bot text-danger">Error connecting to AI.</div>`;
    }
};
