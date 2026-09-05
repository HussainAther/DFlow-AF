from __future__ import annotations

import argparse
import csv
from pathlib import Path

from .alphafold_adapter import write_alphafold3_inputs
from .manifests import write_manifests
from .mismatch import hydrophobic_mismatch
from .systems import canonical_systems


def cmd_list_systems(_: argparse.Namespace) -> int:
    for s in canonical_systems():
        patterns = " + ".join(p.chirality_pattern for p in s.peptides)
        print(f"{s.system_id:10s}  {patterns:24s}  {s.role}")
    return 0


def cmd_make_manifests(args: argparse.Namespace) -> int:
    paths = write_manifests(canonical_systems(), args.out)
    print(f"Wrote {len(paths)} manifests to {args.out}")
    return 0


def cmd_make_af3_inputs(args: argparse.Namespace) -> int:
    allowed = {"ala10_l", "ala10_d"}
    systems = tuple(s for s in canonical_systems() if s.system_id in allowed)
    paths = write_alphafold3_inputs(systems, args.out, seeds=tuple(args.seeds))
    print(f"Wrote {len(paths)} AlphaFold 3 inputs to {args.out}")
    return 0


def cmd_mismatch_sweep(args: argparse.Namespace) -> int:
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    systems = canonical_systems()
    thicknesses = [2.0, 2.5, 3.0, 3.5, 4.0]
    with out.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["system_id", "peptide_id", "span_nm", "membrane_nm", "mismatch_nm", "toy_penalty"],
        )
        writer.writeheader()
        for system in systems:
            for peptide in system.peptides:
                for membrane_nm in thicknesses:
                    r = hydrophobic_mismatch(peptide.nominal_hydrophobic_span_nm, membrane_nm)
                    writer.writerow({
                        "system_id": system.system_id,
                        "peptide_id": peptide.peptide_id,
                        "span_nm": r.peptide_span_nm,
                        "membrane_nm": r.membrane_hydrophobic_thickness_nm,
                        "mismatch_nm": r.mismatch_nm,
                        "toy_penalty": r.toy_penalty,
                    })
    print(f"Wrote toy mismatch sweep to {out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="dflow-af")
    sub = p.add_subparsers(dest="command", required=True)

    q = sub.add_parser("list-systems", help="List canonical benchmark systems")
    q.set_defaults(func=cmd_list_systems)

    q = sub.add_parser("make-manifests", help="Write predictor-agnostic job manifests")
    q.add_argument("--out", default="results/manifests")
    q.set_defaults(func=cmd_make_manifests)

    q = sub.add_parser("make-af3-inputs", help="Write Stage-1 AlphaFold 3 inputs for L/D mirror controls")
    q.add_argument("--out", default="results/af3_inputs")
    q.add_argument("--seeds", nargs="+", type=int, default=[1, 2, 3, 4, 5])
    q.set_defaults(func=cmd_make_af3_inputs)

    q = sub.add_parser("mismatch-sweep", help="Run a toy mismatch sweep")
    q.add_argument("--out", default="results/mismatch.csv")
    q.set_defaults(func=cmd_mismatch_sweep)
    return p


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
