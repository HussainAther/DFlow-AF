# Scientific boundaries

DFlow-AF deliberately separates **prediction**, **physics**, and **evolutionary interpretation**.

## Do not claim

- pLDDT / model confidence is a folding free energy.
- a high-confidence structure is membrane-stable.
- a toy mismatch score is a thermodynamic potential.
- a short MD trajectory demonstrates evolutionary selection.
- failure on one D-containing peptide establishes a general AlphaFold limitation.
- any observed mixed-chirality behavior explains the origin of homochirality without independent evidence.

## Required controls

- all-L versus all-D mirror pair
- multiple prediction seeds
- chemically validated stereocenters
- achiral-environment solution controls
- matched membrane composition and thickness
- replicated MD trajectories
- uncertainty reporting

## Relationship to existing DFlow work

The existing DFlow program uses phenomenological rules for peptide–membrane dynamics. Those rules should not be retroactively treated as validated molecular physics. DFlow-AF is intended to provide candidate structural observables and calibration targets, not to erase that distinction.
