# DFlow-AF

**Membrane-conditioned structural benchmarking for mixed-chirality peptides.**

DFlow-AF is an exploratory research scaffold connecting three layers that should remain scientifically distinct:

1. **Structure proposals** from AlphaFold 3 or another structure predictor.
2. **Stereochemical / mirror-symmetry quality control** for L-, D-, and mixed-chirality peptides.
3. **Membrane-conditioned physics** inspired by the DFlow peptide–membrane program: hydrophobic mismatch, peptide insertion, membrane thickness response, and later molecular-dynamics validation.

The first goal is **not to retrain or modify AlphaFold 3**. The first goal is to establish a reproducible benchmark that asks where structure prediction succeeds or fails for heterochiral membrane-relevant peptides.

## Core question

> Does model confidence track physical plausibility when peptide chirality and membrane hydrophobic mismatch are varied systematically?

A long-term model would condition peptide structure on sequence, residue chirality, temperature, and membrane state:

```text
sequence + chirality
        |
        v
structure predictor
        |
        v
candidate 3-D structure
        |
        v
stereochemical QC + membrane placement
        |
        v
mismatch / MD / persistence measurements
        |
        v
DFlow-style membrane update
        |
        +--> peptide retention / selection
        +--> membrane thickness
        +--> peptide association / rafts
```

## Repository status

**Stage 1 / L-D mirror-control adapter.** No biological claim is established by this repository yet.

- No AlphaFold weights or source code are bundled.
- AlphaFold confidence values are treated as model diagnostics, **not thermodynamic free energies**.
- DFlow mismatch scores are phenomenological unless calibrated against molecular simulation or experiment.
- All-L / all-D mirror controls are required before interpreting mixed-chirality systems.

## Initial benchmark panel

| ID | System | Role |
|---|---|---|
| `ala10_l` | `(L-Ala)10` | all-L mirror control |
| `ala10_d` | `(D-Ala)10` | all-D mirror control |
| `ala10_alt` | `(L-Ala-D-Ala)5` | heterochiral sequence |
| `ala10_ll` | two `(L-Ala)10` strands | homochiral assembly control |
| `ala10_ld` | `(L-Ala)10 + (D-Ala)10` | rippled-sheet candidate |

The benchmark should later expand to hydrophobic transmembrane anchors, glycine interruptions, block chirality, and temperature / membrane-thickness sweeps.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest -q

# Show the canonical benchmark systems
python -m dflow_af.cli list-systems

# Generate predictor-agnostic job manifests
python -m dflow_af.cli make-manifests --out results/manifests

# Generate native AlphaFold 3 JSON for the all-L/all-D mirror controls
python -m dflow_af.cli make-af3-inputs --out results/af3_inputs

# Run a toy hydrophobic-mismatch sweep
python -m dflow_af.cli mismatch-sweep --out results/mismatch.csv
```

## Scientific workflow

### Phase A — predictor benchmark

1. Generate chemically correct L/D systems.
2. Run structure prediction across multiple seeds.
3. Record predictor confidence and candidate structures.
4. Validate stereocenters, clashes, bond geometry, and mirror equivalence.

### Phase B — physics validation

1. Equilibrate all-L / all-D controls in an achiral environment.
2. Test whether they behave as mirror-equivalent systems within uncertainty.
3. Add explicit solvent and then membrane environments.
4. Measure structural persistence, orientation, insertion depth, bilayer deformation, and mismatch energetics.

### Phase C — DFlow coupling

Feed validated structural observables into a dynamic membrane model in which peptide retention and local membrane thickness can co-evolve.

## What would count as an interesting result?

Either outcome is useful:

- **Agreement:** predictor confidence correlates with membrane-conditioned stability.
- **Gap:** high-confidence predictions fail stereochemical or membrane-physics checks, identifying a reproducible chirality / environment blind spot.

The second outcome could motivate an actual membrane-conditioned or chirality-aware structure-prediction extension.

## Relationship to DFlow-Peptide-Membrane

DFlow-AF is intentionally separate from the existing DFlow model. DFlow is an exploratory mesoscale peptide–membrane dynamics framework. DFlow-AF adds a structural-benchmark layer without treating predictor outputs as validated DFlow parameters.

## AlphaFold 3 boundary

This repository does not redistribute AlphaFold 3 code, model parameters, or generated proprietary assets. Users are responsible for obtaining and running AlphaFold 3 under its applicable terms. DFlow-AF stores only predictor-agnostic manifests, metadata, derived measurements, and user-provided result paths.

## Citation / provenance

The research direction grows out of the peptide–membrane and cold-selective membrane work of Syed Hussain Ather and Richard Gordon. See `docs/RESEARCH_PLAN.md` and `docs/SCIENTIFIC_BOUNDARIES.md`.

## License

MIT for DFlow-AF source code. Third-party tools, models, force fields, and data retain their own licenses and terms.
