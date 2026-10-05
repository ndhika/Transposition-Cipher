"""
=============================================================================
MODUL           : advanced.py
DESKRIPSI       : Analisis Kriptografi Lanjutan & Kaitan Modern
MATA KULIAH     : Kriptografi Klasik — Teknik Informatika UDINUS
KELOMPOK        : 2 (Transposition Cipher)
=============================================================================
Dokumentasi Batch:
Modul ini mengimplementasikan konsep teoritis dan matematis mendalam yang
diajarkan pada Slide 30-38 materi kuliah:
1. Pemodelan Aljabar Linier Matriks Permutasi Ortogonal (P_sigma * P_sigma^T = I).
2. Kriptanalisis Kuantitatif: Index of Coincidence (IoC) William F. Friedman.
3. Double Transposition (Transposisi Ganda) — Kriptografi Perang Dunia II.
4. Relevansi Kriptografi Modern: Transformasi ShiftRows AES & Permutation Box DES.
=============================================================================
"""

import math
from typing import List, Tuple, Dict
from utils import clean_text, render_matrix, print_step_header, CYAN, EMERALD, PURPLE, AMBER, BOLD, RESET


# =============================================================================
# BAGIAN 1: ALJABAR LINIER MATRIKS PERMUTASI ORTOGONAL
# =============================================================================

def create_permutation_matrix(permutation_order: List[int]) -> List[List[int]]:
    """
    =============================================================================
    FUNGSI / METODE : create_permutation_matrix
    KATEGORI        : Aljabar Linier Kriptografi
    DASAR TEORI     : Memetakan permutasi spasial sigma ke dalam matriks biner
                      berukuran n x n, di mana P[i][j] = 1 jika dan hanya jika
                      posisi ke-i memetakan ke elemen ke-j dari vektor input.
    -----------------------------------------------------------------------------
    FORMULA MATEMATIKA:
        P_sigma in {0, 1}^(n x n)
        P[i][sigma(i)] = 1, sel lain = 0
    
    PARAMETER:
        - permutation_order (List[int]): Array pemetaan indeks target (0 s.d. n-1).
    
    OUTPUT / RETURN:
        - List[List[int]]: Matriks bujursangkar biner (n x n).
    =============================================================================
    """
    n = len(permutation_order)
    matrix = [[0] * n for _ in range(n)]
    for row_idx, target_col in enumerate(permutation_order):
        matrix[row_idx][target_col] = 1
    return matrix


def transpose_matrix(matrix: List[List[int]]) -> List[List[int]]:
    """
    =============================================================================
    FUNGSI / METODE : transpose_matrix
    KATEGORI        : Operasi Matriks / Dekripsi Ortogonal
    DASAR TEORI     : Mengingat matriks permutasi bersifat ortogonal (P * P^T = I),
                      maka proses dekripsi tidak memerlukan invers matriks Gauss-Jordan
                      yang rumit, melainkan cukup melakukan operasi transposisi:
                      (P_sigma)^(-1) = (P_sigma)^T.
    -----------------------------------------------------------------------------
    FORMULA MATEMATIKA:
        (P^T)[r][c] = P[c][r]
    =============================================================================
    """
    rows = len(matrix)
    cols = len(matrix[0])
    return [[matrix[r][c] for r in range(rows)] for c in range(cols)]


def apply_permutation(matrix_p: List[List[int]], vector_v: List[str]) -> List[str]:
    """
    =============================================================================
    FUNGSI / METODE : apply_permutation
    KATEGORI        : Perkalian Matriks-Vektor Kriptografi
    DASAR TEORI     : Mengalikan matriks permutasi P_sigma dengan vektor kolom
                      karakter teks: y = P_sigma * x.
    -----------------------------------------------------------------------------
    PARAMETER:
        - matrix_p (List[List[int]]): Matriks permutasi (n x n).
        - vector_v (List[str]): Vektor karakter teks sepanjang n.
    
    OUTPUT / RETURN:
        - List[str]: Vektor karakter baru hasil permutasi linear.
    =============================================================================
    """
    n = len(vector_v)
    result = []
    for r in range(n):
        for c in range(n):
            if matrix_p[r][c] == 1:
                result.append(vector_v[c])
                break
    return result


