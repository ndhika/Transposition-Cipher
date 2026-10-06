<div align="center">

# 🛡️ Transposition Cipher Suite

**A pure-Python toolkit for classical transposition ciphers and spatial matrix permutations.**

[![License: MIT](https://img.shields.io/badge/License-MIT-10b981.svg?style=flat-square)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-3b82f6.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Tests: 100% Passed](https://img.shields.io/badge/Tests-100%25%20Passed-10b981.svg?style=flat-square)](main.py)
[![Dependencies: None](https://img.shields.io/badge/Dependencies-Standard%20Library-8b5cf6.svg?style=flat-square)](.)

[Overview](#-overview) •
[Interactive CLI](#-interactive-cli-preview) •
[5 Core Ciphers](#-5-core-cipher-variants) •
[Parameter Flexibility](#-parameter-flexibility) •
[Quickstart](#-quickstart) •
[Python API](#-python-api-usage) •
[License](#-license)

</div>

---

## 📌 Overview

**Transposition Cipher Suite** is a modular, zero-dependency Python implementation of classical spatial transposition ciphers. Unlike substitution ciphers which replace characters, transposition ciphers rearrange the spatial positions of characters while strictly preserving their symbolic values and natural language frequency distributions.

### Key Highlights
* **Zero External Dependencies**: Built entirely using the Python Standard Library (`math`, `sys`, `typing`, `time`). Runs seamlessly on Windows, Linux, and macOS without `pip install`.
* **Dynamic Parameter Flexibility**: All 5 cipher variants support arbitrary plaintext lengths and customizable parameters (diameter, rail count, grid dimensions $R \times C$, keywords, and even $N \times N$ stencil grids).
* **Terminal Matrix Visualizer**: Features clean ASCII-rendered 2D matrices, zig-zag waves, clockwise spiral paths, and 4-quadrant rotating stencil grids with ANSI color highlighting.

---

## 🖥️ Interactive CLI Preview

Run the interactive terminal suite to test any cipher with custom inputs or execute the automated verification suite:

```text
$ python main.py

=============================================================================
             KRIPTOGRAFI KLASIK: TRANSPOSITION CIPHER SUITE
=============================================================================
                 SIMULASI & DEMO INTERAKTIF · KELOMPOK 2
=============================================================================

MENU UTAMA DEMO KRIPTOGRAFI:
  1. Jalankan Uji Otomatis Kasus Sandi (Automated Test Suite)
  2. Simulasi Praktikum Interaktif (Scytale, Rail Fence, Route, Myszkowski, Grille)
  0. Keluar dari Program
```

---

## 🎯 5 Core Cipher Variants

| Cipher | Geometric Model | Secret Key | Characteristic Mechanism |
| :--- | :--- | :--- | :--- |
| **Scytale** | $d \times m$ Cylinder Grid | Rod Diameter $d$ (Rows) | Ancient Spartan parchment wrapped around a wooden rod. Written horizontally, extracted vertically. |
| **Rail Fence** | Triangular Zig-Zag Wave | Rail Depth $n$ | Bounces periodically across $n$ rails with period $T = 2(n - 1)$. Characters extracted rail by rail. |
| **Route Cipher** | $R \times C$ Dynamic Grid | Clockwise Spiral Route | Text is populated row-by-row and extracted along an inward spiral path starting at $(0,0)$. |
| **Myszkowski** | Columnar Tie-Breaker Grid | Keyword String | Permits repeated keyword letters. Unique ranks read vertically ($\downarrow$); duplicate ranks read horizontally ($\rightarrow$). |
| **Turning Grille** | $N \times N$ Fleissner Stencil | 4 Collision-Free Rotations | Stencil is rotated 4 times by 90° ($0^\circ, 90^\circ, 180^\circ, 270^\circ$). All $N^2$ cells filled without collision. |

---

## ⚙️ Parameter Flexibility

Each cipher adapts dynamically to user inputs:

* **Scytale**: Any rod diameter $d \ge 2$, columns calculated dynamically as $\lceil L / d \rceil$.
* **Rail Fence**: Any rail depth $n \ge 2$, wave pattern adjusts automatically.
* **Route Cipher**: Arbitrary row $R$ and column $C$ dimensions (e.g. $3 \times 5, 4 \times 4, 6 \times 6$).
* **Myszkowski**: Any keyword with arbitrary length and repeated characters.
* **Turning Grille**: Any even grid size $N \times N$ ($N = 4, 6, 8, \dots$) with automatic collision-free stencil generation.

---

## 🚀 Quickstart

### Prerequisites
* Python 3.8 or newer.

### Installation & Execution

```bash
# Clone repository
git clone https://github.com/ndhika/Transposition-Cipher.git

# Enter project directory
cd Transposition-Cipher

# Launch interactive CLI
python main.py
```

### Running Individual Module Demos

Each cipher module is standalone and can be executed independently:

```bash
python scytale.py         # Spartan Scytale demo
python rail_fence.py      # Rail Fence zig-zag demo
python route_cipher.py    # Route spiral demo
python myszkowski.py      # Myszkowski duplicate-key demo
python turning_grille.py  # Fleissner 4-rotation stencil demo
```

---

## 💻 Python API Usage

All ciphers can be imported and integrated directly into Python applications:

```python
from scytale import scytale_encrypt, scytale_decrypt
from rail_fence import rail_fence_encrypt, rail_fence_decrypt
from route_cipher import route_cipher_encrypt, route_cipher_decrypt
from myszkowski import myszkowski_encrypt, myszkowski_decrypt
from turning_grille import turning_grille_encrypt, turning_grille_decrypt

# 1. Scytale Cipher
ct, _ = scytale_encrypt("HELPMEARRIVE", key_d=3)
pt, _ = scytale_decrypt(ct, key_d=3)
# ct -> "HMREEILAVPRE", pt -> "HELPMEARRIVE"

# 2. Rail Fence Cipher
ct_rf, _ = rail_fence_encrypt("KRIPTOGRAFI", num_rails=3)
pt_rf, _ = rail_fence_decrypt(ct_rf, num_rails=3)
# ct_rf -> "KTARPORFIGI", pt_rf -> "KRIPTOGRAFI"

# 3. Route Cipher (Spiral 4x4)
ct_rt, _ = route_cipher_encrypt("SERANGANDIBAWAH", rows=4, cols=4)
pt_rt, _ = route_cipher_decrypt(ct_rt, rows=4, cols=4)

# 4. Myszkowski Cipher
ct_my, _ = myszkowski_encrypt("WE ARE DISCOVERED", keyword="TOMATO")
pt_my, _ = myszkowski_decrypt(ct_my, keyword="TOMATO")

# 5. Turning Grille Cipher
ct_tg, _ = turning_grille_encrypt("SENDTROOPSASAPXX", n=4)
pt_tg, _ = turning_grille_decrypt(ct_tg, n=4)
```

---

## 🧪 Verification Matrix

Automated unit tests validate 100% mathematical correctness across all 5 ciphers:

```text
================================================================================
KASUS UJI SANDI                  | TARGET CIPHER        | HASIL OUTPUT         | STATUS
--------------------------------------------------------------------------------
Varian 1: Scytale (d=3)          | HMREEILAVPRE         | HMREEILAVPRE         | [ PASS OK ]
Varian 2: Rail Fence (n=3)       | KTARPORFIGI          | KTARPORFIGI          | [ PASS OK ]
Varian 3: Route Spiral (4x4)     | SERANAXHAWDNGABI     | SERANAXHAWDNGABI     | [ PASS OK ]
Varian 4: Myszkowski (TOMATO)    | ROXACDEDSEEXWEIVRX   | ROXACDEDSEEXWEIVRX   | [ PASS OK ]
Varian 5: Turning Grille (4x4)   | SENTADROPXPOXSAS     | SENTADROPXPOXSAS     | [ PASS OK ]
================================================================================
>>> SELURUH PENGUJIAN 5 VARIAN 100% SUKSES DAN COCOK PERSIS! <<<
```

---

## 🗂️ Project Structure

```text
.
├── LICENSE             # MIT License
├── README.md           # Project documentation
├── PANDUAN_PRESENTASI.md # Presentation script & Q&A guide
├── .gitignore          # Git ignore patterns
├── __init__.py         # Package entrypoint
├── utils.py            # Sanitization, padding, and ANSI table visualizer
├── scytale.py          # Scytale Cipher implementation
├── rail_fence.py       # Rail Fence Cipher implementation
├── route_cipher.py     # Route (Spiral) Cipher implementation
├── myszkowski.py       # Myszkowski Cipher implementation
├── turning_grille.py   # Turning Grille Cipher implementation
└── main.py             # Interactive CLI & automated test runner
```

---

## 📜 License

This project is licensed under the **[MIT License](LICENSE)**.

```text
MIT License
Copyright (c) 2026 Kelompok 2
```
