import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ─────────────────────────────────────────────
#  Akshat_Anand_Task2 — Advanced BMI Calculator
#  Oasis Infobyte Python Internship
# ─────────────────────────────────────────────

DATA_FILE = "bmi_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

class BMIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator — Akshat Anand | Oasis Infobyte")
        self.root.geometry("580x680")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")
        self.data = load_data()
        self._build_ui()

    def _label(self, parent, text, size=11, bold=False, color="#cdd6f4"):
        font = ("Segoe UI", size, "bold") if bold else ("Segoe UI", size)
        return tk.Label(parent, text=text, font=font, bg="#1e1e2e", fg=color)

    def _build_ui(self):
        # Title
        self._label(self.root, "⚖️  BMI Calculator", 18, True, "#cba6f7").pack(pady=(20,4))
        self._label(self.root, "Akshat Anand  •  Oasis Infobyte Internship", 9, color="#6c7086").pack()

        # ── User name ──
        frame_user = tk.Frame(self.root, bg="#1e1e2e")
        frame_user.pack(padx=30, pady=12, fill="x")
        self._label(frame_user, "Your Name:").pack(anchor="w")
        self.name_var = tk.StringVar()
        tk.Entry(frame_user, textvariable=self.name_var,
                 font=("Segoe UI", 11), bg="#313244", fg="#cdd6f4",
                 insertbackground="white", relief="flat").pack(fill="x", pady=4)

        # ── Unit toggle ──
        frame_unit = tk.Frame(self.root, bg="#1e1e2e")
        frame_unit.pack(padx=30, fill="x")
        self._label(frame_unit, "Unit System:").pack(side="left")
        self.unit_var = tk.StringVar(value="Metric")
        ttk.Radiobutton(frame_unit, text="Metric (kg / m)",
                        variable=self.unit_var, value="Metric",
                        command=self._update_labels).pack(side="left", padx=10)
        ttk.Radiobutton(frame_unit, text="Imperial (lbs / ft)",
                        variable=self.unit_var, value="Imperial",
                        command=self._update_labels).pack(side="left")

        # ── Weight ──
        frame_w = tk.Frame(self.root, bg="#1e1e2e")
        frame_w.pack(padx=30, pady=10, fill="x")
        self.weight_label = self._label(frame_w, "Weight (kg):")
        self.weight_label.pack(anchor="w")
        self.weight_var = tk.StringVar()
        tk.Entry(frame_w, textvariable=self.weight_var,
                 font=("Segoe UI", 11), bg="#313244", fg="#cdd6f4",
                 insertbackground="white", relief="flat").pack(fill="x", pady=4)

        # ── Height ──
        frame_h = tk.Frame(self.root, bg="#1e1e2e")
        frame_h.pack(padx=30, fill="x")
        self.height_label = self._label(frame_h, "Height (m):")
        self.height_label.pack(anchor="w")
        self.height_var = tk.StringVar()
        tk.Entry(frame_h, textvariable=self.height_var,
                 font=("Segoe UI", 11), bg="#313244", fg="#cdd6f4",
                 insertbackground="white", relief="flat").pack(fill="x", pady=4)

        # ── Calculate button ──
        tk.Button(self.root, text="📊  Calculate BMI",
                  font=("Segoe UI", 12, "bold"),
                  bg="#cba6f7", fg="#1e1e2e", activebackground="#b4befe",
                  relief="flat", cursor="hand2", pady=8,
                  command=self.calculate).pack(padx=30, pady=14, fill="x")

        # ── Result ──
        self.result_frame = tk.Frame(self.root, bg="#313244", bd=0)
        self.result_frame.pack(padx=30, fill="x")

        self.bmi_label = self._label(self.result_frame, "BMI: —", 22, True, "#89b4fa")
        self.bmi_label.pack(pady=(10,2))

        self.cat_label = self._label(self.result_frame, "Category: —", 13, color="#f9e2af")
        self.cat_label.pack(pady=(0,4))

        self.advice_label = self._label(self.result_frame, "", 10, color="#a6e3a1")
        self.advice_label.pack(pady=(0,10))

        # ── Buttons row ──
        frame_btns = tk.Frame(self.root, bg="#1e1e2e")
        frame_btns.pack(padx=30, pady=10, fill="x")

        tk.Button(frame_btns, text="📈  View History Graph",
                  font=("Segoe UI", 10),
                  bg="#89b4fa", fg="#1e1e2e", relief="flat", cursor="hand2",
                  command=self.show_graph).pack(side="left", expand=True, fill="x", padx=(0,5))

        tk.Button(frame_btns, text="🗂️  View All Users",
                  font=("Segoe UI", 10),
                  bg="#a6e3a1", fg="#1e1e2e", relief="flat", cursor="hand2",
                  command=self.show_users).pack(side="left", expand=True, fill="x", padx=(5,0))

        # ── BMI Scale reference ──
        ref = tk.LabelFrame(self.root, text=" BMI Scale Reference ",
                            font=("Segoe UI", 9),
                            bg="#1e1e2e", fg="#6c7086", bd=1, relief="groove")
        ref.pack(padx=30, pady=8, fill="x")
        scale_data = [
            ("< 18.5",    "Underweight", "#89b4fa"),
            ("18.5–24.9", "Normal",      "#a6e3a1"),
            ("25.0–29.9", "Overweight",  "#f9e2af"),
            ("≥ 30.0",    "Obese",       "#f38ba8"),
        ]
        for i, (rng, cat, col) in enumerate(scale_data):
            tk.Label(ref, text=f"{rng}  →  {cat}",
                     font=("Segoe UI", 9), bg="#1e1e2e", fg=col).grid(
                     row=0, column=i, padx=14, pady=6)

    def _update_labels(self):
        if self.unit_var.get() == "Metric":
            self.weight_label.config(text="Weight (kg):")
            self.height_label.config(text="Height (m):")
        else:
            self.weight_label.config(text="Weight (lbs):")
            self.height_label.config(text="Height (ft):")

    def calculate(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter your name.")
            return
        try:
            w = float(self.weight_var.get())
            h = float(self.height_var.get())
            if w <= 0 or h <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter valid positive numbers.")
            return

        # Convert imperial to metric
        if self.unit_var.get() == "Imperial":
            w = w * 0.453592
            h = h * 0.3048

        bmi = w / (h ** 2)

        if bmi < 18.5:
            cat, col, advice = "Underweight 🔵", "#89b4fa", "Consider a nutrient-rich diet and consult a doctor."
        elif bmi < 25:
            cat, col, advice = "Normal Weight 🟢", "#a6e3a1", "Great! Maintain your healthy lifestyle."
        elif bmi < 30:
            cat, col, advice = "Overweight 🟡", "#f9e2af", "Consider regular exercise and a balanced diet."
        else:
            cat, col, advice = "Obese 🔴", "#f38ba8", "Please consult a healthcare professional."

        self.bmi_label.config(text=f"BMI: {bmi:.2f}", fg=col)
        self.cat_label.config(text=f"Category: {cat}", fg=col)
        self.advice_label.config(text=advice)

        # Save to history
        if name not in self.data:
            self.data[name] = []
        self.data[name].append({
            "bmi": round(bmi, 2),
            "category": cat,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        save_data(self.data)

    def show_graph(self):
        name = self.name_var.get().strip()
        if not name or name not in self.data or len(self.data[name]) == 0:
            messagebox.showinfo("No Data", "No history found for this user.")
            return

        records = self.data[name]
        dates = [r["date"] for r in records]
        bmis  = [r["bmi"]  for r in records]

        win = tk.Toplevel(self.root)
        win.title(f"BMI History — {name}")
        win.configure(bg="#1e1e2e")

        fig, ax = plt.subplots(figsize=(6, 3.5), facecolor="#1e1e2e")
        ax.set_facecolor("#313244")
        ax.plot(range(len(bmis)), bmis, marker="o", color="#cba6f7", linewidth=2)
        ax.axhline(18.5, color="#89b4fa", linestyle="--", linewidth=1, label="Underweight")
        ax.axhline(25.0, color="#a6e3a1", linestyle="--", linewidth=1, label="Normal")
        ax.axhline(30.0, color="#f38ba8", linestyle="--", linewidth=1, label="Obese")
        ax.set_xticks(range(len(dates)))
        ax.set_xticklabels([d[5:16] for d in dates], rotation=30, ha="right",
                           fontsize=7, color="#cdd6f4")
        ax.set_ylabel("BMI", color="#cdd6f4")
        ax.set_title(f"BMI Trend — {name}", color="#cba6f7")
        ax.tick_params(colors="#cdd6f4")
        ax.legend(fontsize=8)
        for spine in ax.spines.values():
            spine.set_edgecolor("#45475a")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def show_users(self):
        if not self.data:
            messagebox.showinfo("No Data", "No user records found.")
            return
        win = tk.Toplevel(self.root)
        win.title("All Users")
        win.geometry("420x320")
        win.configure(bg="#1e1e2e")
        tk.Label(win, text="All User Records", font=("Segoe UI", 13, "bold"),
                 bg="#1e1e2e", fg="#cba6f7").pack(pady=10)
        box = tk.Text(win, font=("Consolas", 10), bg="#313244",
                      fg="#cdd6f4", relief="flat")
        box.pack(fill="both", expand=True, padx=10, pady=10)
        for user, records in self.data.items():
            box.insert(tk.END, f"👤 {user}\n")
            for r in records:
                box.insert(tk.END, f"   {r['date']}  →  BMI: {r['bmi']}  ({r['category']})\n")
            box.insert(tk.END, "\n")
        box.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = BMIApp(root)
    root.mainloop()
