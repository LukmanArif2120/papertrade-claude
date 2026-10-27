"""Kos dagangan REVERSE (AUTOTUNE/SPEC.md §3; REVERSE/SPEC.md §3.1).

Setiap sisi = komisen 0.1% + slippage ikut median nilai dagangan 20 hari pada hari isyarat.
"""
KOMISEN = 0.001


def slippage(median_nilai20):
    """0.05% jika >= USD50j; 0.10% jika USD10-50j; 0.25% jika < USD10j (atau tidak diketahui)."""
    try:
        v = float(median_nilai20)
    except (TypeError, ValueError):
        return 0.0025
    if v != v:
        return 0.0025
    if v >= 50e6:
        return 0.0005
    if v >= 10e6:
        return 0.0010
    return 0.0025


def kos_sisi(median_nilai20):
    """Kos satu sisi (pecahan harga)."""
    return KOMISEN + slippage(median_nilai20)
