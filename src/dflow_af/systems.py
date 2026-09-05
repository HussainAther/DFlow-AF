from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Residue:
    name: str
    chirality: str  # "L", "D", or "achiral"
    hydrophobic_length_nm: float = 0.15


@dataclass(frozen=True)
class Peptide:
    peptide_id: str
    residues: tuple[Residue, ...]

    @property
    def nominal_hydrophobic_span_nm(self) -> float:
        """Toy span used only for scaffold-level mismatch calculations."""
        return sum(r.hydrophobic_length_nm for r in self.residues)

    @property
    def chirality_pattern(self) -> str:
        return "".join({"L": "L", "D": "D", "achiral": "0"}[r.chirality] for r in self.residues)


@dataclass(frozen=True)
class BenchmarkSystem:
    system_id: str
    description: str
    peptides: tuple[Peptide, ...]
    role: str


def alanine_peptide(peptide_id: str, pattern: Iterable[str]) -> Peptide:
    residues = tuple(Residue(name="ALA", chirality=c) for c in pattern)
    return Peptide(peptide_id=peptide_id, residues=residues)


def canonical_systems() -> tuple[BenchmarkSystem, ...]:
    l10 = alanine_peptide("ala10_l_chain", ["L"] * 10)
    d10 = alanine_peptide("ala10_d_chain", ["D"] * 10)
    alt = alanine_peptide("ala10_alt_chain", ["L", "D"] * 5)
    l10_b = alanine_peptide("ala10_l_chain_b", ["L"] * 10)
    d10_b = alanine_peptide("ala10_d_chain_b", ["D"] * 10)

    return (
        BenchmarkSystem("ala10_l", "All-L alanine decamer", (l10,), "mirror control"),
        BenchmarkSystem("ala10_d", "All-D alanine decamer", (d10,), "mirror control"),
        BenchmarkSystem("ala10_alt", "Alternating L/D alanine decamer", (alt,), "heterochiral sequence"),
        BenchmarkSystem("ala10_ll", "Two all-L alanine strands", (l10, l10_b), "pleated-sheet control"),
        BenchmarkSystem("ala10_ld", "One all-L and one all-D alanine strand", (l10, d10_b), "rippled-sheet candidate"),
    )
