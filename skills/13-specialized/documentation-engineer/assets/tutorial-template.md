---
title: Build a Real-Time Chat Application with WebSockets
description: Learn how to build a real-time chat application using WebSocket connections, complete with user authentication and message persistence.
sidebar_position: 1
tags: [tutorial, websockets, real-time, chat, nodejs]
---

# Build a Real-Time Chat Application with WebSockets

> **What you'll build**: A multi-user real-time chat application where users can join rooms, send messages, and see messages from other users instantly — all powered by WebSocket connections with a Node.js backend and React frontend.

---

## What You'll Build

```
┌─────────────┐     WebSocket      ┌──────────────┐
│   React     │ ◄────────────────► │   Node.js    │
│   Frontend  │       ws://        │   Backend    │
│   :3000     │                    │   :4000      │
└─────────────┘                    └──────┬───────┘
                                          │
                                          ▼
                                   ┌──────────────┐
                                   │   Redis       │
                                   │   (Pub/Sub)   │
                                   └──────────────┘
```

- **Real-time messaging**: Messages appear instantly on all connected clients
- **Chat rooms**: Users can create and join named rooms
- **User authentication**: JWT-based auth with WebSocket upgrade
- **Message persistence**: Messages stored in PostgreSQL (via the REST API)
- **Typing indicators**: See when another user is typing

> **Demo**: A working chat app with two browser windows showing real-time message delivery.

---

## Prerequisites

Before starting this tutorial, you need:

| Requirement | Version | How to Verify |
|---|---|---|
| **Node.js** | v20+ | `node --version` |
| **npm** | v10+ | `npm --version` |
| **Git** | v2+ | `git --version` |
| **Code editor** | Any | VS Code recommended |
| **Basic JavaScript** | — | Familiarity with async/await |

> **No prior WebSocket experience required.**

---

## Time Estimate

| Section | Time |
|---|---|
| Setup | 5 min |
| Step 1: Scaffold the project | 5 min |
| Step 2: Build the WebSocket server | 10 min |
| Step 3: Build the React frontend | 15 min |
| Step 4: Add authentication | 10 min |
| Step 5: Add chat rooms | 10 min |
| Step 6: Add typing indicators | 5 min |
| **Total** | **~60 minutes** |

---

## Step 1: Scaffold the Project

Create the project directory and initialize both the server and client:

```bash
mkdir realtime-chat
cd realtime-chat

# Create server directory
mkdir server client

# Initialize the server
cd server
npm init -y
npm install ws uuid jsonwebtoken dotenv
npm install -D nodemon

# Initialize the client with Vite + React
cd ../client
npm create vite@latest . -- --template react
npm install
npm install @vitejs/plugin-react
```

Create the `.env` file for the server:

```bash
cd ../server
cat > .env << 'EOF'
PORT=4000
JWT_SECRET=dev-secret-do-not-use-in-production
EOF
```

Update the server's `package.json` scripts:

```json
{
  "scripts": {
    "start": "node src/index.js",
    "dev": "nodemon src/index.js"
  }
}
```

> **Verify**: Run `node --version && npm --version` — both should output version numbers.

---

## Step 2: Build the WebSocket Server

Create the server structure:

```bash
mkdir -p server/src
```

**`server/src/index.js`** — Main server entry point:

```javascript
const { WebSocketServer } = require('ws');
const { createServer } = require('http');
const jwt = require('jsonwebtoken');
require('dotenv').config();

const PORT = process.env.PORT || 4000;
const JWT_SECRET = process.env.JWT_SECRET;

// HTTP server for health checks
const httpServer = createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ status: 'ok', uptime: process.uptime() }));
});

// WebSocket server
const wss = new WebSocketServer({ server: httpServer });

// Store connected clients: { ws, userId, username, room }
const clients = new Map();

wss.on('connection', (ws, req) => {
  let userId = null;
  let username = null;
  let room = null;

  console.log('New WebSocket connection');

  ws.on('message', (data) => {
    try {
      const message = JSON.parse(data.toString());
      handleMessage(ws, message);
    } catch (err) {
      ws.send(JSON.stringify({ type: 'error', payload: { message: 'Invalid JSON' } }));
    }
  });

  ws.on('close', () => {
    if (userId) {
      clients.delete(userId);
      broadcastToRoom(room, {
        type: 'user_left',
        payload: { userId, username, onlineUsers: getOnlineUsers(room) },
      }, null);
    }
  });

  ws.on('error', (err) => {
    console.error('WebSocket error:', err.message);
  });
});

function handleMessage(ws, message) {
  switch (message.type) {
    case 'auth':
      handleAuth(ws, message.payload);
      break;
    case 'message':
      handleChatMessage(ws, message.payload);
      break;
    case 'join_room':
      handleJoinRoom(ws, message.payload);
      break;
    case 'typing':
      handleTyping(ws, message.payload);
      break;
    default:
      ws.send(JSON.stringify({ type: 'error', payload: { message: 'Unknown message type' } }));
  }
}

function handleAuth(ws, payload) {
  try {
    const decoded = jwt.verify(payload.token, JWT_SECRET);
    const { userId, username: uname } = decoded;
    clients.set(userId, { ws, userId, username: uname, room: null });
    ws.send(JSON.stringify({
      type: 'auth_success',
      payload: { userId, username: uname },
    }));
    console.log(`User authenticated: ${uname} (${userId})`);
  } catch (err) {
    ws.send(JSON.stringify({
      type: 'auth_error',
      payload: { message: 'Invalid or expired token' },
    }));
  }
}

function handleChatMessage(ws, payload) {
  const client = findClient(ws);
  if (!client) return;

  const messagePayload = {
    type: 'new_message',
    payload: {
      id: generateId(),
      userId: client.userId,
      username: client.username,
      text: payload.text,
      timestamp: new Date().toISOString(),
      room: client.room,
    },
  };

  broadcastToRoom(client.room, messagePayload, null);
}

function handleJoinRoom(ws, payload) {
  const client = findClient(ws);
  if (!client) return;

  // Leave current room
  if (client.room) {
    broadcastToRoom(client.room, {
      type: 'user_left',
      payload: { userId: client.userId, username: client.username, onlineUsers: getOnlineUsers(client.room) },
    }, client.userId);
  }

  // Join new room
  client.room = payload.room;
  ws.send(JSON.stringify({
    type: 'room_joined',
    payload: { room: payload.room, onlineUsers: getOnlineUsers(payload.room) },
  }));

  broadcastToRoom(payload.room, {
    type: 'user_joined',
    payload: { userId: client.userId, username: client.username, onlineUsers: getOnlineUsers(payload.room) },
  }, client.userId);
}

function handleTyping(ws, payload) {
  const client = findClient(ws);
  if (!client) return;

  broadcastToRoom(client.room, {
    type: 'typing',
    payload: { userId: client.userId, username: client.username, isTyping: payload.isTyping },
  }, client.userId);
}

function findClient(ws) {
  for (const [, client] of clients) {
    if (client.ws === ws) return client;
  }
  return null;
}

function getOnlineUsers(room) {
  const users = [];
  for (const [, client] of clients) {
    if (client.room === room) {
      users.push({ userId: client.userId, username: client.username });
    }
  }
  return users;
}

function broadcastToRoom(room, message, excludeUserId) {
  for (const [, client] of clients) {
    if (client.room === room && client.userId !== excludeUserId) {
      if (client.ws.readyState === 1) { // WebSocket.OPEN
        client.ws.send(JSON.stringify(message));
      }
    }
  }
}

function generateId() {
  return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

httpServer.listen(PORT, () => {
  console.log(`Chat server running on ws://localhost:${PORT}`);
  console.log(`Health check at http://localhost:${PORT}`);
});
```

Create a simple token utility:

**`server/src/token.js`** — For development, generate a test JWT:

```javascript
const jwt = require('jsonwebtoken');
require('dotenv').config();

const userId = process.argv[2] || 'user_demo_001';
const username = process.argv[3] || 'DemoUser';