# =============================================================================
# BAGIAN 2: KRIPTANALISIS INDEX OF COINCIDENCE (IoC)
# =============================================================================

def calculate_letter_frequencies(text: str) -> Dict[str, int]:
    """
    =============================================================================
    FUNGSI / METODE : calculate_letter_frequencies
    KATEGORI        : Statistik Frekuensi Karakter
    DASAR TEORI     : Menghitung kemunculan tiap huruf A-Z pada teks masukan.
    =============================================================================
    """
    clean_t = clean_text(text)
    freq: Dict[str, int] = {chr(c): 0 for c in range(ord('A'), ord('Z') + 1)}
    for char in clean_t:
        freq[char] += 1
    return freq


def calculate_index_of_coincidence(text: str) -> float:
    """
    =============================================================================
    FUNGSI / METODE : calculate_index_of_coincidence
    KATEGORI        : Kriptanalisis Kuantitatif
    DASAR TEORI     : Diperkenalkan oleh William F. Friedman (1922). Menghitung
                      probabilitas bahwa dua huruf yang dipilih secara acak dari
                      teks memiliki karakter yang sama.
                      
                      Sifat Kritis Transposisi:
                      Karena cipher transposisi HANYA menukar posisi spasial tanpa
                      mengubah simbol karakter, maka nilai IC ciphertext transposisi
                      PERSIS SAMA dengan IC plaintext aslinya (~0.065 s.d. 0.068)!
                      Hal ini membedakannya dari cipher substitusi polialfabetik
                      seperti Vigenere yang menurunkan IC ke angka ~0.038.
    -----------------------------------------------------------------------------
    FORMULA MATEMATIKA:
        IC = sum(f_i * (f_i - 1)) / (N * (N - 1))
        untuk i in [A s.d. Z], di mana N = total panjang teks.
    
    PARAMETER:
        - text (str): Teks yang akan dianalisis.
    
    OUTPUT / RETURN:
        - float: Nilai Index of Coincidence (rentang 0.0 s.d. 1.0).
    =============================================================================
    """
    clean_t = clean_text(text)
    n = len(clean_t)
    if n <= 1:
        return 0.0

    freqs = calculate_letter_frequencies(clean_t)
    numerator = sum(f * (f - 1) for f in freqs.values())
    denominator = n * (n - 1)

    return numerator / denominator


def diagnose_ciphertext_type(text: str) -> Tuple[float, str]:
    """
    =============================================================================
    FUNGSI / METODE : diagnose_ciphertext_type
    KATEGORI        : Diagnostik Otomatis Jenis Sandi
    DASAR TEORI     : Menguji apakah suatu ciphertext merupakan hasil transposisi
                      atau substitusi polialfabetik berdasarkan ambang batas IC.
    =============================================================================
    """
    ic = calculate_index_of_coincidence(text)
    if ic >= 0.055:
        diagnosis = (
            f"KEMUNGKINAN BESAR CIPHER TRANSPOSISI (IC = {ic:.4f} mendekati bahasa alami ~0.068). "
            f"Distribusi frekuensi huruf utuh dipertahankan!"
        )
    else:
        diagnosis = (
            f"KEMUNGKINAN BESAR CIPHER SUBSTITUSI POLIALFABETIK / ACAK (IC = {ic:.4f} mendekati flat ~0.038)."
        )
    return ic, diagnosis


# =============================================================================
# BAGIAN 3: DOUBLE TRANSPOSITION (TRANSPOSISI GANDA - PERANG DUNIA II)
# =============================================================================

