import numpy as np

from dflow_af.qc import centered_rmsd, reflect_x


def test_reflection_is_involution():
    x = np.array([[1.0, 2.0, 3.0], [-2.0, 0.0, 1.0]])
    assert np.allclose(reflect_x(reflect_x(x)), x)


def test_reflected_copy_matches_after_reflection():
    x = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 1.0], [-1.0, 0.0, 2.0]])
    y = reflect_x(x)
    assert centered_rmsd(reflect_x(x), y) == 0.0
