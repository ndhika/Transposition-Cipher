"""
=============================================================================
MODUL           : utils.py
DESKRIPSI       : Utilitas Pembantu Kriptografi & Visualisasi Terminal
TOPIK           : Kriptografi Klasik — Transposition Cipher
KELOMPOK        : 2 (Transposition Cipher)
=============================================================================
Dokumentasi Batch:
Modul ini menyediakan fungsi-fungsi dasar untuk pembersihan string (sanitasi),
padding karakter dummy, pewarnaan ANSI pada terminal, serta rendering visual
matriks ASCII resolusi tinggi agar simulasi praktikum terlihat profesional.
=============================================================================
"""

import math
import sys
from typing import List, Optional, Tuple, Any

# Pastikan output terminal mendukung UTF-8 di Windows PowerShell / CMD
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# =============================================================================
# KONSTANTA FORMATTING TERMINAL (ANSI CODES)
# =============================================================================
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
CYAN    = "\033[38;2;56;189;248m"
PURPLE  = "\033[38;2;168;85;247m"
EMERALD = "\033[38;2;52;211;153m"
AMBER   = "\033[38;2;251;191;36m"
ROSE    = "\033[38;2;251;113;133m"
BG_CARD = "\033[48;2;15;23;42m"


# =============================================================================
# FUNGSI 1: clean_text
# =============================================================================
def clean_text(text: str, keep_spaces: bool = False) -> str:
    """
    =============================================================================
    FUNGSI / METODE : clean_text
    KATEGORI        : Pra-Pemrosesan Data / Sanitasi Teks
    DASAR TEORI     : Dalam kriptografi klasik, ciphertext dan plaintext 
                      distandardisasi ke huruf kapital alfabetik A-Z untuk
                      mencegah kebocoran struktur spasi dan tanda baca.
    -----------------------------------------------------------------------------
    FORMULA MATEMATIKA:
        S' = { c | c in S and c in [A-Za-z] }, dikonversi ke UpperCase.
    
    PARAMETER:
        - text (str): Teks mentah (raw input) yang akan diproses.
        - keep_spaces (bool, opsional): Jika True, spasi akan dipertahankan.
                                       Default bernilai False.
    
    OUTPUT / RETURN:
        - str: Teks terkapitalisasi murni tanpa karakter non-alfabetik.
    
    KOMPLEKSITAS:
        - Waktu : O(N), di mana N adalah panjang karakter string masukan.
        - Ruang : O(N) untuk mengalokasikan string hasil sanitasi.
        
    CONTOH PENGGUNAAN:
        >>> clean_text("Help Me, Arrive! 123")
        'HELPMEARRIVE'
    =============================================================================
    """
    if not isinstance(text, str):
        raise TypeError(f"Ekspektasi tipe data string, diterima: {type(text).__name__}")

    sanitized = []
    for char in text.upper():
        if 'A' <= char <= 'Z':
            sanitized.append(char)
        elif keep_spaces and char == ' ':
            sanitized.append(' ')
            
    return "".join(sanitized)


# =============================================================================
# FUNGSI 2: pad_text
# =============================================================================
def pad_text(text: str, block_size: int, pad_char: str = 'X') -> Tuple[str, int]:
    """
    =============================================================================
    FUNGSI / METODE : pad_text
    KATEGORI        : Pra-Pemrosesan Data / Padding Matriks
    DASAR TEORI     : Cipher transposisi berbasis grid 2D (seperti Route Cipher 
                      atau Myszkowski) mensyaratkan jumlah elemen |P| merupakan
                      kelipatan eksak dari dimensi matriks (r x c). Karakter dummy
                      (umumnya 'X') ditambahkan di akhir jika terjadi sisa pembagian.
    -----------------------------------------------------------------------------
    FORMULA MATEMATIKA:
        remainder = |P| mod B
        k_padding = (B - remainder) mod B
        P_padded  = P || (pad_char * k_padding)
    
    PARAMETER:
        - text (str): Teks yang sudah disanitasi.
        - block_size (int): Ukuran blok kapasitas grid (jumlah kolom / sel).
        - pad_char (str, opsional): Karakter dummy pengisi. Default 'X'.
    
    OUTPUT / RETURN:
        - Tuple[str, int]: Pasangan (teks_setelah_padding, jumlah_karakter_dummy).
    
    KOMPLEKSITAS:
        - Waktu : O(1) perhitungan modulo, O(N + K) pembuatan string.
        - Ruang : O(N + K).
        
    CONTOH PENGGUNAAN:
        >>> pad_text("SERANGANDIBAWAH", 16, 'X')
        ('SERANGANDIBAWAHX', 1)
    =============================================================================
    """
    if block_size <= 0:
        raise ValueError(f"Ukuran blok (block_size) harus bilangan positif > 0, diterima: {block_size}")
    
    remainder = len(text) % block_size
    pad_needed = (block_size - remainder) % block_size
    
    return text + (pad_char.upper() * pad_needed), pad_needed


