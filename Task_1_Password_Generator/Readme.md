<div align="center">

# 🔐 Password Generator
### *Generate Strong, Secure Passwords Instantly*

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-purple?style=for-the-badge)
![Pyperclip](https://img.shields.io/badge/Pyperclip-Clipboard-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=for-the-badge)

<br/>

> *"Never use a weak password again — let the generator do the work!"*

<br/>

**Built by Akshat Anand** | 🏢 Oasis Infobyte Python Internship | 📅 June 2026

</div>

---

## 📸 Preview

```
🔐  Password Generator
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Password Length          [ 16 ]
▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░

☑ Uppercase (A–Z)    ☑ Lowercase (a–z)
☑ Digits (0–9)       ☑ Symbols (!@#$...)

Exclude characters: [ 0O1l ]
How many passwords?  [ 3 ]

[ ⚡ Generate Password ]

Generated Password(s):
K#9mP@vL2xQr!nWd
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Strength: Strong 🟢 (90/100)
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░

[ 📋 Copy to Clipboard ]  [ 🕓 View History ]
```

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 🎚️ **Length Slider** | Adjust password length from 6 to 64 characters |
| 🔤 **Character Types** | Toggle Uppercase, Lowercase, Digits, Symbols |
| 🚫 **Exclude Chars** | Remove specific characters you don't want |
| 🔢 **Bulk Generate** | Generate up to 10 passwords at once |
| 💪 **Strength Meter** | Real-time password strength score out of 100 |
| 📋 **Clipboard Copy** | One-click copy to clipboard |
| 🕓 **History Viewer** | View all previously generated passwords |
| 🌙 **Dark Theme** | Beautiful dark-themed modern UI |

---

## 🚀 Getting Started

### Prerequisites
```bash
python --version  # Python 3.x required
```

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/akshatanand-cell/OIBSIP.git
cd OIBSIP/Task_1_Password_Generator
```

**2. Install dependencies**
```bash
pip install pyperclip
```

**3. Run the app**
```bash
python password_generator.py
```

---

## 🛡️ How Strength is Calculated

```
Length ≥ 8   chars   → +20 points
Length ≥ 12  chars   → +20 points
Length ≥ 16  chars   → +10 points
Has Uppercase        → +15 points
Has Lowercase        → +15 points
Has Digits           → +10 points
Has Symbols          → +10 points
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Score < 40   → Weak 🔴
Score < 70   → Moderate 🟡
Score ≥ 70   → Strong 🟢
```

---

## 🛠️ Tech Stack

```
├── Python 3.x    → Core language
├── Tkinter       → GUI framework
├── pyperclip     → Clipboard integration
├── random        → Password randomization
└── string        → Character set handling
```

---

## 📁 Project Structure

```
Task_1_Password_Generator/
├── 📄 password_generator.py    → Main application
└── 📄 README.md                → Project documentation
```

---

## 🎯 Key Concepts Learned

- 🔀 **Randomization** — Generating cryptographically random characters
- ✅ **Input Validation** — Ensuring valid user preferences
- 🔡 **Character Sets** — Managing multiple character type pools
- 📊 **Scoring Logic** — Implementing a strength algorithm
- 🖥️ **GUI Design** — Building interactive Tkinter interfaces
- 📋 **Clipboard API** — Integrating system clipboard

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
