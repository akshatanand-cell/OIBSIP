import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip

# ─────────────────────────────────────────────
#  Akshat_Anand_Task1 — Advanced Password Generator
#  Oasis Infobyte Python Internship
# ─────────────────────────────────────────────

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator — Akshat Anand | Oasis Infobyte")
        self.root.geometry("520x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        self.password_history = []
        self._build_ui()

    # ── UI Construction ──────────────────────
    def _build_ui(self):
        # Title
        tk.Label(self.root, text="🔐 Password Generator",
                 font=("Segoe UI", 18, "bold"),
                 bg="#1e1e2e", fg="#cba6f7").pack(pady=(20, 4))
        tk.Label(self.root, text="Akshat Anand  •  Oasis Infobyte Internship",
                 font=("Segoe UI", 9), bg="#1e1e2e", fg="#6c7086").pack()

        # ── Length slider ──
        frame_len = tk.Frame(self.root, bg="#1e1e2e")
        frame_len.pack(pady=16, padx=30, fill="x")
        tk.Label(frame_len, text="Password Length", font=("Segoe UI", 11),
                 bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w")

        self.length_var = tk.IntVar(value=16)
        self.length_label = tk.Label(frame_len, text="16",
                                     font=("Segoe UI", 11, "bold"),
                                     bg="#1e1e2e", fg="#89b4fa")
        self.length_label.pack(anchor="e")

        self.slider = ttk.Scale(frame_len, from_=6, to=64,
                                variable=self.length_var, orient="horizontal",
                                command=self._update_length_label)
        self.slider.pack(fill="x")

        # ── Character options ──
        frame_opts = tk.LabelFrame(self.root, text=" Character Types ",
                                   font=("Segoe UI", 10),
                                   bg="#1e1e2e", fg="#a6e3a1",
                                   bd=1, relief="groove")
        frame_opts.pack(padx=30, pady=8, fill="x")

        self.use_upper  = self._checkbox(frame_opts, "Uppercase  (A–Z)", True)
        self.use_lower  = self._checkbox(frame_opts, "Lowercase  (a–z)", True)
        self.use_digits = self._checkbox(frame_opts, "Digits       (0–9)", True)
        self.use_symbols= self._checkbox(frame_opts, "Symbols   (!@#$...)", True)

        # ── Exclude characters ──
        frame_excl = tk.Frame(self.root, bg="#1e1e2e")
        frame_excl.pack(padx=30, pady=6, fill="x")
        tk.Label(frame_excl, text="Exclude characters (optional):",
                 font=("Segoe UI", 10), bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w")
        self.exclude_var = tk.StringVar()
        tk.Entry(frame_excl, textvariable=self.exclude_var,
                 font=("Segoe UI", 11), bg="#313244", fg="#cdd6f4",
                 insertbackground="white", relief="flat",
                 width=30).pack(anchor="w", pady=4)

        # ── Quantity ──
        frame_qty = tk.Frame(self.root, bg="#1e1e2e")
        frame_qty.pack(padx=30, pady=4, fill="x")
        tk.Label(frame_qty, text="How many passwords?",
                 font=("Segoe UI", 10), bg="#1e1e2e", fg="#cdd6f4").pack(side="left")
        self.qty_var = tk.IntVar(value=1)
        ttk.Spinbox(frame_qty, from_=1, to=10, width=5,
                    textvariable=self.qty_var,
                    font=("Segoe UI", 10)).pack(side="left", padx=10)

        # ── Generate button ──
        tk.Button(self.root, text="⚡  Generate Password",
                  font=("Segoe UI", 12, "bold"),
                  bg="#cba6f7", fg="#1e1e2e", activebackground="#b4befe",
                  relief="flat", cursor="hand2", pady=8,
                  command=self.generate).pack(padx=30, pady=12, fill="x")

        # ── Result box ──
        frame_res = tk.Frame(self.root, bg="#1e1e2e")
        frame_res.pack(padx=30, fill="x")
        tk.Label(frame_res, text="Generated Password(s):",
                 font=("Segoe UI", 10), bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w")

        self.result_box = tk.Text(frame_res, height=4,
                                  font=("Consolas", 12),
                                  bg="#313244", fg="#a6e3a1",
                                  relief="flat", wrap="word",
                                  state="disabled")
        self.result_box.pack(fill="x", pady=4)

        # ── Strength bar ──
        self.strength_label = tk.Label(self.root, text="Strength: —",
                                       font=("Segoe UI", 10),
                                       bg="#1e1e2e", fg="#f9e2af")
        self.strength_label.pack()

        self.strength_bar = ttk.Progressbar(self.root, length=460,
                                            maximum=100, mode="determinate")
        self.strength_bar.pack(padx=30, pady=4)

        # ── Copy button ──
        tk.Button(self.root, text="📋  Copy to Clipboard",
                  font=("Segoe UI", 11),
                  bg="#89b4fa", fg="#1e1e2e", activebackground="#74c7ec",
                  relief="flat", cursor="hand2",
                  command=self.copy_to_clipboard).pack(padx=30, pady=(6,0), fill="x")

        # ── History button ──
        tk.Button(self.root, text="🕓  View History",
                  font=("Segoe UI", 10),
                  bg="#313244", fg="#cdd6f4", activebackground="#45475a",
                  relief="flat", cursor="hand2",
                  command=self.show_history).pack(padx=30, pady=6, fill="x")

    # ── Helpers ──────────────────────────────
    def _checkbox(self, parent, label, default):
        var = tk.BooleanVar(value=default)
        tk.Checkbutton(parent, text=label, variable=var,
                       font=("Segoe UI", 10),
                       bg="#1e1e2e", fg="#cdd6f4",
                       selectcolor="#313244",
                       activebackground="#1e1e2e").pack(anchor="w", padx=10, pady=2)
        return var

    def _update_length_label(self, _=None):
        self.length_label.config(text=str(self.length_var.get()))

    def _build_charset(self):
        charset = ""
        if self.use_upper.get():   charset += string.ascii_uppercase
        if self.use_lower.get():   charset += string.ascii_lowercase
        if self.use_digits.get():  charset += string.digits
        if self.use_symbols.get(): charset += string.punctuation
        excluded = self.exclude_var.get()
        charset = "".join(c for c in charset if c not in excluded)
        return charset

    def _make_password(self, charset, length):
        # Guarantee at least one char from each selected type
        guaranteed = []
        pool_list = []
        if self.use_upper.get():
            valid = [c for c in string.ascii_uppercase if c not in self.exclude_var.get()]
            if valid: guaranteed.append(random.choice(valid))
            pool_list += valid
        if self.use_lower.get():
            valid = [c for c in string.ascii_lowercase if c not in self.exclude_var.get()]
            if valid: guaranteed.append(random.choice(valid))
            pool_list += valid
        if self.use_digits.get():
            valid = [c for c in string.digits if c not in self.exclude_var.get()]
            if valid: guaranteed.append(random.choice(valid))
            pool_list += valid
        if self.use_symbols.get():
            valid = [c for c in string.punctuation if c not in self.exclude_var.get()]
            if valid: guaranteed.append(random.choice(valid))
            pool_list += valid

        remaining = length - len(guaranteed)
        password = guaranteed + [random.choice(charset) for _ in range(remaining)]
        random.shuffle(password)
        return "".join(password)

    def _score_strength(self, password):
        score = 0
        if len(password) >= 8:  score += 20
        if len(password) >= 12: score += 20
        if len(password) >= 16: score += 10
        if any(c.isupper() for c in password): score += 15
        if any(c.islower() for c in password): score += 15
        if any(c.isdigit() for c in password): score += 10
        if any(c in string.punctuation for c in password): score += 10
        return min(score, 100)

    # ── Actions ──────────────────────────────
    def generate(self):
        charset = self._build_charset()
        if not charset:
            messagebox.showerror("Error", "Please select at least one character type.")
            return

        length = self.length_var.get()
        qty    = self.qty_var.get()
        passwords = [self._make_password(charset, length) for _ in range(qty)]

        self.result_box.config(state="normal")
        self.result_box.delete("1.0", tk.END)
        self.result_box.insert(tk.END, "\n".join(passwords))
        self.result_box.config(state="disabled")

        self.password_history.extend(passwords)

        # Strength of first password
        score = self._score_strength(passwords[0])
        self.strength_bar["value"] = score
        if score < 40:
            label, color = "Weak 🔴", "#f38ba8"
        elif score < 70:
            label, color = "Moderate 🟡", "#f9e2af"
        else:
            label, color = "Strong 🟢", "#a6e3a1"
        self.strength_label.config(text=f"Strength: {label} ({score}/100)", fg=color)

    def copy_to_clipboard(self):
        content = self.result_box.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Nothing to copy", "Generate a password first.")
            return
        pyperclip.copy(content.split("\n")[0])  # copy first password
        messagebox.showinfo("Copied!", "Password copied to clipboard ✅")

    def show_history(self):
        if not self.password_history:
            messagebox.showinfo("History", "No passwords generated yet.")
            return
        win = tk.Toplevel(self.root)
        win.title("Password History")
        win.geometry("400x300")
        win.configure(bg="#1e1e2e")
        tk.Label(win, text="Password History",
                 font=("Segoe UI", 13, "bold"),
                 bg="#1e1e2e", fg="#cba6f7").pack(pady=10)
        box = tk.Text(win, font=("Consolas", 11),
                      bg="#313244", fg="#a6e3a1", relief="flat")
        box.pack(fill="both", expand=True, padx=10, pady=10)
        for i, p in enumerate(self.password_history, 1):
            box.insert(tk.END, f"{i:02d}. {p}\n")
        box.config(state="disabled")


# ── Entry Point ───────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
