# PasswordNexus
<!--
PasswordNexus — ICT Project README
Air University · Islamabad · 2025
Abdul Haseeb [2500710]
-->

<div align="center">

```
██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗     
██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗    
██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║    
██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║    
██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝    
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝     
                N  E  X  U  S
```

*Your all-in-one platform for generating, analyzing, and securing your digital life.*

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![University](https://img.shields.io/badge/Air_University-ICT_Project-00D4FF?style=flat-square)

</div>

---

## Overview

PasswordNexus is a full-stack web application built with **Python + Flask** as an ICT course project at Air University, Islamabad. It provides a complete password security toolkit with five integrated modules, persistent SQLite logging, and a clean browser-based interface.

```
┌─────────────────────────────────────────────────────────────────┐
│                    PasswordNexus Modules                        │
├──────────────────────┬──────────────────────────────────────────┤
│  🔐 Generator        │  Cryptographically secure passwords      │
│  🧪 Strength Analyzer│  zxcvbn scoring + crack time estimate    │
│  ⏱️  Brute Force Est │  Math-based crack time calculator        │
│  🔄 Hash Converter   │  MD5 · SHA1 · SHA256 · SHA512 + more    │
│  📦 Base Enc/Dec     │  Base64 · Base32 · Base16 · URL encode   │
└──────────────────────┴──────────────────────────────────────────┘
```

All tool usage is logged to a **SQLite database** (`nexus.db`) and exported to `log.txt` automatically.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3 · Flask · zxcvbn · hashlib · secrets |
| Frontend | HTML5 · CSS3 · Jinja2 templates |
| Database | SQLite3 (activity logging) |
| Security | `secrets` module (CSPRNG) · policy enforcement |

---

## Project Structure

```
PasswordNexus/
├── backend.py              ← Flask app · all routes · logic functions
├── nexus.db                ← SQLite database (auto-created)
├── log.txt                 ← Exported activity log
├── static/
│   ├── style.css           ← Main page styles
│   ├── generator.css       ← Tool page styles
│   └── Image.jpeg          ← Background image
├── templates/
│   ├── index.html          ← Landing page + tool overview
│   ├── base.html           ← Base encode/decode page
│   ├── generator.html      ← Password generator page
│   ├── analyzer.html       ← Strength analyzer page
│   ├── bruteforcetime.html ← Brute force estimator page
│   ├── hashconverter.html  ← Hash converter page
│   └── terms.html          ← Terms of use
└── README.md
```

---

## Module Details

### 🔐 Password Generator
Uses Python's `secrets` module (cryptographically secure RNG) to generate passwords with guaranteed character class coverage:
- Enforces at least 1 lowercase, 1 uppercase, 1 digit, 1 symbol
- Minimum length: 8 · Maximum: 100
- Character pool: `A-Z a-z 0-9 !@#$%&*()`
- Final password is shuffled with `random.shuffle()` to eliminate positional bias

### 🧪 Strength Analyzer
Two-stage analysis pipeline:
1. **Policy check** — regex validation for uppercase, lowercase, digit presence + minimum length
2. **zxcvbn scoring** — realistic strength estimation accounting for dictionary words, patterns, and common substitutions. Returns score (0–4), crack time, and improvement suggestions.

### ⏱️ Brute Force Estimator
Mathematical crack-time calculator:

```
combinations = charset_size ^ password_length
time = combinations / attempts_per_second
```

Charset options: lowercase only (26) · mixed case (52) · alphanumeric (62) · full ASCII printable (95)

### 🔄 Hash Converter
Wraps Python's `hashlib` to convert any text to: MD5 · SHA1 · SHA224 · SHA256 · SHA384 · SHA512 · and any other algo in `hashlib.algorithms_available`

### 📦 Base Encoder/Decoder
Supports: Base64 · Base32 · Base16 (hex) · URL encoding/decoding — bidirectional, with terms agreement gate.

---

## Setup & Run

```bash
# Clone the repo
git clone https://github.com/AceX98/PasswordNexus.git
cd PasswordNexus

# Install dependencies
pip install flask zxcvbn

# Run
python backend.py
# → http://127.0.0.1:5000
```

---

## Activity Logging

Every tool usage is recorded in `nexus.db`:

```sql
CREATE TABLE logs (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    type       TEXT NOT NULL,        -- e.g. "Generator", "Analyzer", "Hash"
    detail     TEXT NOT NULL,        -- e.g. "Generated pass length: 16"
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

On shutdown, logs are exported to `log.txt` automatically via `export_logs()`.

---

## Security Notes

- Passwords are generated using `secrets.choice()` — **not** `random.choice()`. The `secrets` module uses OS-level entropy (suitable for cryptographic use).
- No passwords are stored anywhere — only event metadata is logged.
- Hash conversion is one-way; the app never stores input text.

---

## Screenshots

> *Add screenshots here after deployment — `docs/screenshots/`*

---

<div align="center">

*Air University ·  
*Abdul Haseeb *

![Python](https://img.shields.io/badge/Built_with-Python_%2B_Flask-3776AB?style=flat-square&logo=python&logoColor=white)

</div>
