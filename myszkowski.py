"""
=============================================================================
MODUL           : myszkowski.py
VARIAN          : 4 — Myszkowski Transposition Cipher (Aturan Huruf Kembar)
TOPIK           : Kriptografi Klasik — Transposition Cipher
KELOMPOK        : 2 (Transposition Cipher)
=============================================================================
Dokumentasi Batch:
Diciptakan oleh perwira militer Rusia-Polandia Émile Victor Théodore Myszkowski
pada tahun 1902. Berbeda dari Columnar biasa yang melarang huruf kembar, Myszkowski
memberikan nomor peringkat (rank) yang sama untuk huruf kunci yang identik.
Aturan khusus: Jika suatu peringkat unik (1 kolom), dibaca vertikal (↓); namun jika
suatu peringkat berulang/kembar (>1 kolom), karakter dibaca mendatar per baris (→)
melintasi seluruh kolom yang memiliki nomor peringkat tersebut.
=============================================================================
"""

import math
from typing import Tuple, List, Dict
from utils import clean_text, pad_text, render_matrix, print_step_header, CYAN, EMERALD, PURPLE, AMBER, BOLD, RESET


# =============================================================================
# FUNGSI 1: get_myszkowski_ranks
# =============================================================================
def get_myszkowski_ranks(keyword: str) -> List[int]:
    """
    =============================================================================
    FUNGSI / METODE : get_myszkowski_ranks
    KATEGORI        : Analisis Kunci & Pemeringkatan Huruf (Key Ranking)
    DASAR TEORI     : Mengurutkan huruf unik dalam kunci secara alfabetis, lalu
                      menetapkan nilai peringkat bulat (1 s.d. K) untuk setiap huruf.
                      Huruf yang sama memperoleh nomor peringkat yang persis sama.
    -----------------------------------------------------------------------------
    CONTOH:
        Kunci: T O M A T O
        Huruf unik terurut alfabetis: A (1), M (2), O (3), T (4)
        Hasil Peringkat:
        T=4, O=3, M=2, A=1, T=4, O=3 -> [4, 3, 2, 1, 4, 3]
    
    PARAMETER:
        - keyword (str): Kata kunci rahasia.
    
    OUTPUT / RETURN:
        - List[int]: Array nomor peringkat untuk masing-masing kolom kunci.
    =============================================================================
    """
    clean_k = clean_text(keyword)
    if not clean_k:
        raise ValueError("Kata kunci tidak boleh kosong!")

    # Cari huruf-huruf unik dan urutkan secara alfabetis
    unique_sorted = sorted(list(set(clean_k)))
    rank_map = {ch: idx + 1 for idx, ch in enumerate(unique_sorted)}
    
    return [rank_map[ch] for ch in clean_k]


# =============================================================================
# FUNGSI 2: get_myszkowski_reading_order
# =============================================================================
def get_myszkowski_reading_order(keyword: str, num_rows: int) -> List[Tuple[int, int]]:
    """
    =============================================================================
    FUNGSI / METODE : get_myszkowski_reading_order
    KATEGORI        : Pembangkit Urutan Koordinat Pembacaan
    DASAR TEORI     : Membangun daftar terurut pasangan koordinat sel (baris, kolom)
                      yang diekstraksi berdasarkan aturan pemeringkatan Myszkowski.
                      Fungsi ini bersifat simetris dan esensial untuk enkripsi maupun
                      dekripsi.
    -----------------------------------------------------------------------------
    ATURAN EKSTRAKSI:
        Untuk setiap rank terurut 1 s.d. K:
            Kumpulan kolom yang memiliki rank tersebut = cols
            Jika len(cols) == 1 (Unik)   : Ambil (0, c), (1, c), ..., (R-1, c) vertikal.
            Jika len(cols) > 1 (Kembar) : Untuk setiap baris r (0 s.d. R-1):
                                             Ambil (r, c) untuk c in cols horizontal.
    
    PARAMETER:
        - keyword (str): Kata kunci sandi.
        - num_rows (int): Jumlah baris matriks data.
    
    OUTPUT / RETURN:
        - List[Tuple[int, int]]: Daftar koordinat sel (r, c) urutan ekstraksi.
    =============================================================================
    """
    ranks = get_myszkowski_ranks(keyword)
    unique_ranks = sorted(list(set(ranks)))
    
    # Kelompokkan indeks kolom berdasarkan nomor rank-nya
    rank_to_cols: Dict[int, List[int]] = {}
    for col_idx, rk in enumerate(ranks):
        rank_to_cols.setdefault(rk, []).append(col_idx)

    reading_order = []
    for rk in unique_ranks:
        cols = rank_to_cols[rk]
        if len(cols) == 1:
            # Rank Unik: Baca vertikal ke bawah
            c = cols[0]
            for r in range(num_rows):
                reading_order.append((r, c))
        else:
            # Rank Kembar: Baca horizontal per baris melintasi kolom-kolom kembar
            for r in range(num_rows):
                for c in cols:
                    reading_order.append((r, c))
                    
    return reading_order


