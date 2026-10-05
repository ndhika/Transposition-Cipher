"""
=============================================================================
MODUL           : route_cipher.py
VARIAN          : 3 — Route Cipher (Lintasan Spiral Searah Jarum Jam)
TOPIK           : Kriptografi Klasik — Transposition Cipher
KELOMPOK        : 2 (Transposition Cipher)
=============================================================================
Dokumentasi Batch:
Route Cipher memetakan plaintext ke dalam grid dua dimensi (R baris x C kolom),
kemudian mengekstraksi karakter mengikuti lintasan geometris tertentu yang disepakati
sebagai kunci rahasia. Pada varian standar modern ini, lintasan yang digunakan
adalah Spiral Melingkar Masuk Searah Jarum Jam (Clockwise Inward Spiral) mulai
dari pojok kiri atas (0, 0) menuju pusat matriks.
=============================================================================
"""

from typing import Tuple, List
from utils import clean_text, pad_text, render_matrix, print_step_header, CYAN, EMERALD, PURPLE, AMBER, BOLD, RESET


# =============================================================================
# FUNGSI 1: generate_spiral_coords
# =============================================================================
def generate_spiral_coords(rows: int, cols: int) -> List[Tuple[int, int]]:
    """
    =============================================================================
    FUNGSI / METODE : generate_spiral_coords
    KATEGORI        : Geometri Komputasi / Pembangkit Jalur Lintasan
    DASAR TEORI     : Menghasilkan urutan koordinat sel (r, c) yang membentuk lintasan
                      spiral dari terluar menuju terdalam secara siklis dengan 4 batas:
                      top, bottom, left, right.
    -----------------------------------------------------------------------------
    ALGORITMA (4 ARAH SIKLIS):
        1. Telusuri batas Atas  : (top, c) untuk c dari left ke right. Lalu top++
        2. Telusuri batas Kanan : (r, right) untuk r dari top ke bottom. Lalu right--
        3. Telusuri batas Bawah : (bottom, c) untuk c dari right ke left. Lalu bottom--
        4. Telusuri batas Kiri  : (r, left) untuk r dari bottom ke top. Lalu left++
        Ulangi hingga seluruh R * C koordinat terisi.
    
    PARAMETER:
        - rows (int): Jumlah baris grid matriks (R >= 2).
        - cols (int): Jumlah kolom grid matriks (C >= 2).
    
    OUTPUT / RETURN:
        - List[Tuple[int, int]]: Daftar koordinat (baris, kolom) urutan spiral.
    =============================================================================
    """
    top = 0
    bottom = rows - 1
    left = 0
    right = cols - 1
    
    coords = []
    total = rows * cols
    
    while len(coords) < total:
        # Arah 1: Kiri ke Kanan pada batas Atas
        for c in range(left, right + 1):
            coords.append((top, c))
            if len(coords) == total:
                break
        top += 1
        
        # Arah 2: Atas ke Bawah pada batas Kanan
        for r in range(top, bottom + 1):
            coords.append((r, right))
            if len(coords) == total:
                break
        right -= 1
        
        # Arah 3: Kanan ke Kiri pada batas Bawah
        if top <= bottom:
            for c in range(right, left - 1, -1):
                coords.append((bottom, c))
                if len(coords) == total:
                    break
            bottom -= 1
            
        # Arah 4: Bawah ke Atas pada batas Kiri
        if left <= right:
            for r in range(bottom, top - 1, -1):
                coords.append((r, left))
                if len(coords) == total:
                    break
            left += 1
            
    return coords


