import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import random
import os

# ─────────────────────────────────────────────
#  Akshat_Anand_Task4 — Advanced Voice Assistant
#  Oasis Infobyte Python Internship
# ─────────────────────────────────────────────

ASSISTANT_NAME = "Nova"

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why was the computer cold? Because it left its Windows open!",
    "What do you call a fish without eyes? A fsh!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads.",
]

GREETINGS = ["hello", "hi", "hey", "good morning", "good evening", "good afternoon"]

class VoiceAssistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 175)
        self.engine.setProperty("volume", 1.0)
        voices = self.engine.getProperty("voices")
        # Try to set a female voice
        for v in voices:
            if "female" in v.name.lower() or "zira" in v.name.lower() or "hazel" in v.name.lower():
                self.engine.setProperty("voice", v.id)
                break
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 1.0

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
        return self.recognizer.recognize_google(audio)

    def process_command(self, cmd):
        cmd = cmd.lower().strip()

        # Greeting
        if any(g in cmd for g in GREETINGS):
            hour = datetime.datetime.now().hour
            if hour < 12:   greet = "Good morning"
            elif hour < 17: greet = "Good afternoon"
            else:           greet = "Good evening"
            return f"{greet}! I'm {ASSISTANT_NAME}, your voice assistant. How can I help you?"

        # Time
        elif "time" in cmd:
            t = datetime.datetime.now().strftime("%I:%M %p")
            return f"The current time is {t}."

        # Date
        elif "date" in cmd:
            d = datetime.datetime.now().strftime("%A, %B %d, %Y")
            return f"Today is {d}."

        # Day
        elif "day" in cmd:
            d = datetime.datetime.now().strftime("%A")
            return f"Today is {d}."

        # Joke
        elif "joke" in cmd:
            return random.choice(JOKES)

        # Search web
        elif "search" in cmd or "google" in cmd:
            query = cmd.replace("search", "").replace("google", "").strip()
            if query:
                webbrowser.open(f"https://www.google.com/search?q={query}")
                return f"Searching Google for: {query}"
            return "What would you like me to search for?"

        # YouTube
        elif "youtube" in cmd:
            query = cmd.replace("youtube", "").replace("play", "").strip()
            if query:
                webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
                return f"Opening YouTube for: {query}"
            else:
                webbrowser.open("https://www.youtube.com")
                return "Opening YouTube!"

        # Open websites
        elif "open" in cmd:
            if "github" in cmd:
                webbrowser.open("https://github.com/akshatanand-cell")
                return "Opening your GitHub profile!"
            elif "linkedin" in cmd:
                webbrowser.open("https://linkedin.com")
                return "Opening LinkedIn!"
            elif "google" in cmd:
                webbrowser.open("https://google.com")
                return "Opening Google!"
            else:
                return "I can open GitHub, LinkedIn, or Google. Which one?"

        # Calculator
        elif "calculate" in cmd or "calculator" in cmd:
            os.system("calc")
            return "Opening Calculator!"

        # Name
        elif "your name" in cmd or "who are you" in cmd:
            return f"I'm {ASSISTANT_NAME}, your personal voice assistant built by Akshat Anand!"

        # Creator
        elif "who made you" in cmd or "who created you" in cmd:
            return "I was created by Akshat Anand as part of the Oasis Infobyte Python Internship!"

        # Help
        elif "help" in cmd or "what can you do" in cmd:
            return ("I can: tell time & date, tell jokes, search Google, "
                    "open YouTube, open websites, open calculator, and chat with you!")

        # Thanks
        elif "thank" in cmd:
            return "You're welcome! Always happy to help! 😊"

        # Goodbye
        elif any(w in cmd for w in ["bye", "goodbye", "exit", "quit"]):
            return f"Goodbye! Have a wonderful day! 👋"

        # Default
        else:
            webbrowser.open(f"https://www.google.com/search?q={cmd}")
            return f"I'm not sure about that, but I searched Google for: {cmd}"


class VoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant — Akshat Anand | Oasis Infobyte")
        self.root.geometry("540x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")
        self.assistant = VoiceAssistant()
        self.listening = False
        self._build_ui()
        self._add_message(ASSISTANT_NAME,
            f"Hello! I'm {ASSISTANT_NAME}, your voice assistant. "
            "Click 🎙️ to speak or type a command below!", "assistant")

    def _build_ui(self):
        # Title
        tk.Label(self.root, text="🎙️  Voice Assistant",
                 font=("Segoe UI", 18, "bold"),
                 bg="#1e1e2e", fg="#cba6f7").pack(pady=(20,4))
        tk.Label(self.root, text="Akshat Anand  •  Oasis Infobyte Internship",
                 font=("Segoe UI", 9), bg="#1e1e2e", fg="#6c7086").pack()

        # ── Status indicator ──
        self.status_var = tk.StringVar(value="● Ready")
        self.status_label = tk.Label(self.root, textvariable=self.status_var,
                                     font=("Segoe UI", 10, "bold"),
                                     bg="#1e1e2e", fg="#a6e3a1")
        self.status_label.pack(pady=6)

        # ── Chat area ──
        self.chat_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.chat_frame.pack(padx=20, pady=8, fill="both", expand=True)

        self.chat_box = scrolledtext.ScrolledText(
            self.chat_frame, font=("Segoe UI", 11),
            bg="#181825", fg="#cdd6f4", relief="flat",
            wrap="word", state="disabled", height=20)
        self.chat_box.pack(fill="both", expand=True)

        self.chat_box.tag_config("user",      foreground="#89b4fa", font=("Segoe UI", 11, "bold"))
        self.chat_box.tag_config("assistant", foreground="#cba6f7", font=("Segoe UI", 11, "bold"))
        self.chat_box.tag_config("msg",       foreground="#cdd6f4", font=("Segoe UI", 11))
        self.chat_box.tag_config("time",      foreground="#6c7086", font=("Segoe UI", 8))

        # ── Mic button ──
        self.mic_btn = tk.Button(self.root, text="🎙️  Hold to Speak",
                                  font=("Segoe UI", 13, "bold"),
                                  bg="#cba6f7", fg="#1e1e2e",
                                  activebackground="#b4befe",
                                  relief="flat", cursor="hand2", pady=10,
                                  command=self.toggle_listen)
        self.mic_btn.pack(padx=30, pady=10, fill="x")

        # ── Type command ──
        frame_type = tk.Frame(self.root, bg="#1e1e2e")
        frame_type.pack(padx=30, pady=(0,10), fill="x")

        self.type_var = tk.StringVar()
        entry = tk.Entry(frame_type, textvariable=self.type_var,
                         font=("Segoe UI", 11), bg="#313244", fg="#cdd6f4",
                         insertbackground="white", relief="flat")
        entry.pack(side="left", fill="x", expand=True, ipady=7, padx=(0,8))
        entry.bind("<Return>", lambda e: self.send_typed())

        tk.Button(frame_type, text="Send",
                  font=("Segoe UI", 11, "bold"),
                  bg="#89b4fa", fg="#1e1e2e", relief="flat",
                  cursor="hand2", padx=12,
                  command=self.send_typed).pack(side="left")

        # ── Quick commands ──
        frame_quick = tk.Frame(self.root, bg="#1e1e2e")
        frame_quick.pack(padx=30, pady=(0,16), fill="x")
        cmds = ["What time is it?", "Tell me a joke", "What's today's date?", "Help"]
        for i, cmd in enumerate(cmds):
            tk.Button(frame_quick, text=cmd,
                      font=("Segoe UI", 8),
                      bg="#313244", fg="#cdd6f4",
                      activebackground="#45475a",
                      relief="flat", cursor="hand2",
                      command=lambda c=cmd: self._handle_command(c)).grid(
                      row=0, column=i, padx=3, sticky="ew")
            frame_quick.columnconfigure(i, weight=1)

    def _add_message(self, sender, message, tag):
        self.chat_box.config(state="normal")
        time_str = datetime.datetime.now().strftime("%H:%M")
        self.chat_box.insert(tk.END, f"\n{sender}  ", tag)
        self.chat_box.insert(tk.END, f"[{time_str}]\n", "time")
        self.chat_box.insert(tk.END, f"{message}\n", "msg")
        self.chat_box.config(state="disabled")
        self.chat_box.see(tk.END)

    def _handle_command(self, cmd):
        self._add_message("You", cmd, "user")
        response = self.assistant.process_command(cmd)
        self._add_message(ASSISTANT_NAME, response, "assistant")
        threading.Thread(target=self.assistant.speak, args=(response,), daemon=True).start()

    def send_typed(self):
        cmd = self.type_var.get().strip()
        if not cmd:
            return
        self.type_var.set("")
        self._handle_command(cmd)

    def toggle_listen(self):
        if self.listening:
            return
        threading.Thread(target=self._listen_thread, daemon=True).start()

    def _listen_thread(self):
        self.listening = True
        self.mic_btn.config(text="🔴  Listening...", bg="#f38ba8")
        self.status_var.set("● Listening...")
        self.status_label.config(fg="#f38ba8")
        try:
            cmd = self.assistant.listen()
            self.root.after(0, self._handle_command, cmd)
        except sr.WaitTimeoutError:
            self.root.after(0, self._add_message, ASSISTANT_NAME,
                            "I didn't hear anything. Please try again.", "assistant")
        except sr.UnknownValueError:
            self.root.after(0, self._add_message, ASSISTANT_NAME,
                            "Sorry, I couldn't understand. Please speak clearly.", "assistant")
        except Exception as e:
            self.root.after(0, self._add_message, ASSISTANT_NAME,
                            f"Error: {str(e)}", "assistant")
        finally:
            self.listening = False
            self.mic_btn.config(text="🎙️  Hold to Speak", bg="#cba6f7")
            self.status_var.set("● Ready")
            self.status_label.config(fg="#a6e3a1")


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()
