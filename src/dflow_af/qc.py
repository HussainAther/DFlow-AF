from __future__ import annotations

import numpy as np


def reflect_x(coords: np.ndarray) -> np.ndarray:
    """Mirror Cartesian coordinates through the yz-plane."""
    arr = np.asarray(coords, dtype=float)
    if arr.ndim != 2 or arr.shape[1] != 3:
        raise ValueError("coords must have shape (N, 3)")
    mirrored = arr.copy()
    mirrored[:, 0] *= -1.0
    return mirrored


def centered_rmsd(a: np.ndarray, b: np.ndarray) -> float:
    """Centroid-aligned RMSD without rotational fitting.

    Useful only as a simple regression check. Production mirror tests should use
    a chemically aware atom mapping and optimal rigid-body alignment.
    """
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.shape != b.shape or a.ndim != 2 or a.shape[1] != 3:
        raise ValueError("a and b must share shape (N, 3)")
    aa = a - a.mean(axis=0)
    bb = b - b.mean(axis=0)
    return float(np.sqrt(np.mean(np.sum((aa - bb) ** 2, axis=1))))