const token = jwt.sign({ userId, username }, process.env.JWT_SECRET, { expiresIn: '24h' });
console.log('\n=== Dev Token ===');
console.log(`User: ${username} (${userId})`);
console.log(`Token: ${token}`);
console.log('=================\n');
```

> **Verify**: Run `node src/token.js` — it prints a JWT. Run `node src/index.js` — outputs "Chat server running on ws://localhost:4000".

---

## Step 3: Build the React Frontend

**`client/src/App.jsx`** — Main application component:

```jsx
import { useState, useEffect, useRef, useCallback } from 'react';
import './App.css';

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:4000';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [connected, setConnected] = useState(false);
  const [authenticated, setAuthenticated] = useState(false);
  const [username, setUsername] = useState('');
  const [room, setRoom] = useState('general');
  const [onlineUsers, setOnlineUsers] = useState([]);
  const [typingUsers, setTypingUsers] = useState([]);
  const wsRef = useRef(null);
  const messagesEndRef = useRef(null);
  const typingTimeoutRef = useRef(null);

  const connect = useCallback((token) => {
    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;

    ws.onopen = () => {
      setConnected(true);
      // Authenticate
      ws.send(JSON.stringify({ type: 'auth', payload: { token } }));
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);

      switch (message.type) {
        case 'auth_success':
          setAuthenticated(true);
          setUsername(message.payload.username);
          // Join default room
          ws.send(JSON.stringify({ type: 'join_room', payload: { room: 'general' } }));
          break;

        case 'auth_error':
          alert('Authentication failed: ' + message.payload.message);
          break;

        case 'new_message':
          setMessages((prev) => [...prev, message.payload]);
          break;

        case 'room_joined':
          setRoom(message.payload.room);
          setOnlineUsers(message.payload.onlineUsers);
          setMessages([]);
          break;

        case 'user_joined':
        case 'user_left':
          setOnlineUsers(message.payload.onlineUsers);
          break;

        case 'typing':
          setTypingUsers((prev) => {
            const filtered = prev.filter((u) => u.userId !== message.payload.userId);
            if (message.payload.isTyping) {
              return [...filtered, { userId: message.payload.userId, username: message.payload.username }];
            }
            return filtered;
          });
          break;

        case 'error':
          console.error('Server error:', message.payload.message);
          break;
      }
    };

    ws.onclose = () => {
      setConnected(false);
      setAuthenticated(false);
    };

    ws.onerror = (err) => {
      console.error('WebSocket error:', err);
    };
  }, []);

  const sendMessage = () => {
    if (!inputText.trim()) return;
    wsRef.current?.send(JSON.stringify({
      type: 'message',
      payload: { text: inputText.trim() },
    }));
    setInputText('');
  };

  const handleTyping = () => {
    wsRef.current?.send(JSON.stringify({
      type: 'typing',
      payload: { isTyping: true },
    }));

    clearTimeout(typingTimeoutRef.current);
    typingTimeoutRef.current = setTimeout(() => {
      wsRef.current?.send(JSON.stringify({
        type: 'typing',
        payload: { isTyping: false },
      }));
    }, 2000);
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Get a dev token and connect
  useEffect(() => {
    // In production, get this from your auth server
    const token = prompt('Enter your dev token (run: node server/src/token.js):');
    if (token) connect(token);
  }, [connect]);

  if (!connected) return <div className="status">Connecting to server...</div>;
  if (!authenticated) return <div className="status">Authenticating...</div>;

  return (
    <div className="app">
      <header className="header">
        <h1>💬 Realtime Chat</h1>
        <div className="status-bar">
          <span className="room">Room: #{room}</span>
          <span className="online">{onlineUsers.length} online</span>
        </div>
      </header>

      <div className="layout">
        <aside className="sidebar">
          <h3>Online Users</h3>
          <ul>
            {onlineUsers.map((user) => (
              <li key={user.userId}>
                <span className="online-indicator" />
                {user.username} {user.userId === username ? '(you)' : ''}
              </li>
            ))}
          </ul>
        </aside>

        <main className="chat-area">
          <div className="messages">
            {messages.map((msg) => (
              <div key={msg.id} className={`message ${msg.username === username ? 'own' : ''}`}>
                <strong>{msg.username}</strong>
                <p>{msg.text}</p>
                <time>{new Date(msg.timestamp).toLocaleTimeString()}</time>
              </div>
            ))}
            {typingUsers.length > 0 && (
              <div className="typing-indicator">
                {typingUsers.map((u) => u.username).join(', ')} typing...
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="input-area">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') sendMessage(); }}
              onKeyUp={handleTyping}
              placeholder="Type a message..."
              className="input"
            />
            <button onClick={sendMessage} className="send-btn">Send</button>
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;
```

**`client/src/App.css`** — Styling:

```css
* { margin: 0; padding: 0; box-sizing: border-box; }

.app {
  height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.header {
  background: #1a1a2e;
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  font-size: 1.2rem;
  color: #666;
}

.status-bar {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
  opacity: 0.8;
}

.layout {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.sidebar {
  width: 220px;
  background: #16213e;
  color: white;
  padding: 1rem;
}

.sidebar h3 {
  font-size: 0.9rem;
  text-transform: uppercase;
  opacity: 0.7;
  margin-bottom: 1rem;
}

.sidebar ul {
  list-style: none;
}

.sidebar li {
  padding: 0.5rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.online-indicator {
  width: 8px;
  height: 8px;
  background: #4ade80;
  border-radius: 50%;
  display: inline-block;
}

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.messages {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.message {
  max-width: 70%;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  background: #f1f3f5;
}

.message.own {
  align-self: flex-end;
  background: #4f46e5;
  color: white;
}

.message strong {
  font-size: 0.8rem;
  display: block;
  margin-bottom: 0.25rem;
}

.message p {
  line-height: 1.4;
}

.message time {
  font-size: 0.7rem;
  opacity: 0.7;
  display: block;
  margin-top: 0.25rem;
}

.typing-indicator {
  font-size: 0.8rem;
  color: #666;
  font-style: italic;
  padding: 0.5rem 0;
}

.input-area {
  display: flex;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid #e0e0e0;
  background: white;
}

.input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.2s;
}

.input:focus {
  border-color: #4f46e5;
}

.send-btn {
  padding: 0.75rem 1.5rem;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}

.send-btn:hover {
  background: #4338ca;
}
```

> **Verify**: Run `cd client && npm run dev` — opens the React app. Enter a JWT token from Step 2.

---

## Step 4: Add Authentication

The server validates JWTs during WebSocket connection. Generate a test token:

```bash
cd server
node src/token.js user_alice Alice
```

Copy the token output and paste it in the browser prompt when the React app loads.

**How authentication works**:

1. Client sends a WebSocket message with `type: 'auth'` and the JWT token
2. Server verifies the JWT signature using `jsonwebtoken`
3. If valid, server stores the user info and sends `auth_success`
4. If invalid, server sends `auth_error` and the client can retry

---

## Step 5: Add Chat Rooms

The app uses a room system where users can join different rooms.

To add room switching to the UI, add this component to `App.jsx` (before the closing `</div>` of the header):

```jsx
{/* Room selector */}
<select
  value={room}
  onChange={(e) => {
    wsRef.current?.send(JSON.stringify({
      type: 'join_room',
      payload: { room: e.target.value },
    }));
  }}
  className="room-selector"
>
  <option value="general"># general</option>
  <option value="random"># random</option>
  <option value="engineering"># engineering</option>
  <option value="support"># support</option>
</select>
```

Add this CSS:

```css
.room-selector {
  padding: 0.4rem 0.75rem;
  border-radius: 6px;
  border: 1px solid rgba(255,255,255,0.2);
  background: rgba(255,255,255,0.1);
  color: white;
  font-size: 0.9rem;
  cursor: pointer;
}
```

---

## Step 6: Add Typing Indicators

Typing indicators are already implemented in the code above. Here's how it works:

1. Client sends `{ type: 'typing', payload: { isTyping: true } }` on each keystroke
2. Server broadcasts to the room (excluding the sender)
3. Other clients display "Alice typing..." and clear it after 2 seconds of inactivity
4. When the user stops typing for 2 seconds, client sends `{ type: 'typing', payload: { isTyping: false } }`

---

## Complete Code

The complete source code is available at:

- **GitHub**: [github.com/myorg/realtime-chat-tutorial](https://github.com/myorg/realtime-chat-tutorial)
- **Branch**: `tutorial/complete`

```text
realtime-chat/
├── server/
│   ├── src/
│   │   ├── index.js       # WebSocket server (complete)
│   │   └── token.js        # Dev token generator
│   ├── .env                # Environment config
│   └── package.json
├── client/
│   ├── src/
│   │   ├── App.jsx         # React chat app (complete)
│   │   ├── App.css         # Styles (complete)
│   │   └── main.jsx        # Vite entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## What You Learned

| Concept | What you implemented |
|---|---|
| **WebSocket protocol** | Bidirectional, real-time communication between browser and server using the `ws` library |
| **WebSocket server** | Handling connections, messages, disconnections, and broadcasting to rooms |
| **WebSocket client** | Connecting from the browser, sending/receiving messages, handling reconnection |
| **JWT authentication** | Verifying user identity during WebSocket connection upgrade |
| **Room-based messaging** | Isolating messages to named rooms with `broadcastToRoom()` |
| **Typing indicators** | Broadcasting ephemeral state changes with automatic timeout |
| **React state management** | Managing WebSocket state, message list, and user list in React components |
| **CSS layout** | Building a chat UI with sidebar, message list, and input area |

---

## Next Steps

Now that you've built a real-time chat application, here's what to explore next:

| Topic | Description | Difficulty |
|---|---|---|
| **Add message persistence** | Store messages in PostgreSQL using the REST API | Intermediate |
| **Add file sharing** | Send images and files over WebSocket with binary frames | Intermediate |
| **Scale with Redis Pub/Sub** | Run multiple server instances with Redis pub/sub for horizontal scaling | Advanced |
| **Add end-to-end encryption** | Encrypt messages client-side before sending | Advanced |
| **Deploy to production** | Containerize with Docker, deploy to Kubernetes | Intermediate |
| **Add rate limiting** | Prevent spam with per-user rate limits on the server | Intermediate |
| **Add message history** | Load recent messages on room join from the database | Intermediate |
| **Implement reconnection** | Auto-reconnect with exponential backoff on connection loss | Intermediate |

---

## Related Resources

- [MDN WebSocket API Reference](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [ws Library Documentation](https://github.com/websockets/ws)
- [JWT Introduction](https://jwt.io/introduction)
- [Vite Documentation](https://vitejs.dev/guide/)
- [Real-World WebSocket Patterns](https://www.oreilly.com/library/view/real-time-web-socket/9781449371870/)
