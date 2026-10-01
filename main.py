"""
=============================================================================
PROGRAM UTAMA   : main.py
DESKRIPSI       : CLI Interaktif & Demo Otomatis Praktikum Kriptografi Klasik
MATA KULIAH     : Kriptografi Klasik — Teknik Informatika UDINUS
KELOMPOK        : 2 (Transposition Cipher)
=============================================================================
Dokumentasi Batch:
Entrypoint terminal utama untuk mendemonstrasikan seluruh materi presentasi
Transposition Cipher (38 Slide). Program ini menyediakan 3 mode operasi:
1. Uji Otomatis Seluruh Kasus Slide Presentasi (Verifikasi Matematika 100%).
2. Simulasi Interaktif Praktikum Mandiri (Uji Coba Teks & Kunci Kustom).
3. Laboratorium Kriptanalisis (Index of Coincidence) & Kaitan Modern (AES/DES).
=============================================================================
"""

import sys
import os
import time

# Pastikan folder saat ini berada di sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import (
    clean_text, render_matrix, print_step_header,
    CYAN, PURPLE, EMERALD, AMBER, ROSE, BOLD, RESET, DIM
)
from scytale import scytale_encrypt, scytale_decrypt
from rail_fence import rail_fence_encrypt, rail_fence_decrypt
from route_cipher import route_cipher_encrypt, route_cipher_decrypt
from myszkowski import myszkowski_encrypt, myszkowski_decrypt
from turning_grille import turning_grille_encrypt, turning_grille_decrypt
from advanced import (
    create_permutation_matrix, transpose_matrix, apply_permutation,
    calculate_index_of_coincidence, diagnose_ciphertext_type,
    aes_shift_rows, aes_inv_shift_rows, des_pbox_permute
)


# =============================================================================
# FUNGSI BANNER UTAMA
# =============================================================================
def print_main_banner():
    banner = f"""
{BOLD}{PURPLE}=============================================================================
      KULIAH KRIPTOGRAFI KLASIK · PROGRAM STUDI TEKNIK INFORMATIKA
                  UNIVERSITAS DIAN NUSWANTORO (UDINUS)
=============================================================================
           DEMO PRAKTIKUM & SIMULASI: TRANSPOSITION CIPHER
                            KELOMPOK 2
============================================================================={RESET}
"""
    print(banner)