# =============================================================================
# FUNGSI 2: route_cipher_encrypt
# =============================================================================
def route_cipher_encrypt(plaintext: str, rows: int = 4, cols: int = 4, verbose: bool = False) -> Tuple[str, List[List[str]]]:
    """
    =============================================================================
    FUNGSI / METODE : route_cipher_encrypt
    KATEGORI        : Algoritma Enkripsi Transposisi Geometri Rute
    DASAR TEORI     : Plaintext diplot ke grid R x C baris demi baris dari kiri
                      ke kanan. Ciphertext diekstraksi dengan menelusuri koordinat
                      spiral searah jarum jam dari sel (0, 0).
    -----------------------------------------------------------------------------
    PARAMETER:
        - plaintext (str): Pesan asli yang akan dienkripsi.
        - rows (int): Jumlah baris grid. Default bernilai 4.
        - cols (int): Jumlah kolom grid. Default bernilai 4.
        - verbose (bool, opsional): Jika True, menampilkan visualisasi matriks rute.
    
    OUTPUT / RETURN:
        - Tuple[str, List[List[str]]]:
            1. Ciphertext hasil ekstraksi spiral.
            2. Matriks 2D data teks (R x C).
    
    KOMPLEKSITAS:
        - Waktu : O(R * C)
        - Ruang : O(R * C)
        
    CONTOH PENGGUNAAN:
        >>> ct, _ = route_cipher_encrypt("SERANGANDIBAWAH", 4, 4)
        >>> ct
        'SERANAXHAWDNGABI'
    =============================================================================
    """
    clean_p = clean_text(plaintext)
    total_cells = rows * cols
    
    # Padding dengan karakter dummy 'X'
    padded_p, pad_count = pad_text(clean_p, total_cells, 'X')
    
    if verbose:
        print_step_header(1, "Pengisian Grid Matriks Mendatar (Row-by-Row)", 
                          f"Dimensi {rows}x{cols} ({total_cells} sel) | Panjang Teks = {len(clean_p)}")
        print(f"  Plaintext Bersih : {BOLD}{clean_p}{RESET}")
        if pad_count > 0:
            print(f"  Padding Dummy    : Ditambahkan {pad_count} huruf 'X' -> {padded_p}")

    # Plot ke matriks baris per baris
    matrix = []
    idx = 0
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(padded_p[idx])
            idx += 1
        matrix.append(row)

    if verbose:
        col_headers = [f"K{c}" for c in range(cols)]
        row_labels = [f"B{r}" for r in range(rows)]
        print(render_matrix(matrix, col_headers=col_headers, row_labels=row_labels, color_code=CYAN))

    # Bangkitkan koordinat spiral dan ambil karakter
    spiral_coords = generate_spiral_coords(rows, cols)
    ciphertext_chars = [matrix[r][c] for r, c in spiral_coords]
    ciphertext = "".join(ciphertext_chars)

    if verbose:
        print_step_header(2, "Penelusuran Rute Spiral Searah Jarum Jam (Clockwise)", 
                          "Menelusuri dari tepi luar (0,0) memutar ke dalam")
        
        # Buat matriks penomoran urutan langkah
        step_grid = [[0] * cols for _ in range(rows)]
        for step_idx, (r, c) in enumerate(spiral_coords):
            step_grid[r][c] = step_idx + 1
        
        print(f"  Peta Urutan Penelusuran Langkah 1 s.d. {total_cells}:")
        print(render_matrix(step_grid, col_headers=col_headers, row_labels=row_labels, color_code=PURPLE))
        
        print(f"\n  {EMERALD}{BOLD}HASIL CIPHERTEXT ROUTE CIPHER :{RESET} {BOLD}{ciphertext}{RESET}\n")

    return ciphertext, matrix


