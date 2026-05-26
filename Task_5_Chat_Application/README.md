<div align="center">

# 💬 Chat Application
### *Real-Time Multi-User Chat Over Local Network*

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![Sockets](https://img.shields.io/badge/Sockets-Networking-green?style=for-the-badge)
![Threading](https://img.shields.io/badge/Threading-Concurrent-orange?style=for-the-badge)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-purple?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=for-the-badge)

<br/>

> *"Connect, chat, and communicate — all in real time!"*

<br/>

**Built by Akshat Anand** | 🏢 Oasis Infobyte Python Internship | 📅 June 2026

</div>

---

## 📸 Preview

```
💬  Chat Application
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
● Connected as Akshat        👥 Online: Akshat
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[04:04] 🟢 Nova joined the chat!

[04:04] Nova: hello everyone!

[04:04] You: hey Nova! 👋

[04:04] Nova: how's the internship going? 🔥

[04:05] You: amazing! just built this chat app 😎
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
😊 😂 ❤️ 👍 🔥 😎 🎉 😢 😮 🙏
[ Type a message...          ] [Send ➤]
```

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 🌐 **Server-Client** | Real socket-based networking architecture |
| 👥 **Multi-User** | Multiple users can chat simultaneously |
| ⚡ **Real-Time** | Instant message delivery with no delay |
| 🎨 **Color Coded** | Each user gets a unique username color |
| 😊 **Emoji Bar** | One-click emoji insertion into messages |
| 📜 **Live History** | All messages displayed with timestamps |
| 🟢 **Join/Leave** | System notifications when users connect |
| ⌨️ **Enter to Send** | Press Enter or click Send button |
| 🌙 **Dark Theme** | Sleek modern dark-themed UI |

---

## 🚀 Getting Started

### Prerequisites
```bash
python --version  # Python 3.x required
# No extra libraries needed — uses built-in Python modules!
```

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/akshatanand-cell/OIBSIP.git
cd OIBSIP/Task_5_Chat_Application
```

**2. Start the Server (Terminal 1)**
```bash
python server.py
```
You should see:
```
🚀 Server started on 127.0.0.1:55555
Waiting for connections...
```

**3. Start Client (Terminal 2)**
```bash
python client.py
```

**4. Start another Client (Terminal 3)**
```bash
python client.py
```

**5. Enter different usernames and start chatting! 💬**

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│              SERVER (server.py)          │
│         127.0.0.1 : 55555               │
│  • Accepts connections                   │
│  • Broadcasts messages to all clients    │
│  • Handles join/leave notifications      │
└──────────┬──────────────────┬───────────┘
           │                  │
    ┌──────▼──────┐    ┌──────▼──────┐
    │  CLIENT 1   │    │  CLIENT 2   │
    │  (Akshat)   │    │   (Nova)    │
    │  client.py  │    │  client.py  │
    └─────────────┘    └─────────────┘
```

---

## 🛠️ Tech Stack

```
├── Python 3.x    → Core language
├── socket        → TCP/IP networking
├── threading     → Handle multiple clients concurrently
└── tkinter       → GUI chat interface
```

---

## 📁 Project Structure

```
Task_5_Chat_Application/
├── 📄 server.py      → Chat server (run first)
├── 📄 client.py      → Chat client GUI
└── 📄 README.md      → Project documentation
```

---

## 🎯 Key Concepts Learned

- 🔌 **Socket Programming** — TCP/IP client-server communication
- 🧵 **Multithreading** — Handling multiple clients simultaneously
- 📡 **Broadcasting** — Sending messages to all connected clients
- 🖥️ **GUI Design** — Real-time updating Tkinter interface
- ⚠️ **Error Handling** — Managing disconnections gracefully
- 🔄 **Event-Driven** — Responding to network and UI events

---

## 👨‍💻 Author

<div align="center">

**Akshat Anand**

[![GitHub](https://img.shields.io/badge/GitHub-akshatanand--cell-black?style=for-the-badge&logo=github)](https://github.com/akshatanand-cell)

*Python Programming Intern @ Oasis Infobyte*
*Duration: June 2026 — July 2026*

</div>

---

<div align="center">

⭐ **If you found this helpful, please star the repo!** ⭐

*Made with ❤️ and Python*

</div>
