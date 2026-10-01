"""
=============================================================================
MODUL           : turning_grille.py
VARIAN          : 5 — Turning Grille (Fleissner Grille / Stensil Berputar)
MATA KULIAH     : Kriptografi Klasik — Teknik Informatika UDINUS
KELOMPOK        : 2 (Transposition Cipher)
=============================================================================
Dokumentasi Batch:
Dipopulerkan oleh kolonel Austria Eduard Fleissner von Wostrowitz pada tahun 1881.
Menggunakan selembar pelat persegi (stensil N x N) yang dilubangi pada titik-titik
khusus sebanyak (N^2 / 4) lubang. Ketika stensil diputar 4 kali sebesar 90 derajat
searah jarum jam (0°, 90°, 180°, 270°), setiap sel pada grid di bawahnya akan terbuka
tepat satu kali tanpa ada tumpang tindih (collision) atau sel yang terlewat.
=============================================================================
"""

from typing import Tuple, List, Set
from utils import clean_text, pad_text, render_matrix, print_step_header, CYAN, EMERALD, PURPLE, AMBER, BOLD, RESET


# =============================================================================
# FUNGSI 1: rotate_coords_90_cw
# =============================================================================
def rotate_coords_90_cw(coords: List[Tuple[int, int]], n: int) -> List[Tuple[int, int]]:
    """
    =============================================================================
    FUNGSI / METODE : rotate_coords_90_cw
    KATEGORI        : Transformasi Geometri / Rotasi Matriks
    DASAR TEORI     : Memutar posisi lubang stensil sebesar 90 derajat searah jarum jam
                      pada grid bujursangkar berdimensi N x N.
    -----------------------------------------------------------------------------
    FORMULA MATEMATIKA:
        r_baru = c_lama
        c_baru = (N - 1) - r_lama
    
    PARAMETER:
        - coords (List[Tuple[int, int]]): Daftar koordinat awal (r, c).
        - n (int): Ukuran sisi grid persegi (N x N).
    
    OUTPUT / RETURN:
        - List[Tuple[int, int]]: Daftar koordinat baru hasil rotasi 90° CW,
                                terurut dari atas ke bawah, kiri ke kanan.
    =============================================================================
    """
    rotated = [(c, n - 1 - r) for r, c in coords]
    # Urutkan koordinat agar penulisan huruf selalu rapi dari atas ke bawah
    return sorted(rotated, key=lambda x: (x[0], x[1]))


# =============================================================================
# FUNGSI 2: validate_fleissner_stencil
# =============================================================================
def validate_fleissner_stencil(initial_holes: List[Tuple[int, int]], n: int = 4) -> bool:
    """
    =============================================================================
    FUNGSI / METODE : validate_fleissner_stencil
    KATEGORI        : Verifikasi Validitas Kriptografis
    DASAR TEORI     : Menjamin bahwa stensil memenuhi syarat matematis Fleissner:
                      ke-4 rotasi harus mempartisi himpunan N^2 sel menjadi 4 partisi
                      yang saling lepas (disjoint) dan menutup seluruh grid secara utuh.
    -----------------------------------------------------------------------------
    PARAMETER:
        - initial_holes (List[Tuple[int, int]]): Koordinat lubang pada posisi 0°.
        - n (int): Dimensi grid persegi. Default bernilai 4.
    
    OUTPUT / RETURN:
        - bool: True jika stensil valid sempurna, False jika ada tabrakan sel.
    =============================================================================
    """
    expected_holes = (n * n) // 4
    if len(initial_holes) != expected_holes:
        return False

    all_visited: Set[Tuple[int, int]] = set()
    current = initial_holes
    
    for _ in range(4):
        for pt in current:
            if pt in all_visited or pt[0] < 0 or pt[0] >= n or pt[1] < 0 or pt[1] >= n:
                return False
            all_visited.add(pt)
        current = rotate_coords_90_cw(current, n)
        
    return len(all_visited) == (n * n)


