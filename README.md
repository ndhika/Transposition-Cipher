<div align="center">

# 🛡️ Transposition Cipher Suite

**A pure-Python toolkit for classical transposition ciphers, spatial matrix permutation, and modern cryptanalysis.**

[![License: MIT](https://img.shields.io/badge/License-MIT-10b981.svg?style=flat-square)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-3b82f6.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Tests: 100% Passed](https://img.shields.io/badge/Tests-100%25%20Passed-10b981.svg?style=flat-square)](main.py)
[![Dependencies: None](https://img.shields.io/badge/Dependencies-Standard%20Library-8b5cf6.svg?style=flat-square)](.)

[Overview](#-overview) •
[Interactive CLI](#-interactive-cli-preview) •
[Cipher Variants](#-5-core-cipher-variants) •
[Cryptanalysis](#-cryptanalysis--modern-diffusion) •
[Quickstart](#-quickstart) •
[Python API](#-python-api-usage) •
[License](#-license)

</div>

---

## 📌 Overview

**Transposition Cipher Suite** is a modular, zero-dependency Python implementation of classical spatial transposition ciphers. Unlike substitution ciphers which replace characters, transposition ciphers rearrange the spatial positions of characters while strictly preserving their symbolic values and natural language frequency distributions.

### Key Highlights
* **Zero External Dependencies**: Built entirely using the Python Standard Library (`math`, `sys`, `typing`, `time`). Runs seamlessly on Windows, Linux, and macOS.
* **Terminal Matrix Visualizer**: Features clean ASCII-rendered 2D matrices, zig-zag waves, clockwise spiral paths, and 4-quadrant rotating stencil grids.
* **Mathematical & Cryptanalytic Rigor**: Includes full implementations of Friedman's Index of Coincidence (IoC), orthogonal permutation matrices ($P_\sigma \cdot P_\sigma^T = I$), and Shannon diffusion bridges to modern standards (AES `ShiftRows` and DES `P-Box`).

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

MENU UTAMA:
  1. Jalankan Uji Otomatis Kasus Sandi (Automated Test Suite)
  2. Simulasi Praktikum Interaktif (Scytale, Rail Fence, Route, Myszkowski, Grille)
  3. Laboratorium Kriptanalisis (Index of Coincidence) & Kaitan Modern
  0. Keluar dari Program
```

---

## 🎯 5 Core Cipher Variants

| Cipher | Geometric Model | Secret Key | Characteristic Mechanism |
| :--- | :--- | :--- | :--- |
| **Scytale** | $d \times m$ Cylinder Grid | Rod Diameter $d$ (Rows) | Ancient Spartan parchment wrapped around a wooden rod. Written horizontally, extracted vertically. |
| **Rail Fence** | Triangular Zig-Zag Wave | Rail Depth $n$ | Bounces periodically across $n$ rails with period $T = 2(n - 1)$. Characters extracted rail by rail. |
| **Route Cipher** | $4 \times 4$ Coordinate Grid | Clockwise Spiral Route | Text is populated row-by-row and extracted along an inward spiral path starting at $(0,0)$. |
| **Myszkowski** | Columnar Tie-Breaker Grid | Keyword String | Permits repeated keyword letters. Unique ranks read vertically ($\downarrow$); duplicate ranks read horizontally ($\rightarrow$). |
| **Turning Grille** | $4 \times 4$ Fleissner Stencil | 4 Collision-Free Holes | Stencil is rotated 4 times by 90° ($0^\circ, 90^\circ, 180^\circ, 270^\circ$). All 16 cells filled without collision. |

---

## 🔬 Cryptanalysis & Modern Diffusion

### 1. Index of Coincidence (IoC)
William F. Friedman's quantitative test measures the probability that two randomly selected letters from a ciphertext are identical:

$$IC = \frac{\sum_{i=A}^Z f_i (f_i - 1)}{N(N - 1)}$$

* **Natural Language (ID/EN)**: $IC \approx 0.065 - 0.068$
* **Transposition Cipher**: $IC \approx 0.065 - 0.068$ *(Letter frequencies remain unaltered!)*
* **Polyalphabetic Substitution (e.g. Vigenère)**: $IC \approx 0.038 - 0.042$ *(Frequencies flattened)*

### 2. Orthogonal Permutation Matrix
Every spatial transposition of $N$ characters corresponds to an $N \times N$ binary orthogonal permutation matrix $P_\sigma$. Because $P_\sigma$ is orthogonal:

$$P_\sigma^{-1} = P_\sigma^T \implies \vec{x} = P_\sigma^T \cdot \vec{y}$$

Decryption is performed simply by transposing the matrix, eliminating the need for matrix inversion algorithms.

### 3. Shannon Diffusion in Modern Ciphers
* **AES `ShiftRows` (FIPS 197)**: Cyclically rotates rows of a $4 \times 4$ state array by 0, 1, 2, and 3 bytes.
* **DES `P-Box` (FIPS 46-3)**: 32-bit spatial bit permutation dispersing S-box outputs into subsequent Feistel rounds.

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

Each cipher module is fully standalone and can be executed independently:

```bash
python scytale.py         # Spartan Scytale demo
python rail_fence.py      # Rail Fence zig-zag demo
python route_cipher.py    # Route spiral 4x4 demo
python myszkowski.py      # Myszkowski duplicate-key demo
python turning_grille.py  # Fleissner 4-rotation stencil demo
python advanced.py        # Permutation matrix & IoC cryptanalysis demo
```

---

## 💻 Python API Usage

All ciphers can be imported and integrated directly into your own Python applications:

```python
from scytale import scytale_encrypt, scytale_decrypt
from rail_fence import rail_fence_encrypt, rail_fence_decrypt
from advanced import calculate_index_of_coincidence, diagnose_ciphertext_type

# 1. Scytale Cipher
ct, _ = scytale_encrypt("HELPMEARRIVE", key_d=3)
pt, _ = scytale_decrypt(ct, key_d=3)
# ct -> "HMREEILAVPRE", pt -> "HELPMEARRIVE"

# 2. Rail Fence Cipher
ct_rf, _ = rail_fence_encrypt("KRIPTOGRAFI", num_rails=3)
pt_rf, _ = rail_fence_decrypt(ct_rf, num_rails=3)
# ct_rf -> "KTARPORFIGI", pt_rf -> "KRIPTOGRAFI"

# 3. Cryptanalysis Diagnosis
ic_score = calculate_index_of_coincidence(ct)
print(f"IC Score: {ic_score:.4f}")  # ~0.068 (Diagnosed as Transposition)
```

---

## 🧪 Verification Matrix

Automated unit tests validate 100% mathematical correctness across all ciphers:

```text
================================================================================
KASUS UJI SLIDE                  | TARGET CIPHER        | HASIL OUTPUT         | STATUS
--------------------------------------------------------------------------------
Varian 1: Scytale (d=3)          | HMREEILAVPRE         | HMREEILAVPRE         | [ PASS OK ]
Varian 2: Rail Fence (n=3)       | KTARPORFIGI          | KTARPORFIGI          | [ PASS OK ]
Varian 3: Route Spiral (4x4)     | SERANAXHAWDNGABI     | SERANAXHAWDNGABI     | [ PASS OK ]
Varian 4: Myszkowski (TOMATO)    | ROXACDEDSEEXWEIVRX   | ROXACDEDSEEXWEIVRX   | [ PASS OK ]
Varian 5: Turning Grille (4x4)   | SENTADROPXPOXSAS     | SENTADROPXPOXSAS     | [ PASS OK ]
Aljabar: Ortogonal P*P^T=I       | ['A', 'B', 'C', 'D'] | ['A', 'B', 'C', 'D'] | [ PASS OK ]
Analisis: IoC (~0.068) & AES     | Shift OK             | Shift OK             | [ PASS OK ]
================================================================================
>>> SELURUH PENGUJIAN 100% SUKSES DENGAN HASIL MATEMATIS PERSISI! <<<
```

---

## 🗂️ Project Structure

```text
.
├── LICENSE             # MIT License
├── README.md           # Project documentation
├── .gitignore          # Git ignore patterns
├── __init__.py         # Package entrypoint
├── utils.py            # Sanitization, padding, and ANSI table visualizer
├── scytale.py          # Scytale Cipher implementation
├── rail_fence.py       # Rail Fence Cipher implementation
├── route_cipher.py     # Route (Spiral) Cipher implementation
├── myszkowski.py       # Myszkowski Cipher implementation
├── turning_grille.py   # Turning Grille Cipher implementation
├── advanced.py         # Linear algebra & cryptanalysis engine
└── main.py             # Interactive CLI & automated test runner
```

---

## 📜 License

This project is licensed under the **[MIT License](LICENSE)**.

```text
MIT License
Copyright (c) 2026 Kelompok 2
```

Feel free to use, modify, and distribute this codebase for academic, research, or personal projects.
