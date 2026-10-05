"""
=============================================================================
PAKET           : kripto_transposisi
MATA KULIAH     : Kriptografi Klasik — Teknik Informatika UDINUS
KELOMPOK        : 2 (Transposition Cipher)
=============================================================================
Dokumentasi Batch:
Paket simulasi komprehensif 5 Varian Inti Transposition Cipher beserta
Analisis Kriptanalisis (Index of Coincidence), Aljabar Linier Matriks
Permutasi, dan Relevansi Kriptografi Modern (AES ShiftRows & DES P-Box).
=============================================================================
"""

try:
    from .scytale import scytale_encrypt, scytale_decrypt
    from .rail_fence import rail_fence_encrypt, rail_fence_decrypt
    from .route_cipher import route_cipher_encrypt, route_cipher_decrypt
    from .myszkowski import myszkowski_encrypt, myszkowski_decrypt
    from .turning_grille import turning_grille_encrypt, turning_grille_decrypt
    from .advanced import (
        create_permutation_matrix,
        transpose_matrix,
        apply_permutation,
        calculate_index_of_coincidence,
        diagnose_ciphertext_type,
        aes_shift_rows,
        aes_inv_shift_rows,
        des_pbox_permute,
        double_transposition_encrypt,
        double_transposition_decrypt,
    )
except (ImportError, ValueError):
    from scytale import scytale_encrypt, scytale_decrypt
    from rail_fence import rail_fence_encrypt, rail_fence_decrypt
    from route_cipher import route_cipher_encrypt, route_cipher_decrypt
    from myszkowski import myszkowski_encrypt, myszkowski_decrypt
    from turning_grille import turning_grille_encrypt, turning_grille_decrypt
    from advanced import (
        create_permutation_matrix,
        transpose_matrix,
        apply_permutation,
        calculate_index_of_coincidence,
        diagnose_ciphertext_type,
        aes_shift_rows,
        aes_inv_shift_rows,
        des_pbox_permute,
        double_transposition_encrypt,
        double_transposition_decrypt,
    )

__all__ = [
    "scytale_encrypt",
    "scytale_decrypt",
    "rail_fence_encrypt",
    "rail_fence_decrypt",
    "route_cipher_encrypt",
    "route_cipher_decrypt",
    "myszkowski_encrypt",
    "myszkowski_decrypt",
    "turning_grille_encrypt",
    "turning_grille_decrypt",
    "create_permutation_matrix",
    "transpose_matrix",
    "apply_permutation",
    "calculate_index_of_coincidence",
    "diagnose_ciphertext_type",
    "aes_shift_rows",
    "aes_inv_shift_rows",
    "des_pbox_permute",
    "double_transposition_encrypt",
    "double_transposition_decrypt",
]
