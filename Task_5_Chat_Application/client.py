import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import socket
import threading
import datetime

# ─────────────────────────────────────────────
#  Akshat_Anand_Task5 — Chat Application Client
#  Oasis Infobyte Python Internship
# ─────────────────────────────────────────────

HOST = "127.0.0.1"
PORT = 55555

EMOJIS = ["😊","😂","❤️","👍","🔥","😎","🎉","😢","😮","🙏"]

USER_COLORS = [
    "#89b4fa", "#a6e3a1", "#f9e2af", "#fab387",
    "#cba6f7", "#f38ba8", "#89dceb", "#b4befe"
]

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat App — Akshat Anand | Oasis Infobyte")
        self.root.geometry("560x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        self.socket = None
        self.username = None
        self.running = False
        self.user_colors = {}
        self.color_index = 0

        self._build_ui()
        self._ask_username()

    def _build_ui(self):
        # Title
        tk.Label(self.root, text="💬  Chat Application",
                 font=("Segoe UI", 18, "bold"),
                 bg="#1e1e2e", fg="#cba6f7").pack(pady=(20,4))
        tk.Label(self.root, text="Akshat Anand  •  Oasis Infobyte Internship",
                 font=("Segoe UI", 9), bg="#1e1e2e", fg="#6c7086").pack()

        # Status
        self.status_var = tk.StringVar(value="● Disconnected")
        self.status_label = tk.Label(self.root, textvariable=self.status_var,
                                     font=("Segoe UI", 10, "bold"),
                                     bg="#1e1e2e", fg="#f38ba8")
        self.status_label.pack(pady=4)

        # Online users
        frame_top = tk.Frame(self.root, bg="#313244")
        frame_top.pack(padx=20, fill="x")
        tk.Label(frame_top, text="👥 Online: ",
                 font=("Segoe UI", 9), bg="#313244", fg="#6c7086").pack(side="left", padx=8, pady=4)
        self.online_var = tk.StringVar(value="—")
        tk.Label(frame_top, textvariable=self.online_var,
                 font=("Segoe UI", 9, "bold"), bg="#313244", fg="#a6e3a1").pack(side="left")

        # Chat box
        self.chat_box = scrolledtext.ScrolledText(
            self.root, font=("Segoe UI", 11),
            bg="#181825", fg="#cdd6f4",
            relief="flat", wrap="word",
            state="disabled", height=22)
        self.chat_box.pack(padx=20, pady=10, fill="both", expand=True)

        # Tags
        self.chat_box.tag_config("system", foreground="#6c7086", font=("Segoe UI", 9, "italic"))
        self.chat_box.tag_config("time",   foreground="#6c7086", font=("Segoe UI", 8))
        self.chat_box.tag_config("self",   foreground="#a6e3a1", font=("Segoe UI", 11, "bold"))
        for i, color in enumerate(USER_COLORS):
            self.chat_box.tag_config(f"user{i}", foreground=color, font=("Segoe UI", 11, "bold"))

        # Emoji bar
        emoji_frame = tk.Frame(self.root, bg="#1e1e2e")
        emoji_frame.pack(padx=20, fill="x")
        for emoji in EMOJIS:
            tk.Button(emoji_frame, text=emoji,
                      font=("Segoe UI", 13),
                      bg="#1e1e2e", relief="flat",
                      cursor="hand2", bd=0,
                      command=lambda e=emoji: self._insert_emoji(e)).pack(side="left")

        # Input area
        frame_input = tk.Frame(self.root, bg="#1e1e2e")
        frame_input.pack(padx=20, pady=8, fill="x")

        self.msg_var = tk.StringVar()
        self.entry = tk.Entry(frame_input, textvariable=self.msg_var,
                              font=("Segoe UI", 12), bg="#313244", fg="#cdd6f4",
                              insertbackground="white", relief="flat")
        self.entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0,8))
        self.entry.bind("<Return>", lambda e: self.send_message())

        tk.Button(frame_input, text="Send ➤",
                  font=("Segoe UI", 11, "bold"),
                  bg="#cba6f7", fg="#1e1e2e",
                  activebackground="#b4befe",
                  relief="flat", cursor="hand2",
                  padx=12, command=self.send_message).pack(side="left")

    def _ask_username(self):
        name = simpledialog.askstring("Username",
                                      "Enter your username:",
                                      parent=self.root)
        if not name or not name.strip():
            self.root.destroy()
            return
        self.username = name.strip()
        self.root.title(f"Chat — {self.username} | Oasis Infobyte")
        self._connect()

    def _get_user_color(self, username):
        if username not in self.user_colors:
            self.user_colors[username] = f"user{self.color_index % len(USER_COLORS)}"
            self.color_index += 1
        return self.user_colors[username]

    def _connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((HOST, PORT))
            self.running = True
            self.status_var.set(f"● Connected as {self.username}")
            self.status_label.config(fg="#a6e3a1")
            self.online_var.set(self.username)

            thread = threading.Thread(target=self._receive, daemon=True)
            thread.start()
        except ConnectionRefusedError:
            messagebox.showerror("Error",
                "Could not connect to server!\nMake sure server.py is running.")
            self.root.destroy()

    def _receive(self):
        while self.running:
            try:
                message = self.socket.recv(1024).decode("utf-8")
                if message == "USERNAME":
                    self.socket.send(self.username.encode("utf-8"))
                else:
                    self._display_message(message)
            except:
                if self.running:
                    self._display_message("⚠️  Disconnected from server.")
                break

    def _display_message(self, message):
        self.chat_box.config(state="normal")

        # System messages (join/leave)
        if "joined the chat" in message or "left the chat" in message or "Connected!" in message:
            self.chat_box.insert(tk.END, f"{message}\n", "system")
        else:
            # Parse: [HH:MM] username: text
            try:
                parts = message.split("] ", 1)
                time_part = parts[0] + "]  "
                rest = parts[1] if len(parts) > 1 else message
                name_end = rest.index(": ")
                sender = rest[:name_end]
                text = rest[name_end+2:]

                self.chat_box.insert(tk.END, time_part, "time")
                if sender == self.username:
                    self.chat_box.insert(tk.END, f"You: ", "self")
                else:
                    color_tag = self._get_user_color(sender)
                    self.chat_box.insert(tk.END, f"{sender}: ", color_tag)
                self.chat_box.insert(tk.END, f"{text}\n")
            except:
                self.chat_box.insert(tk.END, f"{message}\n")

        self.chat_box.config(state="disabled")
        self.chat_box.see(tk.END)

    def _insert_emoji(self, emoji):
        current = self.msg_var.get()
        self.msg_var.set(current + emoji)
        self.entry.focus()
        self.entry.icursor(tk.END)

    def send_message(self):
        msg = self.msg_var.get().strip()
        if not msg or not self.running:
            return
        try:
            self.socket.send(msg.encode("utf-8"))
            self.msg_var.set("")
        except:
            messagebox.showerror("Error", "Failed to send message.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
