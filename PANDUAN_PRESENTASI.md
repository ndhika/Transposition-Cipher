# 🎙️ PANDUAN & NASKAH PRESENTASI KODE PROGRAM
## Proyek Kriptografi Klasik: Transposition Cipher Suite (Kelompok 2)

> **Catatan Pemakaian**: Panduan ini dibuat khusus agar kamu bisa presentasi dengan **santai, jelas, dan percaya diri** tanpa pusing dengan rumus-rumus rumit yang berlebihan (*too much*). Cukup ikuti petunjuk tindakan di terminal (**[AKSI]**) dan kalimat yang diucapkan (**[BICARA]**).

---

## 📋 DAFTAR ISI
1. [Alur & Durasi Presentasi](#1-alur--durasi-presentasi)
2. [Kalimat Pembuka (Opening)](#2-kalimat-pembuka-opening)
3. [Arsitektur Singkat Repositori](#3-arsitektur-singkat-repositori)
4. [Penjelasan Modul Pondasi: `utils.py`](#4-penjelasan-modul-pondasi-utilspy)
5. [Penjelasan 5 Varian Sandi Transposisi (Inti Presentasi)](#5-penjelasan-5-varian-sandi-transposisi-inti-presentasi)
   - [1. Scytale Cipher (`scytale.py`)](#1-scytale-cipher-scytalepy)
   - [2. Rail Fence Cipher (`rail_fence.py`)](#2-rail-fence-cipher-rail_fencepy)
   - [3. Route Cipher (`route_cipher.py`)](#3-route-cipher-route_cipherpy)
   - [4. Myszkowski Cipher (`myszkowski.py`)](#4-myszkowski-cipher-myszkowskipy)
   - [5. Turning Grille / Fleissner (`turning_grille.py`)](#5-turning-grille--fleissner-turning_grillepy)
6. [Penjelasan Antarmuka: `main.py`](#6-penjelasan-antarmuka-mainpy)
7. [Panduan Live Demo di Terminal](#7-panduan-live-demo-di-terminal)
8. [Antisipasi Pertanyaan Dosen (Q&A Santai)](#8-antisipasi-pertanyaan-dosen-qa-santai)
9. [Kalimat Penutup (Closing)](#9-kalimat-penutup-closing)

---

## 1. Alur & Durasi Presentasi
* **Target Waktu**: 7 – 10 Menit (Pas, padat, tidak bertele-tele).
* **Rundown**:
  * *Menit 01*: Pembukaan & Konsep Dasar Transposisi.
  * *Menit 02*: Penjelasan Utilitas (`utils.py`).
  * *Menit 03–06*: Bedah 5 Varian Sandi (Pola Geometri & Alur Enkripsi-Dekripsi).
  * *Menit 07–09*: Live Demo Program di Terminal (`python main.py`).
  * *Menit 10*: Penutup & Tanya Jawab.

---

## 2. Kalimat Pembuka (Opening)

**[AKSI]**: Tampilkan terminal atau kode program di layar proyektor.

**[BICARA]**:
> *"Selamat pagi/siang kepada Bapak/Ibu dosen pengampu mata kuliah Kriptografi dan teman-teman sekalian.*
> 
> *Kami dari **Kelompok 2** hari ini akan mempresentasikan dan mendemonstrasikan program Python yang telah kami buat untuk materi **Transposition Cipher** (Sandi Transposisi).*
> 
> *Konsep inti yang membedakan cipher transposisi dengan cipher substitusi adalah: **huruf aslinya sama sekali tidak diganti atau diubah**. Yang kita acak murni adalah **posisi atau urutan spasialnya**.*
> 
> *Pada proyek ini, kami mengimplementasikan **5 varian inti sandi transposisi** secara modular menggunakan Python murni tanpa library luar, lengkap dengan visualisasi matriks langsung di terminal."*

---

## 3. Arsitektur Singkat Repositori

**[AKSI]**: Tunjukkan daftar file di folder proyek.

**[BICARA]**:
> *"Program kami bagi menjadi beberapa file terpisah agar kodenya bersih dan mudah dipahami:*
> * `utils.py`: Berisi fungsi pembersihan teks, padding, dan penggambaran tabel ASCII.
> * `scytale.py` s.d. `turning_grille.py`: Mengimplementasikan 5 varian sandi secara independen.
> * `main.py`: Menu interaktif terminal untuk menjalankan demo dan pengujian otomatis."*

---

## 4. Penjelasan Modul Pondasi: `utils.py`

**[AKSI]**: Buka file `utils.py`.

**[BICARA]**:
> *"Sebelum pesan dienkripsi, kita memerlukan fungsi bantuan di `utils.py`:*
> 
> 1. **`clean_text(text)`**: Mengubah teks masukan menjadi huruf kapital A–Z dan membuang spasi atau tanda baca. Ini standar kriptografi klasik agar spasi kata tidak membocorkan pola pesan.
> 2. **`pad_text(text, block_size, pad_char='X')`**: Karena cipher transposisi bekerja dalam bentuk grid matriks, jika jumlah huruf tidak pas membagi ukuran kolom/grid, kita tambahkan huruf dummy `'X'` di belakangnya.
> 3. **`render_matrix(...)`**: Fungsi visualizer untuk mencetak tabel matriks 2D ke terminal dengan garis ASCII dan warna penanda, sehingga alur pengacakan huruf bisa dilihat mata dengan jelas."*

---

## 5. Penjelasan 5 Varian Sandi Transposisi (Inti Presentasi)

---

### 1. Scytale Cipher (`scytale.py`)
**[AKSI]**: Buka `scytale.py`.

**[BICARA]**:
> *"Varian pertama adalah **Scytale**, sandi silinder kayu dari masa Sparta Kuno.*
> * **Konsep**: Pesan ditulis melilit silinder kayu berdiameter $d$ (jumlah baris).
> * **Enkripsi**: Plaintext ditulis **mendatar per baris** dari kiri ke kanan. Lalu ciphertext dibaca **tegak lurus per kolom** dari atas ke bawah.
> * **Dekripsi**: Penerima yang memiliki tongkat berdiameter sama memasukkan ciphertext secara vertikal per kolom, lalu membaca pesan aslinya secara mendatar per baris."*

---

### 2. Rail Fence Cipher (`rail_fence.py`)
**[AKSI]**: Buka `rail_fence.py`.

**[BICARA]**:
> *"Varian kedua adalah **Rail Fence Cipher** (Sandi Zig-Zag).*
> * **Konsep**: Huruf-huruf ditulis mengikuti lintasan diagonal yang memantul naik-turun pada sejumlah $n$ rel (pagar).
> * **Siklus Pantulan**: Panjang satu gelombang penuh pantulan adalah $2(n - 1)$.
> * **Enkripsi**: Huruf ditaruh di rel zig-zag, lalu ciphertext dibaca mendatar baris per baris dari rel paling atas (rel 0) sampai rel terbawah.
> * **Dekripsi**: Kita hitung kuota karakter tiap rel, potong ciphertext sesuai kuotanya, lalu kita telusuri kembali jalur zig-zagnya untuk mengambil huruf secara berurutan."*

---

### 3. Route Cipher (`route_cipher.py`)
**[AKSI]**: Buka `route_cipher.py`.

**[BICARA]**:
> *"Varian ketiga adalah **Route Cipher** dengan rute Spiral Searah Jarum Jam (*Clockwise Inward Spiral*).*
> * **Konsep**: Plaintext ditulis mendatar ke dalam grid berukuran baris $\times$ kolom.
> * **Enkripsi**: Huruf diekstraksi mengikuti jalur melingkar spiral, mulai dari sudut kiri-atas $(0,0)$, bergerak ke kanan, ke bawah, ke kiri, lalu ke atas menuju pusat matriks.
> * **Dekripsi**: Ciphertext dimasukkan kembali mengikuti jalur spiral yang sama, lalu pesan asli dibaca secara normal baris demi baris dari kiri ke kanan."*

---

### 4. Myszkowski Cipher (`myszkowski.py`)
**[AKSI]**: Buka `myszkowski.py`.

**[BICARA]**:
> *"Varian keempat adalah **Myszkowski Cipher**, variasi Columnar Transposition ciptaan tahun 1902.*
> * **Keunggulan**: Mengizinkan kata kunci memiliki huruf kembar (misalnya kata kunci `'TOMATO'`).
> * **Aturan Khusus Myszkowski**:
>   * Huruf kunci diurutkan alfabetis untuk mendapatkan nomor ranking (A=1, M=2, O=3, T=4).
>   * Jika nomor ranking **UNIK** (hanya 1 kolom): kolom tersebut dibaca **vertikal ke bawah** ($\downarrow$).
>   * Jika nomor ranking **KEMBAR** (seperti huruf O dan T yang muncul dua kali): kolom-kolom yang ber-rank sama dibaca **mendatar per baris** ($\rightarrow$)!
> * Aturan ini membuat teks semakin acak dan tidak mudah ditebak pola kolomnya."*

---

### 5. Turning Grille / Fleissner (`turning_grille.py`)
**[AKSI]**: Buka `turning_grille.py`.

**[BICARA]**:
> *"Varian kelima adalah **Turning Grille** atau Stensil Berputar Fleissner.*
> * **Konsep**: Menggunakan pelat persegi $N \times N$ yang dilubangi pada seperempat bagiannya.
> * **Enkripsi**:
>   1. Letakkan stensil pada posisi awal (0°), tulis huruf pada lubang yang terbuka.
>   2. Putar stensil 90 derajat searah jarum jam, tulis huruf berikutnya.
>   3. Putar ke posisi 180° dan 270°, lakukan hal yang sama hingga seluruh kotak terisi penuh.
>   4. Ciphertext dibaca mendatar baris per baris.
> * **Dekripsi**: Masukkan ciphertext ke grid, lalu tumpangkan stensil dan putar 4 kali untuk membaca huruf-huruf aslinya secara bertahap."*

---

## 6. Penjelasan Antarmuka: `main.py`

**[AKSI]**: Buka file `main.py`.

**[BICARA]**:
> *"Untuk memudahkan pengujian dan presentasi, seluruh varian ini kami hubungkan ke antarmuka terminal `main.py` yang memiliki menu:*
> * **Menu 1 (Automated Test Suite)**: Menjalankan tes otomatis untuk memvalidasi keakuratan matematika kelima cipher secara instan.
> * **Menu 2 (Interactive Simulation)**: Memungkinkan kita memasukkan kata sembarang dan kunci pilihan sendiri untuk melihat visualisasi langkah per langkah."*

---

## 7. Panduan Live Demo di Terminal

**[AKSI 1 - Buka Terminal & Jalankan]**:
Ketik perintah:
```bash
python main.py
```

**[AKSI 2 - Pilih Menu 1 (Uji Otomatis)]**:
Tekan `1` lalu tekan `Enter`.
**[BICARA]**:
> *"Di layar terlihat program menjalankan pengujian otomatis untuk Scytale, Rail Fence, Route, Myszkowski, dan Turning Grille. Semua varian sukses menghasilkan status `[ PASS OK ]` yang membuktikan bahwa fungsi enkripsi dan dekripsi kami 100% konsisten."*

**[AKSI 3 - Tekan Enter, lalu Pilih Menu 2 (Simulasi Interaktif)]**:
Tekan `Enter`, lalu pilih opsi `2`.
Pilih salah satu varian, misalnya **Varian 1 (Scytale)** atau **Varian 2 (Rail Fence)**.
Tunjukkan matriks ASCII yang muncul dengan warna di terminal.
**[BICARA]**:
> *"Saat kita pilih simulasi interaktif, terminal langsung mencetak matriks 2 dimensi lengkap dengan penanda langkah dan hasil enkripsi serta dekripsinya."*

---

## 8. Antisipasi Pertanyaan Dosen (Q&A Santai)

Berikut contekan jawaban santai dan tepat jika dosen bertanya:

### Q1: "Apa bedanya cipher transposisi dengan cipher substitusi?"
> **Jawaban**:  
> *"Cipher substitusi mengganti hurufnya (misal huruf A diganti D seperti di Caesar), tapi urutannya tetap. Sedangkan cipher transposisi **hurufnya sama sekali tidak diganti**, melainkan **urutan posisinya yang ditukar-tukar** secara geometris."*

### Q2: "Mengapa teks hasil transposisi masih bisa dipecahkan?"
> **Jawaban**:  
> *"Karena huruf aslinya tidak berubah, frekuensi hurufnya masih sama seperti bahasa asli (huruf vokal seperti A, E, I tetap mendominasi). Kriptanalis bisa menyusunnya kembali menggunakan teknik anagramming atau mencocokkan pasangan dua huruf (diagram) yang sering muncul."*

### Q3: "Bagaimana cara kerja stensil Turning Grille agar saat diputar lubangnya tidak saling tumpang tindih?"
> **Jawaban**:  
> *"Di grid persegi genap, setiap sel memiliki 4 pasangan posisi rotasi (orbit 90°, 180°, 270°). Syarat stensil valid adalah dari setiap kelompok 4 sel tersebut, kita hanya boleh memilih tepat 1 lubang saja. Sehingga saat diputar 4 kali, seluruh kotak akan tertutup bergantian tanpa ada yang bertabrakan."*

---

## 9. Kalimat Penutup (Closing)

**[BICARA]**:
> *"Demikian presentasi dan demonstrasi source code Transposition Cipher dari Kelompok 2.*
> 
> *Kelima varian yang kami bangun menunjukkan bagaimana bentuk geometri 2 dimensi seperti silinder, gelombang zig-zag, spiral, perangkingan kolom, dan stensil rotasi dapat digunakan untuk mengamankan informasi secara efektif.*
> 
> *Terima kasih atas perhatian Bapak/Ibu dosen dan rekan-rekan sekalian. Jika ada pertanyaan, kami persilakan."*


