# AlphaFold 3 adapter boundary

DFlow-AF does not vendor AlphaFold 3 or its model parameters.

## Stage 1 representation now implemented

The first adapter is deliberately narrow and covers only the mandatory mirror-control pair:

- `ala10_l`: `(L-Ala)10`
- `ala10_d`: `(D-Ala)10`

The emitted files use the native AlphaFold 3 JSON dialect (`version: 4`). L-alanine is represented as the ordinary protein residue `A`. D-alanine is represented as the same polymer sequence plus a protein modification at each D position using wwPDB CCD code `DAL`.

`DAL` is the Chemical Component Dictionary entry for **D-alanine** and is typed as `D-PEPTIDE LINKING`. This gives AF3 a polymer-linking chemical component with explicit D stereochemistry rather than pretending that the one-letter protein alphabet encodes chirality.

Example for an all-D alanine tripeptide:

```json
{
  "protein": {
    "id": "A",
    "sequence": "AAA",
    "modifications": [
      {"ptmType": "DAL", "ptmPosition": 1},
      {"ptmType": "DAL", "ptmPosition": 2},
      {"ptmType": "DAL", "ptmPosition": 3}
    ]
  }
}
```

## What this does *not* prove

Generating valid-looking JSON is not chemical validation. Before mixed-chirality systems are interpreted, we still must run these controls through an actual AlphaFold 3 installation and verify:

1. AF3 accepts `DAL` as a protein modification in polymer context.
2. The output model retains the intended D stereocenters.
3. `(L-Ala)10` and `(D-Ala)10` are mirror-equivalent after reflection and chemically aware atom mapping, within model/run variability.
4. No silent residue normalization back to ordinary L-alanine occurs.

If any of those fail, Stage 1 fails and the adapter must move to a user-provided CCD / alternative polymer representation rather than papering over the problem.

## Generate the controls

```bash
dflow-af make-af3-inputs --out results/af3_inputs --seeds 1 2 3 4 5
```

Generated predictor inputs are experiment artifacts. Record the exact AlphaFold 3 commit/version and CCD provenance used for every executed run.