def double_transposition_encrypt(
    plaintext: str, key1: str, key2: str, verbose: bool = False
) -> str:
    """
    =============================================================================
    FUNGSI / METODE : double_transposition_encrypt
    KATEGORI        : Enkripsi Transposisi Berlapis (Perang Dunia II)
    DASAR TEORI     : Double Transposition menerapkan cipher columnar transposisi
                      DUA KALI berturut-turut dengan kunci yang berbeda. Teknik ini
                      digunakan oleh agen Sekutu dalam PD II karena jauh lebih sulit
                      dipecahkan secara kriptanalisis dibanding transposisi tunggal.
                      Putaran pertama mengacak posisi, putaran kedua mengacak hasil
                      pengacakan pertama sehingga pola frekuensi posisi semakin sulit
                      dideteksi.
    -----------------------------------------------------------------------------
    PARAMETER:
        - plaintext (str): Pesan asli.
        - key1 (str): Kunci putaran pertama.
        - key2 (str): Kunci putaran kedua (berbeda dari key1 untuk keamanan maksimal).
        - verbose (bool): Jika True, tampilkan proses tiap putaran.

    OUTPUT / RETURN:
        - str: Ciphertext hasil dua kali transposisi.

    CONTOH PENGGUNAAN:
        >>> ct = double_transposition_encrypt("ATTACKATDAWN", "KEY", "CODE")
    =============================================================================
    """
    from myszkowski import myszkowski_encrypt
    from rail_fence import rail_fence_encrypt

    clean_k1 = clean_text(key1)
    clean_k2 = clean_text(key2)
    if len(clean_k2) < 2:
        raise ValueError("Kunci kedua harus minimal 2 karakter (digunakan sebagai jumlah rel Rail Fence).")

    # Putaran 1: Myszkowski (keyword columnar)
    if verbose:
        print(f"\n  {BOLD}{PURPLE}=== DOUBLE TRANSPOSITION — PUTARAN 1 (Myszkowski) ==={RESET}")
        print(f"  Kunci Putaran 1 : {BOLD}{clean_k1}{RESET}")

    ct1, _ = myszkowski_encrypt(plaintext, clean_k1, verbose=verbose)

    # Putaran 2: Rail Fence (kunci = panjang kunci kedua sebagai jumlah rel)
    num_rails = len(clean_k2)
    if verbose:
        print(f"\n  {BOLD}{PURPLE}=== DOUBLE TRANSPOSITION — PUTARAN 2 (Rail Fence n={num_rails}) ==={RESET}")
        print(f"  Kunci Putaran 2 : {BOLD}{clean_k2}{RESET} (panjang={num_rails} rel)")
        print(f"  Input Putaran 2 : {BOLD}{ct1}{RESET}")

    ct2, _ = rail_fence_encrypt(ct1, num_rails, verbose=verbose)

    if verbose:
        print(f"\n  {BOLD}{EMERALD}HASIL AKHIR DOUBLE TRANSPOSITION :{RESET} {BOLD}{ct2}{RESET}\n")

    return ct2


