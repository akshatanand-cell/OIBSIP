import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime

# ─────────────────────────────────────────────
#  Akshat_Anand_Task3 — Advanced Weather App
#  Oasis Infobyte Python Internship
# ─────────────────────────────────────────────

API_KEY = "78bef98a160f19bdd8565bf02989709e"
BASE_URL = "https://api.openweathermap.org/data/2.5/"

WEATHER_ICONS = {
    "Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️",
    "Drizzle": "🌦️", "Thunderstorm": "⛈️", "Snow": "❄️",
    "Mist": "🌫️", "Fog": "🌫️", "Haze": "🌫️",
}

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App — Akshat Anand | Oasis Infobyte")
        self.root.geometry("560x720")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")
        self.unit_var = tk.StringVar(value="metric")
        self._build_ui()

    def _label(self, parent, text, size=11, bold=False, color="#cdd6f4", bg="#1e1e2e"):
        font = ("Segoe UI", size, "bold") if bold else ("Segoe UI", size)
        return tk.Label(parent, text=text, font=font, bg=bg, fg=color)

    def _build_ui(self):
        # Title
        self._label(self.root, "🌤️  Weather App", 18, True, "#cba6f7").pack(pady=(20,4))
        self._label(self.root, "Akshat Anand  •  Oasis Infobyte Internship", 9, color="#6c7086").pack()

        # ── Search bar ──
        frame_search = tk.Frame(self.root, bg="#1e1e2e")
        frame_search.pack(padx=30, pady=16, fill="x")

        self.city_var = tk.StringVar()
        entry = tk.Entry(frame_search, textvariable=self.city_var,
                         font=("Segoe UI", 12), bg="#313244", fg="#cdd6f4",
                         insertbackground="white", relief="flat")
        entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0,8))
        entry.insert(0, "Enter city name...")
        entry.bind("<FocusIn>", lambda e: entry.delete(0, tk.END) if entry.get() == "Enter city name..." else None)
        entry.bind("<Return>", lambda e: self.fetch_weather())

        tk.Button(frame_search, text="🔍 Search",
                  font=("Segoe UI", 11, "bold"),
                  bg="#cba6f7", fg="#1e1e2e", relief="flat",
                  cursor="hand2", padx=12, pady=6,
                  command=self.fetch_weather).pack(side="left")

        # ── Unit toggle ──
        frame_unit = tk.Frame(self.root, bg="#1e1e2e")
        frame_unit.pack()
        ttk.Radiobutton(frame_unit, text="°C (Metric)", variable=self.unit_var,
                        value="metric", command=self.fetch_weather).pack(side="left", padx=10)
        ttk.Radiobutton(frame_unit, text="°F (Imperial)", variable=self.unit_var,
                        value="imperial", command=self.fetch_weather).pack(side="left", padx=10)

        # ── Main weather card ──
        self.card = tk.Frame(self.root, bg="#313244", bd=0)
        self.card.pack(padx=30, pady=16, fill="x")

        self.icon_label  = self._label(self.card, "", 48, bg="#313244")
        self.icon_label.pack(pady=(16,0))

        self.temp_label  = self._label(self.card, "—", 36, True, "#89b4fa", "#313244")
        self.temp_label.pack()

        self.city_label  = self._label(self.card, "—", 16, True, "#cdd6f4", "#313244")
        self.city_label.pack()

        self.desc_label  = self._label(self.card, "—", 11, color="#a6adc8", bg="#313244")
        self.desc_label.pack(pady=(2,8))

        # ── Details row ──
        self.details_frame = tk.Frame(self.card, bg="#313244")
        self.details_frame.pack(fill="x", padx=20, pady=(0,16))

        self.detail_labels = {}
        details = [("💧 Humidity", "—"), ("💨 Wind", "—"),
                   ("👁️ Visibility", "—"), ("🌡️ Feels Like", "—")]
        for i, (key, val) in enumerate(details):
            f = tk.Frame(self.details_frame, bg="#45475a")
            f.grid(row=0, column=i, padx=4, pady=4, sticky="nsew")
            self.details_frame.columnconfigure(i, weight=1)
            self._label(f, key, 8, color="#a6adc8", bg="#45475a").pack(pady=(6,2))
            lbl = self._label(f, val, 10, True, "#cdd6f4", "#45475a")
            lbl.pack(pady=(0,6))
            self.detail_labels[key] = lbl

        # ── Sunrise / Sunset ──
        self.sun_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.sun_frame.pack(padx=30, fill="x")
        self.sunrise_label = self._label(self.sun_frame, "🌅 Sunrise: —", 11, color="#f9e2af")
        self.sunrise_label.pack(side="left", expand=True)
        self.sunset_label  = self._label(self.sun_frame, "🌇 Sunset: —", 11, color="#fab387")
        self.sunset_label.pack(side="left", expand=True)

        # ── 5-Day Forecast ──
        self._label(self.root, "5-Day Forecast", 12, True, "#cba6f7").pack(pady=(16,6))
        self.forecast_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.forecast_frame.pack(padx=30, fill="x")
        self.forecast_cards = []
        for i in range(5):
            f = tk.Frame(self.forecast_frame, bg="#313244")
            f.grid(row=0, column=i, padx=4, sticky="nsew")
            self.forecast_frame.columnconfigure(i, weight=1)
            day_lbl  = self._label(f, "—", 9,  color="#a6adc8", bg="#313244")
            day_lbl.pack(pady=(8,2))
            icon_lbl = self._label(f, "—", 18, bg="#313244")
            icon_lbl.pack()
            temp_lbl = self._label(f, "—", 10, True, "#89b4fa", "#313244")
            temp_lbl.pack(pady=(2,8))
            self.forecast_cards.append((day_lbl, icon_lbl, temp_lbl))

        # ── Status ──
        self.status_label = self._label(self.root, "", 9, color="#6c7086")
        self.status_label.pack(pady=10)

    # ── Fetch Weather ─────────────────────────
    def fetch_weather(self):
        city = self.city_var.get().strip()
        if not city or city == "Enter city name...":
            messagebox.showwarning("Input Error", "Please enter a city name.")
            return

        unit = self.unit_var.get()
        sym  = "°C" if unit == "metric" else "°F"

        try:
            # Current weather
            url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units={unit}"
            r = requests.get(url, timeout=10)
            if r.status_code == 404:
                messagebox.showerror("Not Found", f"City '{city}' not found.")
                return
            r.raise_for_status()
            d = r.json()

            main    = d["weather"][0]["main"]
            icon    = WEATHER_ICONS.get(main, "🌡️")
            temp    = d["main"]["temp"]
            feels   = d["main"]["feels_like"]
            humidity= d["main"]["humidity"]
            wind    = d["wind"]["speed"]
            vis     = d.get("visibility", 0) // 1000
            desc    = d["weather"][0]["description"].title()
            country = d["sys"]["country"]
            sunrise = datetime.fromtimestamp(d["sys"]["sunrise"]).strftime("%H:%M")
            sunset  = datetime.fromtimestamp(d["sys"]["sunset"]).strftime("%H:%M")

            self.icon_label.config(text=icon)
            self.temp_label.config(text=f"{temp:.1f}{sym}")
            self.city_label.config(text=f"{d['name']}, {country}")
            self.desc_label.config(text=desc)
            self.detail_labels["💧 Humidity"].config(text=f"{humidity}%")
            self.detail_labels["💨 Wind"].config(text=f"{wind} m/s")
            self.detail_labels["👁️ Visibility"].config(text=f"{vis} km")
            self.detail_labels["🌡️ Feels Like"].config(text=f"{feels:.1f}{sym}")
            self.sunrise_label.config(text=f"🌅 Sunrise: {sunrise}")
            self.sunset_label.config(text=f"🌇 Sunset: {sunset}")

            # 5-day forecast
            furl = f"{BASE_URL}forecast?q={city}&appid={API_KEY}&units={unit}&cnt=40"
            fr = requests.get(furl, timeout=10)
            fr.raise_for_status()
            fd = fr.json()

            # Pick one reading per day (noon)
            seen, forecasts = set(), []
            for item in fd["list"]:
                date = item["dt_txt"].split(" ")[0]
                if date not in seen:
                    seen.add(date)
                    forecasts.append(item)
                if len(forecasts) == 5:
                    break

            for i, item in enumerate(forecasts):
                day  = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%a")
                fmain= item["weather"][0]["main"]
                ftemp= item["main"]["temp"]
                self.forecast_cards[i][0].config(text=day)
                self.forecast_cards[i][1].config(text=WEATHER_ICONS.get(fmain, "🌡️"))
                self.forecast_cards[i][2].config(text=f"{ftemp:.1f}{sym}")

            self.status_label.config(
                text=f"Last updated: {datetime.now().strftime('%H:%M:%S')}", fg="#6c7086")

        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "No internet connection.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