# =============================================================================
# FUNGSI 3: print_step_header
# =============================================================================
def print_step_header(step_no: int, title: str, subtitle: str = "") -> None:
    """
    =============================================================================
    FUNGSI / METODE : print_step_header
    KATEGORI        : Visualisasi Terminal & UI
    DASAR TEORI     : Memberikan penanda visual terstruktur per tahapan eksekusi
                      algoritma agar dosen penguji dan mahasiswa dapat mengikuti
                      aliran logika kriptografi tahap demi tahap.
    -----------------------------------------------------------------------------
    PARAMETER:
        - step_no (int): Nomor langkah pengerjaan (misal 1, 2, dst).
        - title (str): Judul tahapan eksekusi algoritma.
        - subtitle (str, opsional): Keterangan rinci atau formula sub-tahapan.
    =============================================================================
    """
    badge = f"{BOLD}{CYAN}[LANGKAH {step_no:02d}]{RESET}"
    print(f"\n{badge} {BOLD}{title}{RESET}")
    if subtitle:
        print(f"  {DIM}{subtitle}{RESET}")
    print(f"  {CYAN}{'-' * 65}{RESET}")


# =============================================================================
# FUNGSI 4: render_matrix
# =============================================================================
def render_matrix(
    matrix: List[List[Any]], 
    col_headers: Optional[List[str]] = None, 
    row_labels: Optional[List[str]] = None,
    highlight_coords: Optional[List[Tuple[int, int]]] = None,
    color_code: str = CYAN
) -> str:
    """
    =============================================================================
    FUNGSI / METODE : render_matrix
    KATEGORI        : Visualisasi Grid Matriks Kriptografi
    DASAR TEORI     : Menggambar struktur 2 dimensi matriks transposisi ke terminal
                      dengan garis pembatas ASCII rapi, perataan sel otomatis,
                      serta pewarnaan khusus pada sel yang sedang diakses.
    -----------------------------------------------------------------------------
    PARAMETER:
        - matrix (List[List[Any]]): Matriks 2D data teks/simbol.
        - col_headers (List[str], opsional): Label nama kolom di bagian atas.
        - row_labels (List[str], opsional): Label baris di sisi paling kiri.
        - highlight_coords (List[Tuple[int, int]], opsional): Koordinat (r, c)
          dari sel-sel yang ingin diberi highlight warna cerah.
        - color_code (str, opsional): Kode warna ANSI untuk border & highlight.
    
    OUTPUT / RETURN:
        - str: Representasi string multi-baris tabel ASCII terformat.
    =============================================================================
    """
    if not matrix or not matrix[0]:
        return "  [Matriks Kosong]"

    rows = len(matrix)
    cols = len(matrix[0])
    
    # Hitung lebar maksimum tiap kolom untuk perataan
    col_widths = [1] * cols
    for c in range(cols):
        for r in range(rows):
            val_len = len(str(matrix[r][c]))
            if val_len > col_widths[c]:
                col_widths[c] = val_len
        if col_headers and c < len(col_headers):
            if len(col_headers[c]) > col_widths[c]:
                col_widths[c] = len(col_headers[c])
        col_widths[c] = max(col_widths[c] + 2, 5)

    row_label_width = 0
    if row_labels:
        row_label_width = max(len(str(lbl)) for lbl in row_labels) + 2

    lines = []
    
    # Header Kolom
    if col_headers:
        header_line = " " * row_label_width
        for c in range(cols):
            val = col_headers[c] if c < len(col_headers) else f"K{c}"
            header_line += f"{BOLD}{color_code}{val:^{col_widths[c]}}{RESET}"
        lines.append(header_line)
        
    # Garis Pembatas Atas
    border_top = " " * row_label_width + "+" + "+".join("-" * w for w in col_widths) + "+"
    lines.append(f"{DIM}{border_top}{RESET}")
    
    hl_set = set(highlight_coords) if highlight_coords else set()
    
    for r in range(rows):
        row_str = ""
        if row_labels:
            lbl = row_labels[r] if r < len(row_labels) else f"B{r}"
            row_str += f"{BOLD}{lbl:>{row_label_width-1}} {RESET}|"
        else:
            row_str += "|"
            
        for c in range(cols):
            cell_val = str(matrix[r][c])
            if (r, c) in hl_set:
                formatted_val = f"{BOLD}{EMERALD}{cell_val:^{col_widths[c]}}{RESET}"
            elif cell_val == '.' or cell_val == ' ':
                formatted_val = f"{DIM}{cell_val:^{col_widths[c]}}{RESET}"
            else:
                formatted_val = f"{cell_val:^{col_widths[c]}}"
            row_str += formatted_val + f"{DIM}|{RESET}"
            
        lines.append(row_str)
        lines.append(f"{DIM}{border_top}{RESET}")
        
    return "\n".join("  " + l for l in lines)
