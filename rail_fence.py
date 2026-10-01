"""
=============================================================================
MODUL           : rail_fence.py
VARIAN          : 2 — Rail Fence Cipher (Zig-Zag Transposition)
MATA KULIAH     : Kriptografi Klasik — Teknik Informatika UDINUS
KELOMPOK        : 2 (Transposition Cipher)
=============================================================================
Dokumentasi Batch:
Rail Fence Cipher memetakan karakter-karakter plaintext ke lintasan bergelombang
seperti pagar rel (zig-zag wave). Karakter bergerak diagonal turun hingga menyentuh
rel terbawah (kedalaman n-1), lalu berbalik memantul diagonal naik hingga menyentuh
rel teratas (rel 0), dan berulang secara periodik dengan periode T = 2(n - 1).
=============================================================================
"""

from typing import Tuple, List
from utils import clean_text, render_matrix, print_step_header, CYAN, EMERALD, PURPLE, AMBER, BOLD, RESET, DIM


# =============================================================================
# FUNGSI 1: get_rail_indices
# =============================================================================
def get_rail_indices(length: int, num_rails: int) -> List[int]:
    """
    =============================================================================
    FUNGSI / METODE : get_rail_indices
    KATEGORI        : Fungsi Pembantu Geometri / Lintasan Gelombang
    DASAR TEORI     : Menghitung nomor rel (0 s.d. n-1) untuk setiap indeks
                      karakter 0 s.d. L-1 berdasarkan fungsi gelombang segitiga
                      dengan periode T = 2(n - 1).
    -----------------------------------------------------------------------------
    FORMULA MATEMATIKA:
        T = 2 * (n - 1)
        mod_val = i mod T
        rail(i) = mod_val          jika mod_val < n
        rail(i) = T - mod_val      jika mod_val >= n
    
    PARAMETER:
        - length (int): Panjang total string teks (L).
        - num_rails (int): Kedalaman pagar / jumlah rel (n >= 2).
    
    OUTPUT / RETURN:
        - List[int]: Array berisi nomor rel untuk setiap posisi karakter i.
    =============================================================================
    """
    if num_rails <= 1:
        return [0] * length
        
    cycle = 2 * (num_rails - 1)
    rails = []
    for i in range(length):
        m = i % cycle
        if m < num_rails:
            rails.append(m)
        else:
            rails.append(cycle - m)
    return rails


# =============================================================================
# FUNGSI 2: rail_fence_encrypt
# =============================================================================
def rail_fence_encrypt(plaintext: str, num_rails: int, verbose: bool = False) -> Tuple[str, List[List[str]]]:
    """
    =============================================================================
    FUNGSI / METODE : rail_fence_encrypt
    KATEGORI        : Algoritma Enkripsi Transposisi Zig-Zag
    DASAR TEORI     : Memetakan teks ke kisi berukuran n rel x L kolom. Karakter
                      hanya mengisi posisi zig-zag, sementara sel lain bernilai kosong.
                      Ciphertext dibentuk dengan membaca huruf dari rel teratas (rel 0)
                      hingga rel terbawah (rel n-1).
    -----------------------------------------------------------------------------
    PARAMETER:
        - plaintext (str): Pesan asli yang akan dienkripsi.
        - num_rails (int): Jumlah rel/pagar (kedalaman n >= 2).
        - verbose (bool, opsional): Jika True, menampilkan visualisasi rel zig-zag.
    
    OUTPUT / RETURN:
        - Tuple[str, List[List[str]]]:
            1. Ciphertext hasil penggabungan rel terurut.
            2. Matriks visual 2D (num_rails x |P|) yang memperlihatkan lintasan gelombang.
    
    KOMPLEKSITAS:
        - Waktu : O(|P|)
        - Ruang : O(n * |P|)
        
    CONTOH PENGGUNAAN:
        >>> ct, _ = rail_fence_encrypt("KRIPTOGRAFI", 3)
        >>> ct
        'KTARPORFIGI'
    =============================================================================
    """
    if num_rails < 2:
        raise ValueError(f"Jumlah rel Rail Fence harus >= 2, diterima: {num_rails}")

    clean_p = clean_text(plaintext)
    L = len(clean_p)
    if L == 0:
        return "", []

    cycle = 2 * (num_rails - 1)
    rail_assignment = get_rail_indices(L, num_rails)

    # Konstruksi matriks representasi zig-zag (n x L)
    grid = [['.'] * L for _ in range(num_rails)]
    for col_idx, char in enumerate(clean_p):
        r_idx = rail_assignment[col_idx]
        grid[r_idx][col_idx] = char

    if verbose:
        print_step_header(1, "Plotting Karakter ke Lintasan Gelombang Zig-Zag", 
                          f"Panjang |P| = {L} | Jumlah Rel n = {num_rails} | Periode Siklus T = 2*(n-1) = {cycle}")
        print(f"  Plaintext Bersih : {BOLD}{clean_p}{RESET}\n")
        
        # Cetak rel dengan pewarnaan menarik
        col_headers = [str(i) for i in range(L)]
        row_labels = [f"REL {r}" for r in range(num_rails)]
        print(render_matrix(grid, col_headers=col_headers, row_labels=row_labels, color_code=CYAN))

    # Ekstraksi karakter baris per baris (rel per rel)
    rail_strings = []
    ciphertext_chars = []
    for r in range(num_rails):
        chars_in_rail = [grid[r][c] for c in range(L) if grid[r][c] != '.']
        s = "".join(chars_in_rail)
        rail_strings.append(s)
        ciphertext_chars.extend(chars_in_rail)

    ciphertext = "".join(ciphertext_chars)

    if verbose:
        print_step_header(2, "Ekstraksi Karakter Rel Demi Rel", 
                          "Membaca isi matriks secara mendatar per rel dari atas ke bawah")
        for r_idx, rs in enumerate(rail_strings):
            print(f"  Rel {r_idx} (Kapasitas {len(rs)} huruf) : {BOLD}{PURPLE}{rs}{RESET}")
        print(f"\n  {EMERALD}{BOLD}HASIL CIPHERTEXT RAIL FENCE :{RESET} {BOLD}{ciphertext}{RESET}\n")

    return ciphertext, grid