# =============================================================================
# FUNGSI 3: route_cipher_decrypt
# =============================================================================
def route_cipher_decrypt(ciphertext: str, rows: int = 4, cols: int = 4, verbose: bool = False) -> Tuple[str, List[List[str]]]:
    """
    =============================================================================
    FUNGSI / METODE : route_cipher_decrypt
    KATEGORI        : Algoritma Dekripsi Transposisi Geometri Rute
    DASAR TEORI     : Membalik proses enkripsi dengan memasukkan ciphertext ke dalam
                      grid R x C mengikuti lintasan spiral yang sama persis, lalu
                      membaca pesan asli secara normal baris demi baris (kiri ke kanan).
    -----------------------------------------------------------------------------
    PARAMETER:
        - ciphertext (str): Teks terenkripsi.
        - rows (int): Jumlah baris grid. Default bernilai 4.
        - cols (int): Jumlah kolom grid. Default bernilai 4.
        - verbose (bool, opsional): Jika True, menampilkan visualisasi pemulihan.
    
    OUTPUT / RETURN:
        - Tuple[str, List[List[str]]]:
            1. Plaintext hasil pemulihan.
            2. Matriks 2D hasil rekonstruksi.
    
    KOMPLEKSITAS:
        - Waktu : O(R * C)
        - Ruang : O(R * C)
        
    CONTOH PENGGUNAAN:
        >>> pt, _ = route_cipher_decrypt("SERANAXHAWDNGABI", 4, 4)
        >>> pt
        'SERANGANDIBAWAHX'
    =============================================================================
    """
    clean_c = clean_text(ciphertext)
    total_cells = rows * cols
    
    if len(clean_c) != total_cells:
        raise ValueError(
            f"Panjang ciphertext ({len(clean_c)}) harus tepat sama dengan kapasitas "
            f"grid {rows}x{cols} = {total_cells} sel."
        )

    spiral_coords = generate_spiral_coords(rows, cols)

    # Inisialisasi matriks kosong
    matrix = [[''] * cols for _ in range(rows)]

    # Injeksi karakter ciphertext ke posisi spiral
    for char_idx, (r, c) in enumerate(spiral_coords):
        matrix[r][c] = clean_c[char_idx]

    if verbose:
        print_step_header(1, f"Injeksi Ciphertext ke Jalur Spiral Grid {rows}x{cols}", 
                          "Memasukkan karakter sandi mengikuti rute melingkar ke dalam")
        col_headers = [f"K{c}" for c in range(cols)]
        row_labels = [f"B{r}" for r in range(rows)]
        print(render_matrix(matrix, col_headers=col_headers, row_labels=row_labels, color_code=EMERALD))

    # Ekstraksi baris demi baris (horizontal kiri ke kanan)
    plaintext_chars = []
    row_strings = []
    for r in range(rows):
        s = "".join(matrix[r])
        row_strings.append(s)
        plaintext_chars.append(s)

    plaintext = "".join(plaintext_chars)

    if verbose:
        print_step_header(2, "Pembacaan Grid Baris per Baris (Plaintext Berhasil Pulih)", 
                          "Membaca normal dari Baris 0 s.d. Baris 3 secara horizontal (→)")
        for r_idx, s in enumerate(row_strings):
            print(f"  Baris {r_idx} (→) : {BOLD}{CYAN}{s}{RESET}")
        print(f"\n  {EMERALD}{BOLD}HASIL DEKRIPSI ROUTE CIPHER :{RESET} {BOLD}{plaintext}{RESET} ✓\n")

    return plaintext, matrix


# =============================================================================
# BLOK TESTING MANDIRI
# =============================================================================
if __name__ == "__main__":
    print(f"\n{BOLD}{PURPLE}=== DEMO MODUL ROUTE CIPHER (KELOMPOK 2) ==={RESET}")
    sampel_pt = "SERANGANDIBAWAH"
    
    ct, _ = route_cipher_encrypt(sampel_pt, 4, 4, verbose=True)
    pt, _ = route_cipher_decrypt(ct, 4, 4, verbose=True)
    
    assert pt == "SERANGANDIBAWAHX", f"Gagal: diperoleh {pt}"
    print(f"{EMERALD}{BOLD}UJI VALIDASI ROUTE CIPHER 100% SUKSES TEPAT DENGAN SLIDE 14-18!{RESET}\n")
