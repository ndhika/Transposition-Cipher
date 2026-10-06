"""
=============================================================================
MODUL           : route_cipher.py
VARIAN          : 3 — Route Cipher (Lintasan Spiral Geometris)
TOPIK           : Kriptografi Klasik — Transposition Cipher
KELOMPOK        : 2 (Transposition Cipher)
=============================================================================
Dokumentasi Batch:
Route Cipher memetakan plaintext ke dalam grid dua dimensi (R baris x C kolom),
kemudian mengekstraksi karakter mengikuti lintasan geometris tertentu yang disepakati
sebagai kunci rahasia. Modul ini mendukung dua arah putaran spiral:
1. Clockwise Inward Spiral (Searah Jarum Jam — CW):
   Mulai dari sel (0,0) bergerak ke KANAN, BAWAH, KIRI, ATAS menuju pusat.
2. Counter-Clockwise Inward Spiral (Berlawanan Arah Jarum Jam — CCW):
   Mulai dari sel (0,0) bergerak ke BAWAH, KANAN, ATAS, KIRI menuju pusat.
=============================================================================
"""

from typing import Tuple, List
from utils import clean_text, pad_text, render_matrix, print_step_header, CYAN, EMERALD, PURPLE, AMBER, BOLD, RESET


# =============================================================================
# FUNGSI 1: generate_spiral_coords
# =============================================================================
def generate_spiral_coords(rows: int, cols: int, direction: str = 'cw') -> List[Tuple[int, int]]:
    """
    =============================================================================
    FUNGSI / METODE : generate_spiral_coords
    KATEGORI        : Geometri Komputasi / Pembuat Jalur Lintasan Spiral
    DASAR TEORI     : Menghasilkan urutan koordinat sel (r, c) yang membentuk lintasan
                      spiral dari terluar menuju terdalam secara siklis dengan 4 batas:
                      top, bottom, left, right. Mendukung arah searah jarum jam (CW)
                      maupun berlawanan arah jarum jam (CCW).
    -----------------------------------------------------------------------------
    ALGORITMA (ARAH SEARAH JARUM JAM / CW):
        1. Telusuri batas Atas  : (top, c) untuk c dari left ke right. Lalu top++
        2. Telusuri batas Kanan : (r, right) untuk r dari top ke bottom. Lalu right--
        3. Telusuri batas Bawah : (bottom, c) untuk c dari right ke left. Lalu bottom--
        4. Telusuri batas Kiri  : (r, left) untuk r dari bottom ke top. Lalu left++

    ALGORITMA (ARAH BERLAWANAN JARUM JAM / CCW):
        1. Telusuri batas Kiri  : (r, left) untuk r dari top ke bottom. Lalu left++
        2. Telusuri batas Bawah : (bottom, c) untuk c dari left ke right. Lalu bottom--
        3. Telusuri batas Kanan : (r, right) untuk r dari bottom ke top. Lalu right--
        4. Telusuri batas Atas  : (top, c) untuk c dari right ke left. Lalu top++
    
    PARAMETER:
        - rows (int): Jumlah baris grid matriks (R >= 2).
        - cols (int): Jumlah kolom grid matriks (C >= 2).
        - direction (str, opsional): Arah putaran ('cw' = searah jarum jam, 
                                     'ccw' = berlawanan arah jarum jam). Default 'cw'.
    
    OUTPUT / RETURN:
        - List[Tuple[int, int]]: Daftar koordinat (baris, kolom) urutan spiral.
    =============================================================================
    """
    dir_clean = direction.strip().lower()
    top = 0
    bottom = rows - 1
    left = 0
    right = cols - 1
    
    coords = []
    total = rows * cols
    
    if dir_clean in ('ccw', 'counter-clockwise', 'berlawanan', 'counter'):
        # Arah Berlawanan Arah Jarum Jam (Counter-Clockwise)
        while len(coords) < total:
            # 1. Turun ke Bawah di batas Kiri
            if left <= right:
                for r in range(top, bottom + 1):
                    coords.append((r, left))
                    if len(coords) == total:
                        break
                left += 1
                
            # 2. Geser ke Kanan di batas Bawah
            if top <= bottom:
                for c in range(left, right + 1):
                    coords.append((bottom, c))
                    if len(coords) == total:
                        break
                bottom -= 1
                
            # 3. Naik ke Atas di batas Kanan
            if left <= right:
                for r in range(bottom, top - 1, -1):
                    coords.append((r, right))
                    if len(coords) == total:
                        break
                right -= 1
                
            # 4. Geser ke Kiri di batas Atas
            if top <= bottom:
                for c in range(right, left - 1, -1):
                    coords.append((top, c))
                    if len(coords) == total:
                        break
                top += 1
    else:
        # Arah Searah Jarum Jam (Clockwise - Default)
        while len(coords) < total:
            # 1. Kiri ke Kanan pada batas Atas
            if top <= bottom:
                for c in range(left, right + 1):
                    coords.append((top, c))
                    if len(coords) == total:
                        break
                top += 1
            
            # 2. Atas ke Bawah pada batas Kanan
            if left <= right:
                for r in range(top, bottom + 1):
                    coords.append((r, right))
                    if len(coords) == total:
                        break
                right -= 1
            
            # 3. Kanan ke Kiri pada batas Bawah
            if top <= bottom:
                for c in range(right, left - 1, -1):
                    coords.append((bottom, c))
                    if len(coords) == total:
                        break
                bottom -= 1
                
            # 4. Bawah ke Atas pada batas Kiri
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
def route_cipher_encrypt(
    plaintext: str, 
    rows: int = 4, 
    cols: int = 4, 
    direction: str = 'cw', 
    verbose: bool = False
) -> Tuple[str, List[List[str]]]:
    """
    =============================================================================
    FUNGSI / METODE : route_cipher_encrypt
    KATEGORI        : Algoritma Enkripsi Transposisi Geometri Rute
    DASAR TEORI     : Plaintext diplot ke grid R x C baris demi baris dari kiri
                      ke kanan. Ciphertext diekstraksi dengan menelusuri koordinat
                      spiral (Searah Jarum Jam 'cw' atau Berlawanan 'ccw') dari sel (0, 0).
    -----------------------------------------------------------------------------
    PARAMETER:
        - plaintext (str): Pesan asli yang akan dienkripsi.
        - rows (int): Jumlah baris grid. Default 4.
        - cols (int): Jumlah kolom grid. Default 4.
        - direction (str, opsional): Arah putaran spiral ('cw' atau 'ccw'). Default 'cw'.
        - verbose (bool, opsional): Jika True, menampilkan visualisasi matriks rute.
    
    OUTPUT / RETURN:
        - Tuple[str, List[List[str]]]:
            1. Ciphertext hasil ekstraksi spiral.
            2. Matriks 2D data teks (R x C).
    
    KOMPLEKSITAS:
        - Waktu : O(R * C)
        - Ruang : O(R * C)
        
    CONTOH PENGGUNAAN:
        >>> ct, _ = route_cipher_encrypt("SERANGANDIBAWAH", 4, 4, direction='cw')
        >>> ct
        'SERANAXHAWDNGABI'
    =============================================================================
    """
    clean_p = clean_text(plaintext)
    total_cells = rows * cols
    
    # Padding dengan karakter dummy 'X'
    padded_p, pad_count = pad_text(clean_p, total_cells, 'X')
    
    is_ccw = direction.strip().lower() in ('ccw', 'counter-clockwise', 'berlawanan', 'counter')
    dir_label = "Berlawanan Arah Jarum Jam (Counter-Clockwise / CCW)" if is_ccw else "Searah Jarum Jam (Clockwise / CW)"
    
    if verbose:
        print_step_header(1, "Pengisian Grid Matriks Mendatar (Row-by-Row)", 
                          f"Dimensi {rows}x{cols} ({total_cells} sel) | Arah: {dir_label}")
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

    # Susun koordinat lintasan spiral dan ambil karakter per sel
    spiral_coords = generate_spiral_coords(rows, cols, direction=direction)
    ciphertext_chars = [matrix[r][c] for r, c in spiral_coords]
    ciphertext = "".join(ciphertext_chars)

    if verbose:
        print_step_header(2, f"Penelusuran Rute Spiral: {dir_label}", 
                          "Menelusuri dari tepi luar (0,0) melingkar masuk ke pusat matriks")
        
        # Buat matriks penomoran urutan langkah
        step_grid = [[0] * cols for _ in range(rows)]
        for step_idx, (r, c) in enumerate(spiral_coords):
            step_grid[r][c] = step_idx + 1
        
        print(f"  Peta Urutan Penelusuran Langkah 1 s.d. {total_cells}:")
        print(render_matrix(step_grid, col_headers=col_headers, row_labels=row_labels, color_code=PURPLE))
        
        print(f"\n  {EMERALD}{BOLD}HASIL CIPHERTEXT ROUTE CIPHER ({direction.upper()}) :{RESET} {BOLD}{ciphertext}{RESET}\n")

    return ciphertext, matrix


