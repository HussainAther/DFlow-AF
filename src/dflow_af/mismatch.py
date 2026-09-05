from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MismatchResult:
    peptide_span_nm: float
    membrane_hydrophobic_thickness_nm: float
    mismatch_nm: float
    toy_penalty: float


def hydrophobic_mismatch(
    peptide_span_nm: float,
    membrane_hydrophobic_thickness_nm: float,
    stiffness: float = 1.0,
) -> MismatchResult:
    """Phenomenological quadratic mismatch score.

    This is a toy diagnostic, not a thermodynamic free energy. The stiffness has
    no physical meaning until independently calibrated.
    """
    mismatch = peptide_span_nm - membrane_hydrophobic_thickness_nm
    return MismatchResult(
        peptide_span_nm=peptide_span_nm,
        membrane_hydrophobic_thickness_nm=membrane_hydrophobic_thickness_nm,
        mismatch_nm=mismatch,
        toy_penalty=0.5 * stiffness * mismatch * mismatch,
    )
