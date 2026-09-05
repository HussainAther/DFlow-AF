from __future__ import annotations

import json
from pathlib import Path

from .systems import BenchmarkSystem


def system_manifest(system: BenchmarkSystem, seeds: tuple[int, ...] = (1, 2, 3, 4, 5)) -> dict:
    """Predictor-agnostic manifest.

    This deliberately does not pretend that a one-letter sequence can encode D stereochemistry.
    A predictor adapter must map each residue to chemically correct components before execution.
    """
    return {
        "schema_version": "dflow-af/0.1",
        "system_id": system.system_id,
        "description": system.description,
        "role": system.role,
        "seeds": list(seeds),
        "chains": [
            {
                "peptide_id": p.peptide_id,
                "residues": [
                    {"name": r.name, "chirality": r.chirality}
                    for r in p.residues
                ],
            }
            for p in system.peptides
        ],
        "required_qc": [
            "stereocenter_validation",
            "bond_geometry",
            "clash_check",
            "mirror_symmetry_control",
        ],
        "interpretation_boundary": "Predictor confidence is not a free energy or membrane-stability measurement.",
    }


def write_manifests(systems: tuple[BenchmarkSystem, ...], out_dir: str | Path) -> list[Path]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for system in systems:
        path = out / f"{system.system_id}.json"
        path.write_text(json.dumps(system_manifest(system), indent=2) + "\n")
        paths.append(path)
    return paths
