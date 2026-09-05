# DFlow-AF research plan

## Objective

Test whether contemporary biomolecular structure prediction remains physically reliable when peptide chirality and membrane environment are moved outside the ordinary all-L soluble-protein regime.

## Hypotheses

### H1 — chirality gap
A predictor trained primarily on naturally occurring protein structures may show systematic confidence or geometry failures for D-containing and mixed-D/L peptides.

### H2 — membrane-conditioning gap
Predictor confidence may not track stability once hydrophobic mismatch, insertion orientation, membrane thickness, and lipid deformation are included.

### H3 — physically meaningful coupling
Some peptide motifs may remain structurally persistent only within particular membrane-thickness / temperature regimes, creating a possible physical selection mechanism.

## Milestones

### M0 — scaffold
- benchmark systems
- manifests
- toy mismatch score
- scientific-boundary documentation

### M1 — stereochemical controls
- chemically correct all-L/all-D representations
- mirror-symmetry QC
- repeated structure-prediction seeds

### M2 — heterochiral screen
- alternating D/L
- D/L blocks
- glycine interruptions
- hydrophobic anchor-length series

### M3 — MD reference
- explicit solvent controls
- membrane insertion/orientation
- replicated trajectories
- uncertainty estimates

### M4 — DFlow coupling
- calibrated mismatch response
- peptide retention / insertion events
- local membrane-thickness feedback
- peptide association / raft observables

### M5 — public technical note
A benchmark paper or preprint should be considered only after M1–M3 produce reproducible results.