# =============================================================================
# MODE 1: UJI OTOMATIS KASUS SLIDE PRESENTASI
# =============================================================================
def run_automated_suite():
    """
    =============================================================================
    FUNGSI / METODE : run_automated_suite
    KATEGORI        : Suite Pengujian Otomatis (Automated Test Suite)
    DASAR TEORI     : Memvalidasi kebenaran matematis dari ke-5 varian cipher
                      dan topik lanjutan menggunakan data sampel yang persis sama
                      dengan yang tercantum pada Slide Presentasi 01-38.
    =============================================================================
    """
    print(f"\n{BOLD}{CYAN}>>> MEMULAI PENGUJIAN OTOMATIS SESUAI SLIDE PRESENTASI <<<{RESET}\n")
    results = []

    # 1. Scytale
    print(f"{BOLD}[1/7] Menguji Varian 1: Scytale Cipher (Slide 04-08)...{RESET}")
    pt1 = "HELPMEARRIVE"
    key1 = 3
    ct1, _ = scytale_encrypt(pt1, key1, verbose=False)
    dec1, _ = scytale_decrypt(ct1, key1, verbose=False)
    ok1 = (ct1 == "HMREEILAVPRE" and dec1 == pt1)
    results.append(("Varian 1: Scytale (d=3)", "HMREEILAVPRE", ct1, ok1))

    # 2. Rail Fence
    print(f"{BOLD}[2/7] Menguji Varian 2: Rail Fence Cipher (Slide 09-13)...{RESET}")
    pt2 = "KRIPTOGRAFI"
    key2 = 3
    ct2, _ = rail_fence_encrypt(pt2, key2, verbose=False)
    dec2, _ = rail_fence_decrypt(ct2, key2, verbose=False)
    ok2 = (ct2 == "KTARPORFIGI" and dec2 == pt2)
    results.append(("Varian 2: Rail Fence (n=3)", "KTARPORFIGI", ct2, ok2))

    # 3. Route Cipher
    print(f"{BOLD}[3/7] Menguji Varian 3: Route Cipher Spiral 4x4 (Slide 14-18)...{RESET}")
    pt3 = "SERANGANDIBAWAH"
    ct3, _ = route_cipher_encrypt(pt3, 4, 4, verbose=False)
    dec3, _ = route_cipher_decrypt(ct3, 4, 4, verbose=False)
    ok3 = (ct3 == "SERANAXHAWDNGABI" and dec3 == "SERANGANDIBAWAHX")
    results.append(("Varian 3: Route Spiral (4x4)", "SERANAXHAWDNGABI", ct3, ok3))

    # 4. Myszkowski
    print(f"{BOLD}[4/7] Menguji Varian 4: Myszkowski Cipher (Slide 19-23)...{RESET}")
    pt4 = "WE ARE DISCOVERED"
    key4 = "TOMATO"
    ct4, _ = myszkowski_encrypt(pt4, key4, verbose=False)
    dec4, _ = myszkowski_decrypt(ct4, key4, verbose=False)
    ok4 = (ct4 == "ROXACDEDSEEXWEIVRX" and dec4 == "WEAREDISCOVEREDXXX")
    results.append(("Varian 4: Myszkowski (TOMATO)", "ROXACDEDSEEXWEIVRX", ct4, ok4))

    # 5. Turning Grille
    print(f"{BOLD}[5/7] Menguji Varian 5: Turning Grille 4x4 (Slide 24-29)...{RESET}")
    pt5 = "SENDTROOPSASAPXX"
    ct5, _ = turning_grille_encrypt(pt5, verbose=False)
    dec5, _ = turning_grille_decrypt(ct5, verbose=False)
    ok5 = (ct5 == "SENTADROPXPOXSAS" and dec5 == pt5)
    results.append(("Varian 5: Turning Grille (4x4)", "SENTADROPXPOXSAS", ct5, ok5))

    # 6. Matriks Permutasi Ortogonal
    print(f"{BOLD}[6/7] Menguji Aljabar Linier Matriks Permutasi (Slide 30)...{RESET}")
    vec = ['A', 'B', 'C', 'D']
    p_order = [2, 0, 3, 1]
    P = create_permutation_matrix(p_order)
    P_T = transpose_matrix(P)
    y = apply_permutation(P, vec)
    x_rec = apply_permutation(P_T, y)
    ok6 = (x_rec == vec)
    results.append(("Aljabar: Ortogonal P*P^T=I", str(vec), str(x_rec), ok6))

    # 7. Kriptanalisis IoC & AES ShiftRows
    print(f"{BOLD}[7/7] Menguji Kriptanalisis IoC & AES ShiftRows (Slide 31-34)...{RESET}")
    sample_text = "KRIPTOGRAFIKLASIKADALAHFONDASIDARISISTEMKEAMANANMODERN"
    ic_pt = calculate_index_of_coincidence(sample_text)
    state = [['00','01','02','03'],['10','11','12','13'],['20','21','22','23'],['30','31','32','33']]
    sh = aes_shift_rows(state)
    inv = aes_inv_shift_rows(sh)
    ok7 = (abs(ic_pt - 0.067) < 0.01 and inv == state)
    results.append(("Analisis: IoC (~0.068) & AES", "Shift OK", "Shift OK", ok7))

    # Tampilkan Tabel Hasil
    print(f"\n{BOLD}{CYAN}{'='*80}{RESET}")
    print(f"{BOLD}{'KASUS UJI SLIDE':<32} | {'TARGET CIPHER':<20} | {'HASIL OUTPUT':<20} | STATUS{RESET}")
    print(f"{CYAN}{'-'*80}{RESET}")
    all_pass = True
    for nama, target, actual, status in results:
        status_str = f"{EMERALD}{BOLD}[ PASS OK ]{RESET}" if status else f"{ROSE}{BOLD}[ FAIL X ]{RESET}"
        if not status:
            all_pass = False
        print(f"{nama:<32} | {target:<20} | {actual:<20} | {status_str}")
    print(f"{BOLD}{CYAN}{'='*80}{RESET}")

    if all_pass:
        print(f"\n{EMERALD}{BOLD}>>> SELURUH PENGUJIAN 100% SUKSES DAN COCOK PERSIS DENGAN SLIDE PRESENTASI! <<<{RESET}\n")
    else:
        print(f"\n{ROSE}{BOLD}>>> TERDAPAT KETIDAKSESUAIAN PADA PENGUJIAN! <<<{RESET}\n")


