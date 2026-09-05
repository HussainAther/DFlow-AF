# AlphaFold 3 adapter boundary

DFlow-AF does not vendor AlphaFold 3 or its model parameters.

The repository currently emits **predictor-agnostic manifests**. A future adapter may transform these manifests into valid AlphaFold 3 inputs, but only after the chemical representation of D residues has been explicitly validated.

A correct adapter must preserve:

- residue identity
- residue stereochemistry
- chain identity
- covalent topology
- seed/run metadata

Generated predictor inputs should be treated as derived experiment artifacts and recorded with exact software/version provenance.