def double_transposition_decrypt(
    ciphertext: str, key1: str, key2: str, verbose: bool = False
) -> str:
    """
    =============================================================================
    FUNGSI / METODE : double_transposition_decrypt
    KATEGORI        : Dekripsi Transposisi Berlapis
    DASAR TEORI     : Pemulihan dilakukan dengan membalik urutan kunci:
                      pertama dekripsi menggunakan key2 (membalik putaran 2),
                      lalu dekripsi menggunakan key1 (membalik putaran 1).
    -----------------------------------------------------------------------------
    PARAMETER:
        - ciphertext (str): Teks terenkripsi ganda.
        - key1 (str): Kunci putaran pertama (sama dengan saat enkripsi).
        - key2 (str): Kunci putaran kedua (sama dengan saat enkripsi).
        - verbose (bool): Jika True, tampilkan proses tiap putaran.

    OUTPUT / RETURN:
        - str: Plaintext hasil pemulihan dua kali dekripsi.
    =============================================================================
    """
    from myszkowski import myszkowski_decrypt
    from rail_fence import rail_fence_decrypt

    clean_k1 = clean_text(key1)
    clean_k2 = clean_text(key2)
    num_rails = len(clean_k2)

    # Balik putaran 2 dulu: Rail Fence decrypt
    if verbose:
        print(f"\n  {BOLD}{PURPLE}=== DOUBLE TRANSPOSITION DEKRIPSI — PUTARAN 2 (Rail Fence n={num_rails}) ==={RESET}")
        print(f"  Kunci Putaran 2 (balik) : {BOLD}{clean_k2}{RESET} ({num_rails} rel)")

    mid, _ = rail_fence_decrypt(ciphertext, num_rails, verbose=verbose)

    # Balik putaran 1: Myszkowski decrypt
    if verbose:
        print(f"\n  {BOLD}{PURPLE}=== DOUBLE TRANSPOSITION DEKRIPSI — PUTARAN 1 (Myszkowski) ==={RESET}")
        print(f"  Kunci Putaran 1 : {BOLD}{clean_k1}{RESET}")

    plaintext, _ = myszkowski_decrypt(mid, clean_k1, verbose=verbose)

    if verbose:
        print(f"\n  {BOLD}{EMERALD}HASIL DEKRIPSI DOUBLE TRANSPOSITION :{RESET} {BOLD}{plaintext}{RESET} ✓\n")

    return plaintext


# =============================================================================
# BAGIAN 4: SIMULASI MODERN — AES SHIFTROWS & DES P-BOX
# =============================================================================

def aes_shift_rows(state_matrix: List[List[str]]) -> List[List[str]]:
    """
    =============================================================================
    FUNGSI / METODE : aes_shift_rows
    KATEGORI        : Kriptografi Modern / Standar AES (FIPS 197)
    DASAR TEORI     : Implementasi prinsip difusi Shannon modern. ShiftRows adalah
                      lapisan transposisi byte murni pada blok 4x4 state array:
                      - Baris 0: Tidak digeser (shift 0).
                      - Baris 1: Geser melingkar ke kiri sejauh 1 byte.
                      - Baris 2: Geser melingkar ke kiri sejauh 2 byte.
                      - Baris 3: Geser melingkar ke kiri sejauh 3 byte.
    -----------------------------------------------------------------------------
    FORMULA MATEMATIKA:
        S'[r][c] = S[r][(c + r) mod 4]
    =============================================================================
    """
    new_state = []
    for r in range(4):
        shift = r
        row = state_matrix[r]
        shifted_row = row[shift:] + row[:shift]
        new_state.append(shifted_row)
    return new_state


def aes_inv_shift_rows(state_matrix: List[List[str]]) -> List[List[str]]:
    """
    =============================================================================
    FUNGSI / METODE : aes_inv_shift_rows
    KATEGORI        : Dekripsi Modern AES / Invers ShiftRows
    DASAR TEORI     : Membalik rotasi byte ke arah kanan:
                      S[r][c] = S'[r][(c - r) mod 4].
    =============================================================================
    """
    new_state = []
    for r in range(4):
        shift = r
        row = state_matrix[r]
        # Geser melingkar ke kanan
        shifted_row = row[-shift:] + row[:-shift] if shift > 0 else list(row)
        new_state.append(shifted_row)
    return new_state


