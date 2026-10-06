"""
=============================================================================
PROGRAM UTAMA   : main.py
DESKRIPSI       : CLI Interaktif & Demo Otomatis Praktikum Kriptografi Klasik
TOPIK           : Kriptografi Klasik — Transposition Cipher
KELOMPOK        : 2 (Transposition Cipher)
=============================================================================
Dokumentasi Batch:
Entrypoint terminal utama untuk mendemonstrasikan 5 varian inti Transposition
Cipher. Program ini menyediakan 2 mode operasi:
1. Uji Otomatis Seluruh Kasus Sandi (Verifikasi Matematika 100%).
2. Simulasi Interaktif Praktikum Mandiri (Uji Coba Teks & Kunci Bebas).
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


# =============================================================================
# FUNGSI BANNER UTAMA
# =============================================================================
def print_main_banner():
    banner = f"""
{BOLD}{PURPLE}=============================================================================
             KRIPTOGRAFI KLASIK: TRANSPOSITION CIPHER SUITE
=============================================================================
                 SIMULASI & DEMO INTERAKTIF · KELOMPOK 2
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
                      menggunakan data sampel standar untuk memastikan fungsi
                      enkripsi dan dekripsi konsisten 100%.
    =============================================================================
    """
    print(f"\n{BOLD}{CYAN}>>> MEMULAI PENGUJIAN OTOMATIS 5 VARIAN SANDI TRANSPOSISI <<<{RESET}\n")
    results = []

    # 1. Scytale
    print(f"{BOLD}[1/5] Menguji Varian 1: Scytale Cipher...{RESET}")
    pt1 = "HELPMEARRIVE"
    key1 = 3
    ct1, _ = scytale_encrypt(pt1, key1, verbose=False)
    dec1, _ = scytale_decrypt(ct1, key1, verbose=False)
    ok1 = (ct1 == "HMREEILAVPRE" and dec1 == pt1)
    results.append(("Varian 1: Scytale (d=3)", "HMREEILAVPRE", ct1, ok1))

    # 2. Rail Fence
    print(f"{BOLD}[2/5] Menguji Varian 2: Rail Fence Cipher...{RESET}")
    pt2 = "KRIPTOGRAFI"
    key2 = 3
    ct2, _ = rail_fence_encrypt(pt2, key2, verbose=False)
    dec2, _ = rail_fence_decrypt(ct2, key2, verbose=False)
    ok2 = (ct2 == "KTARPORFIGI" and dec2 == pt2)
    results.append(("Varian 2: Rail Fence (n=3)", "KTARPORFIGI", ct2, ok2))

    # 3. Route Cipher
    print(f"{BOLD}[3/5] Menguji Varian 3: Route Cipher Spiral (4x4)...{RESET}")
    pt3 = "SERANGANDIBAWAH"
    ct3, _ = route_cipher_encrypt(pt3, 4, 4, verbose=False)
    dec3, _ = route_cipher_decrypt(ct3, 4, 4, verbose=False)
    ok3 = (ct3 == "SERANAXHAWDNGABI" and dec3 == "SERANGANDIBAWAHX")
    results.append(("Varian 3: Route Spiral (4x4)", "SERANAXHAWDNGABI", ct3, ok3))

    # 4. Myszkowski
    print(f"{BOLD}[4/5] Menguji Varian 4: Myszkowski Cipher...{RESET}")
    pt4 = "WE ARE DISCOVERED"
    key4 = "TOMATO"
    ct4, _ = myszkowski_encrypt(pt4, key4, verbose=False)
    dec4, _ = myszkowski_decrypt(ct4, key4, verbose=False)
    ok4 = (ct4 == "ROXACDEDSEEXWEIVRX" and dec4 == "WEAREDISCOVEREDXXX")
    results.append(("Varian 4: Myszkowski (TOMATO)", "ROXACDEDSEEXWEIVRX", ct4, ok4))

    # 5. Turning Grille
    print(f"{BOLD}[5/5] Menguji Varian 5: Turning Grille (4x4)...{RESET}")
    pt5 = "SENDTROOPSASAPXX"
    ct5, _ = turning_grille_encrypt(pt5, verbose=False)
    dec5, _ = turning_grille_decrypt(ct5, verbose=False)
    ok5 = (ct5 == "SENTADROPXPOXSAS" and dec5 == pt5)
    results.append(("Varian 5: Turning Grille (4x4)", "SENTADROPXPOXSAS", ct5, ok5))

    # Tampilkan Tabel Hasil
    print(f"\n{BOLD}{CYAN}{'='*80}{RESET}")
    print(f"{BOLD}{'KASUS UJI SANDI':<32} | {'TARGET CIPHER':<20} | {'HASIL OUTPUT':<20} | STATUS{RESET}")
    print(f"{CYAN}{'-'*80}{RESET}")
    all_pass = True
    for nama, target, actual, status in results:
        status_str = f"{EMERALD}{BOLD}[ PASS OK ]{RESET}" if status else f"{ROSE}{BOLD}[ FAIL X ]{RESET}"
        if not status:
            all_pass = False
        print(f"{nama:<32} | {target:<20} | {actual:<20} | {status_str}")
    print(f"{BOLD}{CYAN}{'='*80}{RESET}")

    if all_pass:
        print(f"\n{EMERALD}{BOLD}>>> SELURUH PENGUJIAN 5 VARIAN 100% SUKSES DAN COCOK PERSIS! <<<{RESET}\n")
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
    DASAR TEORI     : Memfasilitasi pengguna untuk memasukkan teks sembarang dan
                      kunci pilihan sendiri untuk melihat visualisasi langkah demi
                      langkah pada terminal.
    =============================================================================
    """
    while True:
        print(f"\n{BOLD}{PURPLE}--- PILIH VARIAN CIPHER UNTUK SIMULASI PRAKTIK ---{RESET}")
        print("  1. Scytale Cipher (Tongkat Silinder Sparta)")
        print("  2. Rail Fence Cipher (Sandi Gelombang Zig-Zag)")
        print("  3. Route Cipher (Sandi Spiral Masuk Searah Jarum Jam)")
        print("  4. Myszkowski Cipher (Sandi Ranking Kunci Huruf Kembar)")
        print("  5. Turning Grille (Fleissner Grille Stensil Berputar)")
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
            print(f"\n{BOLD}{CYAN}=== SIMULASI ROUTE CIPHER (SPIRAL) ==={RESET}")
            pt = input(f"Masukkan Plaintext (default 'SERANGANDIBAWAH'): ").strip() or "SERANGANDIBAWAH"
            r_str = input(f"Masukkan jumlah Baris / Rows (default 4): ").strip() or "4"
            c_str = input(f"Masukkan jumlah Kolom / Cols (default 4): ").strip() or "4"
            try:
                r_val = int(r_str)
                c_val = int(c_str)
                if r_val < 2 or c_val < 2:
                    print(f"{ROSE}Ukuran baris dan kolom harus minimal 2!{RESET}")
                else:
                    ct, _ = route_cipher_encrypt(pt, r_val, c_val, verbose=True)
                    dec, _ = route_cipher_decrypt(ct, r_val, c_val, verbose=True)
            except ValueError as e:
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
            print(f"\n{BOLD}{CYAN}=== SIMULASI TURNING GRILLE (FLEISSNER N x N) ==={RESET}")
            pt = input(f"Masukkan Plaintext (default 'SENDTROOPSASAPXX'): ").strip() or "SENDTROOPSASAPXX"
            n_str = input(f"Masukkan Ukuran Grid N (harus genap >= 4, default 4): ").strip() or "4"
            try:
                n_val = int(n_str)
                if n_val < 2 or n_val % 2 != 0:
                    print(f"{ROSE}Ukuran grid N harus bilangan genap (4, 6, 8, dst)!{RESET}")
                else:
                    ct, _ = turning_grille_encrypt(pt, n=n_val, verbose=True)
                    dec, _ = turning_grille_decrypt(ct, n=n_val, verbose=True)
            except Exception as e:
                print(f"{ROSE}{BOLD}Error:{RESET} {e}")
                
        else:
            print(f"{ROSE}Pilihan tidak valid! Masukkan angka antara 0-5.{RESET}")


# =============================================================================
# ENTRYPOINT UTAMA
# =============================================================================
def main():
    while True:
        print_main_banner()
        print(f"{BOLD}MENU UTAMA DEMO KRIPTOGRAFI:{RESET}")
        print("  1. Jalankan Uji Otomatis Kasus Sandi (Automated Test Suite)")
        print("  2. Simulasi Praktikum Interaktif (Scytale, Rail Fence, Route, Myszkowski, Grille)")
        print("  0. Keluar dari Program")
        
        pilihan = input(f"\n{BOLD}Pilih Menu (0-2): {RESET}").strip()
        
        if pilihan == '1':
            run_automated_suite()
            input(f"\n{DIM}Tekan [Enter] untuk kembali ke Menu Utama...{RESET}")
        elif pilihan == '2':
            interactive_simulation()
        elif pilihan == '0':
            print(f"\n{BOLD}{CYAN}Terima kasih telah menggunakan program simulasi Kriptografi Kelompok 2!{RESET}\n")
            break
        else:
            print(f"\n{ROSE}Pilihan tidak valid! Silakan masukkan 0, 1, atau 2.{RESET}")
            time.sleep(1)


if __name__ == "__main__":
    main()