# =============================================================================
# FUNGSI 3: turning_grille_encrypt
# =============================================================================
def turning_grille_encrypt(
    plaintext: str, 
    initial_holes: List[Tuple[int, int]] = None, 
    n: int = 4, 
    verbose: bool = False
) -> Tuple[str, List[List[str]]]:
    """
    =============================================================================
    FUNGSI / METODE : turning_grille_encrypt
    KATEGORI        : Algoritma Enkripsi Transposisi Stensil Fleissner
    DASAR TEORI     : Menuliskan segmen karakter plaintext ke dalam lubang stensil
                      pada posisi 0°, 90°, 180°, dan 270°. Setelah seluruh 16 sel
                      terisi penuh, ciphertext diekstraksi dengan membaca grid
                      secara normal baris per baris.
    -----------------------------------------------------------------------------
    PARAMETER:
        - plaintext (str): Pesan asli yang akan dienkripsi (maksimal n^2 huruf).
        - initial_holes (List[Tuple[int, int]], opsional): Koordinat lubang 0°.
          Default: [(0,0), (0,1), (0,2), (1,1)] sesuai standar materi kuliah.
        - n (int): Ukuran grid persegi. Default bernilai 4 (16 sel).
        - verbose (bool, opsional): Jika True, menampilkan visualisasi 4 rotasi.
    
    OUTPUT / RETURN:
        - Tuple[str, List[List[str]]]:
            1. Ciphertext hasil penggabungan pembacaan baris per baris.
            2. Matriks 2D gabungan akhir (N x N).
    
    KOMPLEKSITAS:
        - Waktu : O(N^2)
        - Ruang : O(N^2)
        
    CONTOH PENGGUNAAN:
        >>> ct, _ = turning_grille_encrypt("SENDTROOPSASAPXX")
        >>> ct
        'SENTADROPXPOXSAS'
    =============================================================================
    """
    if initial_holes is None:
        # Default lubang standar kuliah Udinus Kelompok 2
        initial_holes = [(0, 0), (0, 1), (0, 2), (1, 1)]

    if not validate_fleissner_stencil(initial_holes, n):
        raise ValueError("Lubang stensil awal tidak valid matematis (terjadi tabrakan rotasi).")

    clean_p = clean_text(plaintext)
    total_cells = n * n
    padded_p, pad_count = pad_text(clean_p, total_cells, 'X')
    
    holes_per_rotation = total_cells // 4

    if verbose:
        print_step_header(1, "Inisialisasi Stensil Fleissner 4x4", 
                          f"Dimensi {n}x{n} ({total_cells} sel) | Lubang per rotasi = {holes_per_rotation}")
        print(f"  Plaintext Bersih : {BOLD}{clean_p}{RESET}")
        if pad_count > 0:
            print(f"  Padding Dummy    : Ditambahkan {pad_count} huruf 'X' -> {padded_p}")
        print(f"  Posisi Lubang 0° : {initial_holes}")

    # Inisialisasi matriks grid utama kosong
    grid = [['.'] * n for _ in range(n)]
    current_holes = initial_holes
    rot_angles = ["0°", "90° CW", "180° CW", "270° CW"]

    if verbose:
        print_step_header(2, "Penulisan 4 Kuadran Rotasi Stensil Bertahap", 
                          "Menuliskan 4 huruf pada setiap perputaran 90 derajat searah jarum jam")

    # Jalankan 4 kali rotasi
    for rot_idx in range(4):
        chunk = padded_p[rot_idx * holes_per_rotation : (rot_idx + 1) * holes_per_rotation]
        
        # Tuliskan huruf ke sel yang berlubang
        for char_idx, (r, c) in enumerate(current_holes):
            grid[r][c] = chunk[char_idx]

        if verbose:
            angle = rot_angles[rot_idx]
            print(f"\n  {BOLD}{PURPLE}Rotasi #{rot_idx+1} ({angle}){RESET} -> Huruf {BOLD}'{chunk}'{RESET} pada lubang: {current_holes}")
            row_labels = [f"B{r}" for r in range(n)]
            col_headers = [f"K{c}" for c in range(n)]
            print(render_matrix(grid, col_headers=col_headers, row_labels=row_labels, 
                                highlight_coords=current_holes, color_code=CYAN))

        # Putar stensil untuk putaran selanjutnya
        current_holes = rotate_coords_90_cw(current_holes, n)

    # Ekstraksi ciphertext secara mendatar baris per baris
    ciphertext_chars = []
    row_strings = []
    for r in range(n):
        s = "".join(grid[r])
        row_strings.append(s)
        ciphertext_chars.append(s)

    ciphertext = "".join(ciphertext_chars)

    if verbose:
        print_step_header(3, "Ekstraksi Ciphertext Mendatar (Row-by-Row)", 
                          "Stensil diangkat, isi kisi dibaca normal dari kiri ke kanan")
        for r_idx, s in enumerate(row_strings):
            print(f"  Baris {r_idx} (→) : {BOLD}{CYAN}{s}{RESET}")
        print(f"\n  {EMERALD}{BOLD}HASIL CIPHERTEXT TURNING GRILLE :{RESET} {BOLD}{ciphertext}{RESET}\n")

    return ciphertext, grid