# =============================================================================
# MODE 2: SIMULASI PRAKTIK INTERAKTIF
# =============================================================================
def interactive_simulation():
    """
    =============================================================================
    FUNGSI / METODE : interactive_simulation
    KATEGORI        : Menu Navigasi Interaktif Terminal
    DASAR TEORI     : Memfasilitasi dosen dan mahasiswa untuk menginputkan teks
                      sembarang dan kunci pilihan sendiri untuk melihat animasi visual
                      matriks secara langsung di terminal.
    =============================================================================
    """
    while True:
        print(f"\n{BOLD}{PURPLE}--- PILIH VARIAN CIPHER UNTUK SIMULASI PRAKTIK ---{RESET}")
        print("  1. Scytale Cipher (Tongkat Sparta Kuno)")
        print("  2. Rail Fence Cipher (Zig-Zag Transposition)")
        print("  3. Route Cipher (Clockwise Inward Spiral)")
        print("  4. Myszkowski Cipher (Keyword Tie-Breaker Ranking)")
        print("  5. Turning Grille (Fleissner Grille 4x4 Stencil)")
        print("  0. Kembali ke Menu Utama")
        
        choice = input(f"\n{BOLD}Pilihan Anda (0-5): {RESET}").strip()
        
        if choice == '0':
            break
            
        elif choice == '1':
            print(f"\n{BOLD}{CYAN}=== SIMULASI SCYTALE CIPHER ==={RESET}")
            pt = input(f"Masukkan Plaintext (default 'HELPMEARRIVE'): ").strip() or "HELPMEARRIVE"
            k_str = input(f"Masukkan Kunci Diameter d (default 3): ").strip() or "3"
            try:
                k = int(k_str)
                ct, _ = scytale_encrypt(pt, k, verbose=True)
                dec, _ = scytale_decrypt(ct, k, verbose=True)
            except Exception as e:
                print(f"{ROSE}{BOLD}Error:{RESET} {e}")

        elif choice == '2':
            print(f"\n{BOLD}{CYAN}=== SIMULASI RAIL FENCE CIPHER ==={RESET}")
            pt = input(f"Masukkan Plaintext (default 'KRIPTOGRAFI'): ").strip() or "KRIPTOGRAFI"
            k_str = input(f"Masukkan Kedalaman Rel n (default 3): ").strip() or "3"
            try:
                k = int(k_str)
                ct, _ = rail_fence_encrypt(pt, k, verbose=True)
                dec, _ = rail_fence_decrypt(ct, k, verbose=True)
            except Exception as e:
                print(f"{ROSE}{BOLD}Error:{RESET} {e}")

        elif choice == '3':
            print(f"\n{BOLD}{CYAN}=== SIMULASI ROUTE CIPHER (SPIRAL 4x4) ==={RESET}")
            pt = input(f"Masukkan Plaintext (default 'SERANGANDIBAWAH'): ").strip() or "SERANGANDIBAWAH"
            try:
                ct, _ = route_cipher_encrypt(pt, 4, 4, verbose=True)
                dec, _ = route_cipher_decrypt(ct, 4, 4, verbose=True)
            except Exception as e:
                print(f"{ROSE}{BOLD}Error:{RESET} {e}")

        elif choice == '4':
            print(f"\n{BOLD}{CYAN}=== SIMULASI MYSZKOWSKI CIPHER ==={RESET}")
            pt = input(f"Masukkan Plaintext (default 'WE ARE DISCOVERED'): ").strip() or "WE ARE DISCOVERED"
            kw = input(f"Masukkan Kata Kunci (default 'TOMATO'): ").strip() or "TOMATO"
            try:
                ct, _ = myszkowski_encrypt(pt, kw, verbose=True)
                dec, _ = myszkowski_decrypt(ct, kw, verbose=True)
            except Exception as e:
                print(f"{ROSE}{BOLD}Error:{RESET} {e}")

        elif choice == '5':
            print(f"\n{BOLD}{CYAN}=== SIMULASI TURNING GRILLE (FLEISSNER 4x4) ==={RESET}")
            pt = input(f"Masukkan Plaintext 16 huruf (default 'SENDTROOPSASAPXX'): ").strip() or "SENDTROOPSASAPXX"
            try:
                ct, _ = turning_grille_encrypt(pt, verbose=True)
                dec, _ = turning_grille_decrypt(ct, verbose=True)
            except Exception as e:
                print(f"{ROSE}{BOLD}Error:{RESET} {e}")
                
        else:
            print(f"{ROSE}Pilihan tidak valid! Masukkan angka antara 0-5.{RESET}")