def des_pbox_permute(bits_32: str) -> str:
    """
    =============================================================================
    FUNGSI / METODE : des_pbox_permute
    KATEGORI        : Kriptografi Modern / Permutation Box DES (FIPS 46-3)
    DASAR TEORI     : Permutasi bit 32-bit tetap di dalam putaran fungsi Feistel DES
                      untuk menyebarkan (difusi) pengaruh bit output S-Box ke 4 blok
                      S-Box berbeda pada putaran berikutnya.
    =============================================================================
    """
    # Tabel P-Box standar FIPS DES (1-indexed dikonversi ke 0-indexed)
    DES_PBOX_TABLE = [
        15,  6, 19, 20, 28, 11, 27, 16,
         0, 14, 22, 25,  4, 17, 30,  9,
         1,  7, 23, 13, 31, 26,  2,  8,
        18, 12, 29,  5, 21, 10,  3, 24
    ]
    if len(bits_32) != 32:
        raise ValueError(f"Input bit DES P-Box harus tepat 32 bit, diterima: {len(bits_32)}")

    return "".join(bits_32[i] for i in DES_PBOX_TABLE)


# =============================================================================
# BLOK TESTING MANDIRI
# =============================================================================
if __name__ == "__main__":
    print(f"\n{BOLD}{PURPLE}=== DEMO ANALISIS LANJUTAN & RELEVANSI MODERN (KELOMPOK 2) ==={RESET}")
    
    # 1. Uji Matriks Permutasi Ortogonal
    print_step_header(1, "Aljabar Linier Matriks Permutasi (P * P^T = I)")
    vektor_awal = ['A', 'B', 'C', 'D']
    permutasi = [2, 0, 3, 1] # A->pos 1, B->pos 3, C->pos 0, D->pos 2
    P = create_permutation_matrix(permutasi)
    P_T = transpose_matrix(P)
    
    vektor_teracak = apply_permutation(P, vektor_awal)
    vektor_pulih = apply_permutation(P_T, vektor_teracak)
    
    print(f"  Vektor Asli    : {vektor_awal}")
    print(f"  Vektor Teracak : {vektor_teracak}")
    print(f"  Vektor Pulih   : {vektor_pulih}")
    assert vektor_pulih == vektor_awal, "Gagal rekonstruksi P^T"
    print(f"  {EMERALD}Validasi Ortogonalitas P * P^T Terbukti Sempurna!{RESET}")

    # 2. Uji Index of Coincidence
    print_step_header(2, "Kriptanalisis Index of Coincidence (IoC)")
    # Enkripsi menggunakan salah satu cipher transposisi (Rail Fence n=4)
    pt_sample = "KRIPTOGRAFIKLASIKADALAHFONDASIDARISISTEMKEAMANANMODERN"
    # Lakukan permutasi murni
    from rail_fence import rail_fence_encrypt
    ct_sample, _ = rail_fence_encrypt(pt_sample, 4)
    
    ic_pt, _ = diagnose_ciphertext_type(pt_sample)
    ic_ct, diag = diagnose_ciphertext_type(ct_sample)
    print(f"  IC Plaintext  : {ic_pt:.5f}")
    print(f"  IC Ciphertext : {ic_ct:.5f}")
    print(f"  Diagnosa      : {diag}")
    assert abs(ic_pt - ic_ct) < 0.000001, "IC harus bernilai identik pada cipher transposisi!"
    print(f"  {EMERALD}Validasi Teori IC Transposisi Terbukti Identik Sempurna!{RESET}")

    # 3. Uji AES ShiftRows
    print_step_header(3, "Simulasi Difusi AES ShiftRows")
    state_sample = [
        ['00', '01', '02', '03'],
        ['10', '11', '12', '13'],
        ['20', '21', '22', '23'],
        ['30', '31', '32', '33'],
    ]
    shifted = aes_shift_rows(state_sample)
    inv_shifted = aes_inv_shift_rows(shifted)
    assert inv_shifted == state_sample, "Gagal rekonstruksi AES ShiftRows"
    print(f"  State Awal (B1)    : {state_sample[1]}")
    print(f"  ShiftRows 1 Byte   : {shifted[1]}")
    print(f"  InvShiftRows Pulih : {inv_shifted[1]}")
    print(f"  {EMERALD}Simulasi AES ShiftRows 100% Berhasil!{RESET}\n")
