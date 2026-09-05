from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .systems import BenchmarkSystem

AF3_DIALECT = "alphafold3"
AF3_INPUT_VERSION = 4
D_ALANINE_CCD = "DAL"


class AlphaFoldAdapterError(ValueError):
    """Raised when a DFlow-AF system cannot yet be represented safely in AF3."""


def _chain_id(index: int) -> str:
    """Return spreadsheet-style uppercase chain IDs: A..Z, AA, AB..."""
    if index < 0:
        raise ValueError("index must be non-negative")
    out = ""
    n = index
    while True:
        n, rem = divmod(n, 26)
        out = chr(ord("A") + rem) + out
        if n == 0:
            return out
        n -= 1


def _protein_entity(peptide, chain_id: str) -> dict:
    # Stage 1 is intentionally alanine-only. Expanding the residue map should be
    # explicit and test-backed rather than silently guessing CCD identifiers.
    if any(r.name != "ALA" for r in peptide.residues):
        raise AlphaFoldAdapterError("Stage-1 AF3 adapter currently supports alanine residues only")

    sequence = "A" * len(peptide.residues)
    modifications = []
    for pos, residue in enumerate(peptide.residues, start=1):
        if residue.chirality == "D":
            modifications.append({"ptmType": D_ALANINE_CCD, "ptmPosition": pos})
        elif residue.chirality != "L":
            raise AlphaFoldAdapterError(
                f"Unsupported chirality {residue.chirality!r} at {peptide.peptide_id}:{pos}"
            )

    protein = {
        "id": chain_id,
        "sequence": sequence,
        "description": (
            f"DFlow-AF {peptide.peptide_id}; chirality={peptide.chirality_pattern}; "
            f"D residues encoded with CCD {D_ALANINE_CCD}"
        ),
    }
    if modifications:
        protein["modifications"] = modifications
    return {"protein": protein}


def alphafold3_input(
    system: BenchmarkSystem,
    seeds: Iterable[int] = (1, 2, 3, 4, 5),
) -> dict:
    """Convert a benchmark system to the AlphaFold 3 JSON input dialect.

    Stage-1 representation rule:
      * L-alanine -> ordinary protein residue A (ALA)
      * D-alanine -> protein sequence A plus a DAL CCD modification at that position

    DAL is the wwPDB CCD component for D-alanine (type D-PEPTIDE LINKING).
    This function creates schema-shaped AF3 input; actual AF3 parsing and output
    stereochemistry remain mandatory experimental validation steps.
    """
    model_seeds = [int(seed) for seed in seeds]
    if not model_seeds:
        raise AlphaFoldAdapterError("AlphaFold 3 requires at least one model seed")

    return {
        "name": f"dflow_af_{system.system_id}",
        "sequences": [
            _protein_entity(peptide, _chain_id(i))
            for i, peptide in enumerate(system.peptides)
        ],
        "modelSeeds": model_seeds,
        "dialect": AF3_DIALECT,
        "version": AF3_INPUT_VERSION,
    }


def write_alphafold3_inputs(
    systems: Iterable[BenchmarkSystem],
    out_dir: str | Path,
    seeds: Iterable[int] = (1, 2, 3, 4, 5),
) -> list[Path]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for system in systems:
        payload = alphafold3_input(system, seeds=seeds)
        path = out / f"{system.system_id}.json"
        path.write_text(json.dumps(payload, indent=2) + "\n")
        paths.append(path)
    return paths
