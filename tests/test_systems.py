from dflow_af.systems import canonical_systems


def test_canonical_system_ids_are_unique():
    systems = canonical_systems()
    ids = [s.system_id for s in systems]
    assert len(ids) == len(set(ids))


def test_mirror_controls_exist():
    by_id = {s.system_id: s for s in canonical_systems()}
    assert by_id["ala10_l"].peptides[0].chirality_pattern == "L" * 10
    assert by_id["ala10_d"].peptides[0].chirality_pattern == "D" * 10
    assert by_id["ala10_alt"].peptides[0].chirality_pattern == "LD" * 5