# =============================================================================
# FUNGSI 3: route_cipher_decrypt
# =============================================================================
def route_cipher_decrypt(
    ciphertext: str, 
    rows: int = 4, 
    cols: int = 4, 
    direction: str = 'cw', 
    verbose: bool = False
) -> Tuple[str, List[List[str]]]:
    """
    =============================================================================
    FUNGSI / METODE : route_cipher_decrypt
    KATEGORI        : Algoritma Dekripsi Transposisi Geometri Rute
    DASAR TEORI     : Membalik proses enkripsi dengan memasukkan ciphertext ke dalam
                      grid R x C mengikuti lintasan spiral yang sama persis (CW atau CCW),
                      lalu membaca pesan asli secara normal baris demi baris (kiri ke kanan).
    -----------------------------------------------------------------------------
    PARAMETER:
        - ciphertext (str): Teks terenkripsi.
        - rows (int): Jumlah baris grid. Default 4.
        - cols (int): Jumlah kolom grid. Default 4.
        - direction (str, opsional): Arah putaran spiral yang digunakan saat enkripsi.
        - verbose (bool, opsional): Jika True, menampilkan visualisasi pemulihan.
    
    OUTPUT / RETURN:
        - Tuple[str, List[List[str]]]:
            1. Plaintext hasil pemulihan.
            2. Matriks 2D hasil rekonstruksi.
    =============================================================================
    """
    clean_c = clean_text(ciphertext)
    total_cells = rows * cols
    
    if len(clean_c) != total_cells:
        raise ValueError(
            f"Panjang ciphertext ({len(clean_c)}) harus tepat sama dengan kapasitas "
            f"grid {rows}x{cols} = {total_cells} sel."
        )

    is_ccw = direction.strip().lower() in ('ccw', 'counter-clockwise', 'berlawanan', 'counter')
    dir_label = "Berlawanan Arah Jarum Jam (Counter-Clockwise / CCW)" if is_ccw else "Searah Jarum Jam (Clockwise / CW)"

    spiral_coords = generate_spiral_coords(rows, cols, direction=direction)

    # Inisialisasi matriks kosong
    matrix = [[''] * cols for _ in range(rows)]

    # Injeksi karakter ciphertext ke posisi spiral
    for char_idx, (r, c) in enumerate(spiral_coords):
        matrix[r][c] = clean_c[char_idx]

    if verbose:
        print_step_header(1, f"Injeksi Ciphertext ke Jalur Spiral {dir_label} Grid {rows}x{cols}", 
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
                          f"Membaca normal dari Baris 0 s.d. Baris {rows-1} secara horizontal (→)")
        for r_idx, s in enumerate(row_strings):
            print(f"  Baris {r_idx} (→) : {BOLD}{CYAN}{s}{RESET}")
        print(f"\n  {EMERALD}{BOLD}HASIL DEKRIPSI ROUTE CIPHER ({direction.upper()}) :{RESET} {BOLD}{plaintext}{RESET} ✓\n")

    return plaintext, matrix


