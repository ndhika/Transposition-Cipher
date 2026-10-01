"""
=============================================================================
MODUL           : scytale.py
VARIAN          : 1 — Scytale Cipher (Tongkat Sparta Kuno)
MATA KULIAH     : Kriptografi Klasik — Teknik Informatika UDINUS
KELOMPOK        : 2 (Transposition Cipher)
=============================================================================
Dokumentasi Batch:
Scytale merupakan instrumen kriptografi mekanis tertua di dunia yang digunakan
oleh bangsa Yunani Kuno (khususnya militer Sparta abad ke-5 SM). Pesan dituliskan
pada sebilah pita perkamen yang dililitkan melingkari silinder kayu berdiameter d.
Ketika pita dilepas, susunan huruf teracak secara periodik. Dekripsi mensyaratkan
silinder dengan diameter diameter identik untuk memulihkan baris pembacaan.
=============================================================================
"""

import math
from typing import Tuple, List, Optional
from utils import clean_text, pad_text, render_matrix, print_step_header, CYAN, EMERALD, PURPLE, AMBER, BOLD, RESET


# =============================================================================
# FUNGSI 1: scytale_encrypt
# =============================================================================
def scytale_encrypt(plaintext: str, key_d: int, verbose: bool = False) -> Tuple[str, List[List[str]]]:
    """
    =============================================================================
    FUNGSI / METODE : scytale_encrypt
    KATEGORI        : Algoritma Enkripsi Transposisi Silinder
    DASAR TEORI     : Merepresentasikan lilitan pita pada tongkat kayu sebagai grid
                      2D berukuran d baris x m kolom. Pesan asli ditulis mendatar
                      per baris (sesuai lilitan pita), lalu diekstraksi tegak lurus
                      per kolom ke bawah (saat pita dilepas lurus).
    -----------------------------------------------------------------------------
    FORMULA MATEMATIKA:
        d = kunci (jumlah baris / keliling silinder)
        m = ceil(|P| / d) (jumlah kolom / panjang tongkat)
        
        Pemetaan Indeks Enkripsi:
        Pesan dipetakan ke Grid[r][c] di mana index_p = (r * m) + c
        Ciphertext diambil dengan urutan kolom:
        C[(c * d) + r] = Grid[r][c]
    
    PARAMETER:
        - plaintext (str): Pesan asli yang akan dienkripsi.
        - key_d (int): Kunci diameter tongkat (jumlah baris matriks, d >= 2).
        - verbose (bool, opsional): Jika True, menampilkan visualisasi matriks 
                                   dan tahapan eksekusi secara step-by-step.
    
    OUTPUT / RETURN:
        - Tuple[str, List[List[str]]]: 
            1. Ciphertext hasil permutasi kolom.
            2. Matriks 2D konseptual silinder ukuran (d x m).
    
    KOMPLEKSITAS:
        - Waktu : O(|P|) untuk penulisan matriks dan pembacaan kolom.
        - Ruang : O(d * m) untuk alokasi matriks konseptual.
        
    CONTOH PENGGUNAAN:
        >>> ct, mat = scytale_encrypt("HELPMEARRIVE", 3)
        >>> ct
        'HMREEILAVPRE'
    =============================================================================
    """
    if key_d < 2:
        raise ValueError(f"Kunci diameter Scytale (key_d) harus >= 2 baris, diterima: {key_d}")

    clean_p = clean_text(plaintext)
    L = len(clean_p)
    if L == 0:
        return "", []

    # Hitung jumlah kolom yang diperlukan
    cols = math.ceil(L / key_d)
    total_cells = key_d * cols
    
    # Lakukan padding dummy 'X' jika panjang teks tidak habis dibagi d
    padded_p, pad_count = pad_text(clean_p, total_cells, 'X')
    
    if verbose:
        print_step_header(1, "Konstruksi Grid Silinder & Plotting Plaintext", 
                          f"Panjang |P| = {L} | Kunci d = {key_d} baris | Kolom m = {cols}")
        print(f"  Plaintext Bersih : {BOLD}{clean_p}{RESET}")
        if pad_count > 0:
            print(f"  Padding Dummy    : Ditambahkan {pad_count} karakter 'X' -> {padded_p}")

    # Buat dan isi matriks secara mendatar (baris per baris)
    matrix = []
    idx = 0
    for r in range(key_d):
        row = []
        for c in range(cols):
            row.append(padded_p[idx])
            idx += 1
        matrix.append(row)

    if verbose:
        col_headers = [f"KOL {c}" for c in range(cols)]
        row_labels = [f"BARIS {r}" for r in range(key_d)]
        print(render_matrix(matrix, col_headers=col_headers, row_labels=row_labels, color_code=CYAN))

    # Ekstraksi kolom demi kolom secara vertikal ke bawah
    ciphertext_chars = []
    column_blocks = []
    for c in range(cols):
        col_block = []
        for r in range(key_d):
            ch = matrix[r][c]
            ciphertext_chars.append(ch)
            col_block.append(ch)
        column_blocks.append("".join(col_block))

    ciphertext = "".join(ciphertext_chars)

    if verbose:
        print_step_header(2, "Ekstraksi Kolom Vertikal (Pita Dilepas)", 
                          "Membaca isi matriks ke bawah kolom demi kolom")
        for c_idx, blk in enumerate(column_blocks):
            print(f"  Kolom {c_idx} (↓) : {BOLD}{PURPLE}{blk}{RESET}")
        print(f"\n  {EMERALD}{BOLD}HASIL CIPHERTEXT SCYTALE :{RESET} {BOLD}{ciphertext}{RESET}\n")

    return ciphertext, matrix