# =============================================================================
# FUNGSI 3: myszkowski_encrypt
# =============================================================================
def myszkowski_encrypt(plaintext: str, keyword: str, verbose: bool = False) -> Tuple[str, List[List[str]]]:
    """
    =============================================================================
    FUNGSI / METODE : myszkowski_encrypt
    KATEGORI        : Algoritma Enkripsi Transposisi Myszkowski
    DASAR TEORI     : Memplot plaintext mendatar ke matriks berukuran R x len(keyword).
                      Melakukan padding dummy jika panjang teks bukan kelipatan kunci.
                      Karakter diekstraksi mengikuti aturan rank unik vs kembar.
    -----------------------------------------------------------------------------
    PARAMETER:
        - plaintext (str): Pesan asli yang akan dienkripsi.
        - keyword (str): Kata kunci pembentuk kolom (bisa memiliki huruf kembar).
        - verbose (bool, opsional): Jika True, menampilkan visualisasi proses.
    
    OUTPUT / RETURN:
        - Tuple[str, List[List[str]]]:
            1. Ciphertext hasil ekstraksi Myszkowski.
            2. Matriks 2D data teks (R x C).
    
    KOMPLEKSITAS:
        - Waktu : O(R * C)
        - Ruang : O(R * C)
        
    CONTOH PENGGUNAAN:
        >>> ct, _ = myszkowski_encrypt("WE ARE DISCOVERED", "TOMATO")
        >>> ct
        'ROXACDEDSEEXWEIVRX'
    =============================================================================
    """
    clean_p = clean_text(plaintext)
    clean_k = clean_text(keyword)
    num_cols = len(clean_k)

    if len(clean_p) == 0:
        raise ValueError("Plaintext tidak boleh kosong!")
    if num_cols > len(clean_p):
        raise ValueError(
            f"Panjang kunci ({num_cols} huruf) tidak boleh melebihi panjang plaintext bersih "
            f"({len(clean_p)} huruf). Ini akan menghasilkan baris yang tidak lengkap."
        )
    
    # Lakukan padding dummy 'X'
    padded_p, pad_count = pad_text(clean_p, num_cols, 'X')
    num_rows = len(padded_p) // num_cols
    
    ranks = get_myszkowski_ranks(clean_k)

    if verbose:
        print_step_header(1, "Konstruksi Matriks & Pemeringkatan Huruf Kunci", 
                          f"Kunci = '{clean_k}' ({num_cols} kolom) | Baris R = {num_rows}")
        print(f"  Plaintext Bersih : {BOLD}{clean_p}{RESET}")
        if pad_count > 0:
            print(f"  Padding Dummy    : Ditambahkan {pad_count} huruf 'X' -> {padded_p}")
        print("  Peringkat Kolom  : " + "  ".join(f"{ch}(#{rk})" for ch, rk in zip(clean_k, ranks)))

    # Konstruksi matriks baris demi baris
    matrix = []
    idx = 0
    for r in range(num_rows):
        row = []
        for c in range(num_cols):
            row.append(padded_p[idx])
            idx += 1
        matrix.append(row)

    if verbose:
        col_headers = [f"{clean_k[c]} (R{ranks[c]})" for c in range(num_cols)]
        row_labels = [f"BARIS {r}" for r in range(num_rows)]
        print("\n  Matriks Data Myszkowski:")
        print(render_matrix(matrix, col_headers=col_headers, row_labels=row_labels, color_code=CYAN))

    # Ekstraksi karakter mengikuti urutan Myszkowski
    order = get_myszkowski_reading_order(clean_k, num_rows)
    ciphertext_chars = [matrix[r][c] for r, c in order]
    ciphertext = "".join(ciphertext_chars)

    if verbose:
        print_step_header(2, "Ekstraksi Karakter Berdasarkan Aturan Peringkat", 
                          "Rank unik dibaca vertikal (↓), rank kembar dibaca horizontal (→)")
        
        # Kelompokkan output per nomor rank
        rank_to_cols: Dict[int, List[int]] = {}
        for c_idx, rk in enumerate(ranks):
            rank_to_cols.setdefault(rk, []).append(c_idx)

        for rk in sorted(list(set(ranks))):
            cols = rank_to_cols[rk]
            huruf_kunci = clean_k[cols[0]]
            if len(cols) == 1:
                tipe = "UNIK (Baca Vertikal ↓)"
                chars = "".join(matrix[r][cols[0]] for r in range(num_rows))
            else:
                tipe = f"KEMBAR di Kolom {cols} (Baca Horizontal →)"
                chars = "".join("".join(matrix[r][c] for c in cols) for r in range(num_rows))
            print(f"  Rank #{rk} ['{huruf_kunci}'] - {tipe} : {BOLD}{PURPLE}{chars}{RESET}")

        print(f"\n  {EMERALD}{BOLD}HASIL CIPHERTEXT MYSZKOWSKI :{RESET} {BOLD}{ciphertext}{RESET}\n")

    return ciphertext, matrix