# =============================================================================
# MODE 3: LABORATORIUM KRIPTANALISIS & KAITAN MODERN
# =============================================================================
def cryptanalysis_lab():
    """
    =============================================================================
    FUNGSI / METODE : cryptanalysis_lab
    KATEGORI        : Laboratorium Kuantitatif
    DASAR TEORI     : Memungkinkan pengguna menguji nilai Index of Coincidence (IoC)
                      dari sembarang teks untuk mendeteksi apakah teks tersebut
                      berasal dari cipher transposisi atau substitusi.
    =============================================================================
    """
    print(f"\n{BOLD}{CYAN}=== LABORATORIUM KRIPTANALISIS INDEX OF COINCIDENCE (IoC) ==={RESET}")
    sample_default = "RKSITGPAORFKAISKLKDAAHANFNODSAIDRASITSEMEKAMAAANMNODRE"
    text = input(f"Masukkan Ciphertext yang akan dianalisis (default sampel transposisi):\n> ").strip() or sample_default
    
    ic, diagnosis = diagnose_ciphertext_type(text)
    print(f"\n  Panjang Teks     : {len(clean_text(text))} karakter")
    print(f"  Nilai Skor IC    : {BOLD}{AMBER}{ic:.5f}{RESET}")
    print(f"  Analisis Sistem  : {BOLD}{EMERALD}{diagnosis}{RESET}\n")

    print(f"{BOLD}{PURPLE}--- Nilai Rujukan Teori Kriptanalisis ---{RESET}")
    print("  * Bahasa Indonesia / Inggris : ~ 0.065 - 0.068 (Puncak Distribusi Huruf)")
    print("  * Cipher Transposisi         : ~ 0.065 - 0.068 (Frekuensi Simbol Tidak Berubah!)")
    print("  * Substitusi Polialfabetik   : ~ 0.038 - 0.042 (Distribusi Diratakan)")
    print("  * Teks Acak Murni (Random)   : ~ 0.0385 (1/26)")


# =============================================================================
# ENTRYPOINT UTAMA
# =============================================================================
def main():
    while True:
        print_main_banner()
        print(f"{BOLD}MENU UTAMA DEMO KRIPTOGRAFI:{RESET}")
        print("  1. Jalankan Uji Otomatis Kasus Slide Presentasi (Automated Test Suite)")
        print("  2. Simulasi Praktikum Interaktif (Scytale, Rail Fence, Route, Myszkowski, Grille)")
        print("  3. Laboratorium Kriptanalisis (Index of Coincidence) & Kaitan Modern")
        print("  0. Keluar dari Program")
        
        pilihan = input(f"\n{BOLD}Pilih Menu (0-3): {RESET}").strip()
        
        if pilihan == '1':
            run_automated_suite()
            input(f"\n{DIM}Tekan [Enter] untuk kembali ke Menu Utama...{RESET}")
        elif pilihan == '2':
            interactive_simulation()
        elif pilihan == '3':
            cryptanalysis_lab()
            input(f"\n{DIM}Tekan [Enter] untuk kembali ke Menu Utama...{RESET}")
        elif pilihan == '0':
            print(f"\n{BOLD}{CYAN}Terima kasih telah menggunakan program simulasi Kriptografi Kelompok 2 UDINUS!{RESET}\n")
            break
        else:
            print(f"\n{ROSE}Pilihan tidak valid! Silakan masukkan 0, 1, 2, atau 3.{RESET}")
            time.sleep(1)


if __name__ == "__main__":
    main()