# =============================================================================
# FUNGSI 2: scytale_decrypt
# =============================================================================
def scytale_decrypt(ciphertext: str, key_d: int, verbose: bool = False) -> Tuple[str, List[List[str]]]:
    """
    =============================================================================
    FUNGSI / METODE : scytale_decrypt
    KATEGORI        : Algoritma Dekripsi Transposisi Silinder
    DASAR TEORI     : Memulihkan plaintext dari pita Scytale dengan melilitkan
                      kembali pita ke silinder berdiameter d yang sama. Karakter
                      ciphertext diinjeksi kolom demi kolom (vertikal), lalu pesan
                      asli dibaca mendatar baris demi baris.
    -----------------------------------------------------------------------------
    FORMULA MATEMATIKA:
        d = kunci penerima (jumlah baris)
        m = |C| / d (jumlah kolom kuota per baris)
        
        Injeksi Vertikal:
        Grid[r][c] = C[(c * d) + r]
        
        Ekstraksi Horizontal Plaintext:
        P[(r * m) + c] = Grid[r][c]
    
    PARAMETER:
        - ciphertext (str): Teks terenkripsi Scytale.
        - key_d (int): Kunci diameter penerima (harus sama dengan pengirim).
        - verbose (bool, opsional): Jika True, menampilkan visualisasi proses.
    
    OUTPUT / RETURN:
        - Tuple[str, List[List[str]]]:
            1. Plaintext hasil rekonstruksi horizontal.
            2. Matriks 2D hasil lilitan ulang.
    
    KOMPLEKSITAS:
        - Waktu : O(|C|)
        - Ruang : O(d * m)
        
    CONTOH PENGGUNAAN:
        >>> pt, mat = scytale_decrypt("HMREEILAVPRE", 3)
        >>> pt
        'HELPMEARRIVE'
    =============================================================================
    """
    if key_d < 2:
        raise ValueError(f"Kunci diameter Scytale (key_d) harus >= 2 baris, diterima: {key_d}")

    clean_c = clean_text(ciphertext)
    L = len(clean_c)
    if L == 0:
        return "", []

    if L % key_d != 0:
        raise ValueError(
            f"Panjang ciphertext ({L}) tidak habis dibagi kunci diameter d ({key_d}). "
            f"Ciphertext Scytale valid harus berupa kelipatan kuota kolom yang tepat."
        )

    cols = L // key_d

    if verbose:
        print_step_header(1, "Rekonstruksi Kolom Vertikal (Pita Dililitkan Kembali)", 
                          f"Panjang |C| = {L} | Kunci Penerima d = {key_d} baris | Kolom m = {cols}")
        print(f"  Ciphertext Masukan : {BOLD}{clean_c}{RESET}")

    # Inisialisasi matriks kosong (d baris x cols kolom)
    matrix = [[''] * cols for _ in range(key_d)]

    # Isi kolom demi kolom secara vertikal
    idx = 0
    for c in range(cols):
        for r in range(key_d):
            matrix[r][c] = clean_c[idx]
            idx += 1

    if verbose:
        col_headers = [f"KOL {c}" for c in range(cols)]
        row_labels = [f"BARIS {r}" for r in range(key_d)]
        print(render_matrix(matrix, col_headers=col_headers, row_labels=row_labels, color_code=EMERALD))

    # Ekstraksi mendatar per baris dari kiri ke kanan
    plaintext_chars = []
    row_words = []
    for r in range(key_d):
        row_str = "".join(matrix[r])
        row_words.append(row_str)
        plaintext_chars.append(row_str)

    plaintext = "".join(plaintext_chars)

    if verbose:
        print_step_header(2, "Pembacaan Mendatar per Baris (Plaintext Berhasil Pulih)", 
                          "Membaca sepanjang keliling silinder secara horizontal (→)")
        for r_idx, w in enumerate(row_words):
            print(f"  Baris {r_idx} (→) : {BOLD}{CYAN}{w}{RESET}")
        print(f"\n  {EMERALD}{BOLD}HASIL DEKRIPSI SCYTALE :{RESET} {BOLD}{plaintext}{RESET} ✓\n")

    return plaintext, matrix


# =============================================================================
# BLOK TESTING MANDIRI
# =============================================================================
if __name__ == "__main__":
    print(f"\n{BOLD}{PURPLE}=== DEMO MODUL SCYTALE CIPHER (KELOMPOK 2) ==={RESET}")
    sampel_pt = "HELPMEARRIVE"
    kunci = 3
    
    ct, _ = scytale_encrypt(sampel_pt, kunci, verbose=True)
    pt, _ = scytale_decrypt(ct, kunci, verbose=True)
    
    assert pt == sampel_pt, f"Gagal: Ekspektasi {sampel_pt}, diperoleh {pt}"
    print(f"{EMERALD}{BOLD}UJI VALIDASI SCYTALE 100% SUKSES TEPAT DENGAN SLIDE 05-08!{RESET}\n")