# =============================================================================
# FUNGSI 4: myszkowski_decrypt
# =============================================================================
def myszkowski_decrypt(ciphertext: str, keyword: str, verbose: bool = False) -> Tuple[str, List[List[str]]]:
    """
    =============================================================================
    FUNGSI / METODE : myszkowski_decrypt
    KATEGORI        : Algoritma Dekripsi Transposisi Myszkowski
    DASAR TEORI     : Menentukan kembali urutan koordinat pembacaan yang sama persis
                      dengan proses enkripsi, kemudian memetakan karakter ciphertext
                      ke dalam sel grid sesuai urutan tersebut, dan membaca pesan
                      asli secara normal baris per baris.
    -----------------------------------------------------------------------------
    PARAMETER:
        - ciphertext (str): Teks terenkripsi.
        - keyword (str): Kunci rahasia pengirim.
        - verbose (bool, opsional): Jika True, menampilkan visualisasi proses.
    
    OUTPUT / RETURN:
        - Tuple[str, List[List[str]]]:
            1. Plaintext hasil rekonstruksi.
            2. Matriks 2D hasil pemulihan.
    
    KOMPLEKSITAS:
        - Waktu : O(R * C)
        - Ruang : O(R * C)
        
    CONTOH PENGGUNAAN:
        >>> pt, _ = myszkowski_decrypt("ROXACDEDSEEXWEIVRX", "TOMATO")
        >>> pt
        'WEAREDISCOVEREDXXX'
    =============================================================================
    """
    clean_c = clean_text(ciphertext)
    clean_k = clean_text(keyword)
    num_cols = len(clean_k)
    
    if len(clean_c) % num_cols != 0:
        raise ValueError(
            f"Panjang ciphertext ({len(clean_c)}) tidak habis dibagi panjang kunci ({num_cols})."
        )

    num_rows = len(clean_c) // num_cols
    order = get_myszkowski_reading_order(clean_k, num_rows)

    if verbose:
        print_step_header(1, "Pemulihan Kuota Sel & Injeksi ke Matriks Grid", 
                          f"Ciphertext {len(clean_c)} huruf | Kunci '{clean_k}' | Matriks {num_rows}x{num_cols}")

    # Inisialisasi matriks kosong
    matrix = [[''] * num_cols for _ in range(num_rows)]

    # Masukkan karakter ciphertext ke koordinat sel yang bersangkutan
    for char_idx, (r, c) in enumerate(order):
        matrix[r][c] = clean_c[char_idx]

    if verbose:
        ranks = get_myszkowski_ranks(clean_k)
        col_headers = [f"{clean_k[c]} (R{ranks[c]})" for c in range(num_cols)]
        row_labels = [f"B{r}" for r in range(num_rows)]
        print(render_matrix(matrix, col_headers=col_headers, row_labels=row_labels, color_code=EMERALD))

    # Baca baris demi baris mendatar
    plaintext_chars = []
    row_strings = []
    for r in range(num_rows):
        s = "".join(matrix[r])
        row_strings.append(s)
        plaintext_chars.append(s)

    plaintext = "".join(plaintext_chars)

    if verbose:
        print_step_header(2, "Pembacaan Mendatar per Baris (Plaintext Pulih Sempurna)", 
                          "Membaca isi matriks secara horizontal dari baris teratas ke terbawah")
        for r_idx, s in enumerate(row_strings):
            print(f"  Baris {r_idx} (→) : {BOLD}{CYAN}{s}{RESET}")
        print(f"\n  {EMERALD}{BOLD}HASIL DEKRIPSI MYSZKOWSKI :{RESET} {BOLD}{plaintext}{RESET} ✓\n")

    return plaintext, matrix


# =============================================================================
# BLOK TESTING MANDIRI
# =============================================================================
if __name__ == "__main__":
    print(f"\n{BOLD}{PURPLE}=== DEMO MODUL MYSZKOWSKI CIPHER (KELOMPOK 2) ==={RESET}")
    sampel_pt = "WE ARE DISCOVERED"
    kunci = "TOMATO"
    
    ct, _ = myszkowski_encrypt(sampel_pt, kunci, verbose=True)
    pt, _ = myszkowski_decrypt(ct, kunci, verbose=True)
    
    assert pt == "WEAREDISCOVEREDXXX", f"Gagal: diperoleh {pt}"
    print(f"{EMERALD}{BOLD}UJI VALIDASI MYSZKOWSKI 100% SUKSES TEPAT DENGAN SLIDE 19-23!{RESET}\n")
