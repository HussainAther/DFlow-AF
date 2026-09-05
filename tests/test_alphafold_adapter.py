import pytest

from dflow_af.alphafold_adapter import (
    AF3_INPUT_VERSION,
    D_ALANINE_CCD,
    AlphaFoldAdapterError,
    alphafold3_input,
)
from dflow_af.systems import canonical_systems


def _system(system_id):
    return next(s for s in canonical_systems() if s.system_id == system_id)


def test_all_l_alanine_is_unmodified_protein_chain():
    payload = alphafold3_input(_system("ala10_l"), seeds=(11,))
    protein = payload["sequences"][0]["protein"]
    assert payload["dialect"] == "alphafold3"
    assert payload["version"] == AF3_INPUT_VERSION
    assert payload["modelSeeds"] == [11]
    assert protein["id"] == "A"
    assert protein["sequence"] == "AAAAAAAAAA"
    assert "modifications" not in protein


def test_all_d_alanine_uses_dal_at_every_position():
    payload = alphafold3_input(_system("ala10_d"), seeds=(11,))
    protein = payload["sequences"][0]["protein"]
    assert protein["sequence"] == "AAAAAAAAAA"
    assert protein["modifications"] == [
        {"ptmType": D_ALANINE_CCD, "ptmPosition": i} for i in range(1, 11)
    ]


def test_seed_list_cannot_be_empty():
    with pytest.raises(AlphaFoldAdapterError):
        alphafold3_input(_system("ala10_l"), seeds=())