# =============================================================================
# BLOK TESTING MANDIRI
# =============================================================================
if __name__ == "__main__":
    print(f"\n{BOLD}{PURPLE}=== DEMO MODUL ROUTE CIPHER: CW & CCW (KELOMPOK 2) ==={RESET}")
    sampel_pt = "SERANGANDIBAWAH"
    
    # 1. Uji Clockwise (CW - Standar Slide Presentasi)
    print(f"\n{BOLD}{CYAN}>>> 1. UJI CLOCKWISE (SEARAH JARUM JAM) <<<{RESET}")
    ct_cw, _ = route_cipher_encrypt(sampel_pt, 4, 4, direction='cw', verbose=True)
    pt_cw, _ = route_cipher_decrypt(ct_cw, 4, 4, direction='cw', verbose=True)
    assert pt_cw == "SERANGANDIBAWAHX", f"Gagal CW: diperoleh {pt_cw}"
    assert ct_cw == "SERANAXHAWDNGABI", f"Gagal mencocokkan slide CW: {ct_cw}"
    print(f"{EMERALD}{BOLD}UJI ROUTE CIPHER CLOCKWISE (CW) 100% SUKSES!{RESET}\n")

    # 2. Uji Counter-Clockwise (CCW - Berlawanan Arah Jarum Jam)
    print(f"\n{BOLD}{CYAN}>>> 2. UJI COUNTER-CLOCKWISE (BERLAWANAN ARAH JARUM JAM) <<<{RESET}")
    ct_ccw, _ = route_cipher_encrypt(sampel_pt, 4, 4, direction='ccw', verbose=True)
    pt_ccw, _ = route_cipher_decrypt(ct_ccw, 4, 4, direction='ccw', verbose=True)
    assert pt_ccw == "SERANGANDIBAWAHX", f"Gagal CCW: diperoleh {pt_ccw}"
    print(f"  Ciphertext CCW: {BOLD}{AMBER}{ct_ccw}{RESET}")
    print(f"{EMERALD}{BOLD}UJI ROUTE CIPHER COUNTER-CLOCKWISE (CCW) 100% SUKSES!{RESET}\n")
