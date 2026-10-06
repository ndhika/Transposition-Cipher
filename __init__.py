"""
=============================================================================
PAKET           : kripto_transposisi
TOPIK           : Kriptografi Klasik — Transposition Cipher
KELOMPOK        : 2 (Transposition Cipher)
=============================================================================
Dokumentasi Batch:
Paket simulasi komprehensif 5 Varian Inti Transposition Cipher:
1. Scytale Cipher (Silinder Sparta Kuno)
2. Rail Fence Cipher (Zig-Zag Periodic Wave)
3. Route Cipher (Clockwise Inward Spiral)
4. Myszkowski Cipher (Keyword Tie-Breaker Ranking)
5. Turning Grille (Fleissner Grille Rotating Stencil)
=============================================================================
"""

try:
    from .scytale import scytale_encrypt, scytale_decrypt
    from .rail_fence import rail_fence_encrypt, rail_fence_decrypt
    from .route_cipher import route_cipher_encrypt, route_cipher_decrypt
    from .myszkowski import myszkowski_encrypt, myszkowski_decrypt
    from .turning_grille import turning_grille_encrypt, turning_grille_decrypt
except (ImportError, ValueError):
    from scytale import scytale_encrypt, scytale_decrypt
    from rail_fence import rail_fence_encrypt, rail_fence_decrypt
    from route_cipher import route_cipher_encrypt, route_cipher_decrypt
    from myszkowski import myszkowski_encrypt, myszkowski_decrypt
    from turning_grille import turning_grille_encrypt, turning_grille_decrypt

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
]