# =============================================================================
# FUNGSI 3: rail_fence_decrypt
# =============================================================================
def rail_fence_decrypt(ciphertext: str, num_rails: int, verbose: bool = False) -> Tuple[str, List[List[str]]]:
    """
    =============================================================================
    FUNGSI / METODE : rail_fence_decrypt
    KATEGORI        : Algoritma Dekripsi Transposisi Zig-Zag
    DASAR TEORI     : Merekonstruksi pola zig-zag asli dengan menghitung kuota
                      karakter pada masing-masing rel, mempartisi ciphertext ke
                      rel-rel tersebut, lalu menelusuri lintasan gelombang untuk
                      mengambil karakter secara berurutan waktu i = 0 s.d. L-1.
    -----------------------------------------------------------------------------
    PARAMETER:
        - ciphertext (str): Ciphertext yang akan didekripsi.
        - num_rails (int): Kedalaman rel penerima.
        - verbose (bool, opsional): Jika True, menampilkan visualisasi pemulihan.
    
    OUTPUT / RETURN:
        - Tuple[str, List[List[str]]]:
            1. Plaintext hasil pemulihan.
            2. Matriks rel zig-zag hasil rekonstruksi.
    
    KOMPLEKSITAS:
        - Waktu : O(|C|)
        - Ruang : O(n * |C|)
        
    CONTOH PENGGUNAAN:
        >>> pt, _ = rail_fence_decrypt("KTARPORFIGI", 3)
        >>> pt
        'KRIPTOGRAFI'
    =============================================================================
    """
    if num_rails < 2:
        raise ValueError(f"Jumlah rel Rail Fence harus >= 2, diterima: {num_rails}")

    clean_c = clean_text(ciphertext)
    L = len(clean_c)
    if L == 0:
        return "", []

    rail_assignment = get_rail_indices(L, num_rails)

    # Hitung kuota karakter tiap rel
    rail_counts = [0] * num_rails
    for r in rail_assignment:
        rail_counts[r] += 1

    if verbose:
        print_step_header(1, "Analisis Kuota Karakter per Rel", 
                          f"Panjang |C| = {L} | Rel n = {num_rails}")
        print(f"  Ciphertext Masukan : {BOLD}{clean_c}{RESET}")
        for r_idx, cnt in enumerate(rail_counts):
            print(f"  Rel {r_idx} menampung tepat : {BOLD}{AMBER}{cnt}{RESET} karakter")

    # Partisi ciphertext ke dalam segmen tiap rel
    rail_segments = []
    current_idx = 0
    for r in range(num_rails):
        cnt = rail_counts[r]
        segment = clean_c[current_idx : current_idx + cnt]
        rail_segments.append(list(segment))
        current_idx += cnt

    # Injeksi segmen ke matriks grid rel
    grid = [['.'] * L for _ in range(num_rails)]
    rail_pointers = [0] * num_rails
    for col_idx in range(L):
        r_target = rail_assignment[col_idx]
        grid[r_target][col_idx] = rail_segments[r_target][rail_pointers[r_target]]
        rail_pointers[r_target] += 1

    if verbose:
        col_headers = [str(i) for i in range(L)]
        row_labels = [f"REL {r}" for r in range(num_rails)]
        print("\n  Matriks Rekonstruksi Rel:")
        print(render_matrix(grid, col_headers=col_headers, row_labels=row_labels, color_code=EMERALD))

    # Telusuri gelombang zig-zag dari kolom 0 s.d. L-1 untuk membaca plaintext
    plaintext_chars = []
    for col_idx in range(L):
        r = rail_assignment[col_idx]
        plaintext_chars.append(grid[r][col_idx])

    plaintext = "".join(plaintext_chars)

    if verbose:
        print_step_header(2, "Penelusuran Lintasan Zig-Zag (Pemulihan Plaintext)", 
                          "Membaca sel demi sel mengikuti gelombang diagonal i = 0 s.d. L-1")
        print(f"  {EMERALD}{BOLD}HASIL DEKRIPSI RAIL FENCE :{RESET} {BOLD}{plaintext}{RESET} ✓\n")

    return plaintext, grid


# =============================================================================
# BLOK TESTING MANDIRI
# =============================================================================
if __name__ == "__main__":
    print(f"\n{BOLD}{PURPLE}=== DEMO MODUL RAIL FENCE CIPHER (KELOMPOK 2) ==={RESET}")
    sampel_pt = "KRIPTOGRAFI"
    rel = 3
    
    ct, _ = rail_fence_encrypt(sampel_pt, rel, verbose=True)
    pt, _ = rail_fence_decrypt(ct, rel, verbose=True)
    
    assert pt == sampel_pt, f"Gagal: Ekspektasi {sampel_pt}, diperoleh {pt}"
    print(f"{EMERALD}{BOLD}UJI VALIDASI RAIL FENCE 100% SUKSES TEPAT DENGAN SLIDE 09-13!{RESET}\n")
