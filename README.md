# 🐍 Kriptografi Klasik: Transposition Cipher (Implementasi Python)

[![License: MIT](https://img.shields.io/badge/License-MIT-34d399.svg)](../LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-38bdf8.svg?logo=python&logoColor=white)](https://www.python.org/)
[![UDINUS](https://img.shields.io/badge/UDINUS-Teknik%20Informatika-a855f7.svg)](https://dinus.ac.id/)
[![Tests](https://img.shields.io/badge/Tests-100%25%20Passed-34d399.svg)](main.py)

> **Mata Kuliah** : Kriptografi  
> **Program Studi**: S1 Teknik Informatika, Fakultas Ilmu Komputer  
> **Institusi**    : Universitas Dian Nuswantoro (UDINUS)  
> **Kelompok**     : 2 (Transposition Cipher)

---

## 📌 Ringkasan Proyek

Repositori folder `python/` ini berisi implementasi perangkat lunak berbasis **Python 3** untuk menyimulasikan seluruh materi perkuliahan yang tercantum pada **Slide Presentasi Transposition Cipher (38 Slide)**.

Kode ditulis dengan standar rekayasa perangkat lunak profesional:
- **Batch Documentation Headers**: Setiap modul dan fungsi dilengkapi blok dokumentasi terstruktur yang mencakup Kategori, Dasar Teori Kriptografis, Formula Matematika, Penjelasan Parameter, Tipe Kembalian (Type Hints), Kompleksitas Waktu & Ruang ($O$), serta Contoh Penggunaan.
- **Tanpa Dependency Eksternal**: 100% menggunakan Python Standard Library (`math`, `sys`, `typing`, `time`), sehingga dapat langsung dijalankan di semua sistem operasi (Windows, Linux, macOS) tanpa perlu instalasi `pip`.
- **Dukungan Terminal UTF-8 & ANSI Safe**: Menampilkan visualisasi matriks 2D, rel zig-zag, rute spiral, dan stensil 4 rotasi dengan warna highlight beresolusi tinggi.

---

## 🗂️ Struktur Direktori

```text
d:/tugas sekolah/kuliah Udinus/kripto/python/
├── __init__.py           # Inisialisasi paket dan eksposur modul publik
├── utils.py              # Sanitasi teks alfabetis, padding dummy 'X', pewarnaan ANSI, & visualizer matriks ASCII
├── scytale.py            # Varian 1: Scytale Cipher (Tongkat Silinder Sparta Kuno)
├── rail_fence.py         # Varian 2: Rail Fence Cipher (Zig-Zag Gelombang Periodik)
├── route_cipher.py       # Varian 3: Route Cipher (Lintasan Spiral Clockwise 4x4)
├── myszkowski.py         # Varian 4: Myszkowski Cipher (Aturan Huruf Kunci Kembar / Tie-Breaker)
├── turning_grille.py     # Varian 5: Turning Grille (Fleissner Grille 4x4 Stensil Berputar)
├── advanced.py           # Teori Lanjutan: Matriks Permutasi Ortogonal (P*P^T=I), IoC, AES ShiftRows, DES P-Box
├── main.py               # Master CLI Interaktif & Suite Pengujian Otomatis
└── README.md             # Buku Panduan Penggunaan & Dokumentasi
```

---

## 🚀 Cara Menjalankan Program

### 1. Menjalankan Master CLI Interaktif

Buka terminal pada direktori `python/`, lalu jalankan:

```bash
python main.py
```

Menu utama akan menampilkan 3 opsi utama:
1. **Jalankan Uji Otomatis Kasus Slide Presentasi** (memverifikasi kebenaran matematika 5 cipher terhadap slide).
2. **Simulasi Praktikum Interaktif** (memasukkan plaintext dan kunci kustom dengan visualisasi step-by-step).
3. **Laboratorium Kriptanalisis (Index of Coincidence) & Kaitan Modern (AES/DES)**.

---

### 2. Menjalankan Modul Tertentu Secara Mandiri

Setiap berkas `.py` dapat dieksekusi secara independen untuk melihat demo step-by-step khusus varian tersebut:

```bash
# Uji Varian 1: Scytale
python scytale.py

# Uji Varian 2: Rail Fence
python rail_fence.py

# Uji Varian 3: Route Cipher
python route_cipher.py

# Uji Varian 4: Myszkowski
python myszkowski.py

# Uji Varian 5: Turning Grille
python turning_grille.py

# Uji Analisis Lanjutan & Kriptanalisis
python advanced.py
```

---

## 📊 Matriks Kasus Uji Slide Presentasi (100% Verifikasi)

| No | Varian Cipher | Plaintext Masukan | Kunci | Output Ciphertext Terverifikasi | Status Dekripsi |
| :---: | :--- | :--- | :--- | :--- | :---: |
| 1 | **Scytale** | `HELPMEARRIVE` | $d = 3$ baris | `HMREEILAVPRE` | **PULIH SEMPURNA** |
| 2 | **Rail Fence** | `KRIPTOGRAFI` | $n = 3$ rel | `KTARPORFIGI` | **PULIH SEMPURNA** |
| 3 | **Route Cipher** | `SERANGANDIBAWAH` | Grid $4 \times 4$ (Spiral) | `SERANAXHAWDNGABI` | **PULIH SEMPURNA** |
| 4 | **Myszkowski** | `WE ARE DISCOVERED` | `TOMATO` | `ROXACDEDSEEXWEIVRX` | **PULIH SEMPURNA** |
| 5 | **Turning Grille**| `SENDTROOPSASAPXX` | Stensil 4 Rotasi | `SENTADROPXPOXSAS` | **PULIH SEMPURNA** |
| 6 | **Aljabar Linier**| `['A', 'B', 'C', 'D']` | Matriks $P_\sigma$ | $P_\sigma \cdot P_\sigma^T = I$ (Ortogonal) | **PULIH SEMPURNA** |
| 7 | **Kriptanalisis**| Sampel Teks Panjang | Uji IoC Friedman | $IC \approx 0.067 - 0.068$ (Transposisi Terbukti) | **TERDIAGNOSA AKURAT** |

---

## 📖 Dokumentasi Batch & Arsitektur Fungsi

Setiap fungsi inti dirancang dengan spesifikasi formal:

```python
"""
=============================================================================
FUNGSI / METODE : scytale_encrypt
KATEGORI        : Algoritma Enkripsi Transposisi Silinder
DASAR TEORI     : Merepresentasikan lilitan pita pada tongkat kayu sebagai grid
                  2D berukuran d baris x m kolom. Pesan asli ditulis mendatar
                  per baris, lalu diekstraksi tegak lurus per kolom ke bawah.
-----------------------------------------------------------------------------
FORMULA MATEMATIKA:
    d = kunci (jumlah baris / keliling silinder)
    m = ceil(|P| / d) (jumlah kolom / panjang tongkat)
    
    Pemetaan Indeks Enkripsi:
    Grid[r][c] = P[(r * m) + c]
    Ciphertext: C[(c * d) + r] = Grid[r][c]

PARAMETER:
    - plaintext (str): Pesan asli yang akan dienkripsi.
    - key_d (int): Kunci diameter tongkat (d >= 2).
    - verbose (bool): Tampilkan visualisasi matriks terminal.

OUTPUT / RETURN:
    - Tuple[str, List[List[str]]]: (ciphertext, matriks_konseptual)

KOMPLEKSITAS:
    - Waktu : O(|P|)
    - Ruang : O(d * m)
=============================================================================
"""
```

---

## 👥 Informasi Kelompok

* **Kelompok**: 2
* **Materi**: Transposition Cipher (5 Varian Inti & Analisis Modern)
* **Dokumen Presentasi HTML**: `../presentasi_kriptografi.html`
* **Dokumen Presentasi PDF**: `../presentasi_kriptografi.pdf` (38 Halaman Pas 16:9)

---

## 📜 Lisensi

Seluruh kode dalam paket ini dirilis di bawah lisensi open-source **[MIT License](../LICENSE)**.

```text
MIT License
Copyright (c) 2026 Kelompok 2 — Teknik Informatika Universitas Dian Nuswantoro (UDINUS)
```
Bebas digunakan untuk keperluan praktikum, tugas perkuliahan, maupun riset lanjutan kriptografi.
