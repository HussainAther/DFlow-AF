from dflow_af.mismatch import hydrophobic_mismatch


def test_zero_mismatch_has_zero_penalty():
    r = hydrophobic_mismatch(3.0, 3.0)
    assert r.mismatch_nm == 0.0
    assert r.toy_penalty == 0.0


def test_penalty_is_symmetric():
    a = hydrophobic_mismatch(2.5, 3.0)
    b = hydrophobic_mismatch(3.5, 3.0)
    assert a.toy_penalty == b.toy_penalty
