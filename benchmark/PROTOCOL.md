# Benchmark protocol

## Stage 1 — chemical representation

1. Define chemically correct residue stereochemistry using predictor-supported custom components or another validated representation.
2. Do not encode D residues merely by changing labels in an L-only sequence alphabet.
3. Record the exact chemical-component definitions used for every run.

## Stage 2 — structure prediction

1. Run each system across multiple random seeds.
2. Keep template/MSA settings identical across mirror controls.
3. Archive run metadata separately from large generated structures.

## Stage 3 — mandatory QC

1. Validate stereocenters.
2. Check bond geometry and severe clashes.
3. Compare all-L and all-D controls after geometric reflection and chemically aware atom mapping.
4. Reject the benchmark interpretation if the mirror controls are not physically symmetric in an achiral reference environment within uncertainty.

## Stage 4 — physics validation

1. Begin with explicit-solvent atomistic controls.
2. Add membrane systems only after solution controls pass.
3. Measure persistence, radius of gyration, secondary structure, insertion/orientation, and bilayer deformation.
4. Use replicated trajectories and uncertainty intervals.

## Stage 5 — DFlow coupling

Only validated observables may become inputs or calibration targets for DFlow-style membrane dynamics.

**Primary pass criterion:** all-L and all-D controls behave as mirrored equivalents in an achiral environment within simulation uncertainty.