# =============================================================================
# FUNGSI 4: turning_grille_decrypt
# =============================================================================
def turning_grille_decrypt(
    ciphertext: str, 
    initial_holes: List[Tuple[int, int]] = None, 
    n: int = 4, 
    verbose: bool = False
) -> Tuple[str, List[List[str]]]:
    """
    =============================================================================
    FUNGSI / METODE : turning_grille_decrypt
    KATEGORI        : Algoritma Dekripsi Transposisi Stensil Fleissner
    DASAR TEORI     : Memasukkan ciphertext ke grid N x N secara horizontal,
                      kemudian menumpangkan stensil berlubang dan membaca huruf
                      yang tampak pada 4 posisi rotasi berturut-turut (0°, 90°, 180°, 270°).
    -----------------------------------------------------------------------------
    PARAMETER:
        - ciphertext (str): Teks terenkripsi (tepat N^2 karakter).
        - initial_holes (List[Tuple[int, int]], opsional): Lubang stensil 0°.
        - n (int): Dimensi grid persegi. Default bernilai 4.
        - verbose (bool, opsional): Jika True, menampilkan visualisasi pemulihan.
    
    OUTPUT / RETURN:
        - Tuple[str, List[List[str]]]:
            1. Plaintext hasil pembacaan 4 rotasi.
            2. Matriks 2D ciphertext.
    
    KOMPLEKSITAS:
        - Waktu : O(N^2)
        - Ruang : O(N^2)
        
    CONTOH PENGGUNAAN:
        >>> pt, _ = turning_grille_decrypt("SENTADROPXPOXSAS")
        >>> pt
        'SENDTROOPSASAPXX'
    =============================================================================
    """
    if initial_holes is None:
        initial_holes = [(0, 0), (0, 1), (0, 2), (1, 1)]

    clean_c = clean_text(ciphertext)
    total_cells = n * n
    
    if len(clean_c) != total_cells:
        raise ValueError(
            f"Panjang ciphertext ({len(clean_c)}) harus tepat sama dengan kapasitas stensil ({total_cells} sel)."
        )

    # Inisialisasi dan isi matriks grid dari ciphertext (row-by-row)
    grid = []
    idx = 0
    for r in range(n):
        row = []
        for c in range(n):
            row.append(clean_c[idx])
            idx += 1
        grid.append(row)

    if verbose:
        print_step_header(1, "Pemetaan Ciphertext ke Grid 4x4", 
                          "Menyusun ciphertext mendatar untuk siap ditutup stensil berputar")
        col_headers = [f"K{c}" for c in range(n)]
        row_labels = [f"B{r}" for r in range(n)]
        print(render_matrix(grid, col_headers=col_headers, row_labels=row_labels, color_code=EMERALD))

    current_holes = initial_holes
    rot_angles = ["0°", "90° CW", "180° CW", "270° CW"]
    recovered_parts = []

    if verbose:
        print_step_header(2, "Pembacaan Huruf Melalui Lubang Stensil 4 Putaran", 
                          "Mengintip karakter yang muncul di balik jendela lubang stensil")

    for rot_idx in range(4):
        letters = [grid[r][c] for r, c in current_holes]
        chunk = "".join(letters)
        recovered_parts.append(chunk)

        if verbose:
            angle = rot_angles[rot_idx]
            print(f"  Rotasi #{rot_idx+1} ({angle}) terbaca kata : {BOLD}{AMBER}{chunk}{RESET}")

        current_holes = rotate_coords_90_cw(current_holes, n)

    plaintext = "".join(recovered_parts)

    if verbose:
        print(f"\n  {EMERALD}{BOLD}HASIL DEKRIPSI TURNING GRILLE :{RESET} {BOLD}{plaintext}{RESET} ✓\n")

    return plaintext, grid


# =============================================================================
# BLOK TESTING MANDIRI
# =============================================================================
if __name__ == "__main__":
    print(f"\n{BOLD}{PURPLE}=== DEMO MODUL TURNING GRILLE CIPHER (KELOMPOK 2) ==={RESET}")
    sampel_pt = "SENDTROOPSASAPXX"
    
    ct, _ = turning_grille_encrypt(sampel_pt, verbose=True)
    pt, _ = turning_grille_decrypt(ct, verbose=True)
    
    assert pt == sampel_pt, f"Gagal: diperoleh {pt}"
    print(f"{EMERALD}{BOLD}UJI VALIDASI TURNING GRILLE 100% SUKSES TEPAT DENGAN SLIDE 24-29!{RESET}\n")
