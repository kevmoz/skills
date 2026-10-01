"""Load card files and expand each pair into its flawed and clean versions."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

from .taxonomy import FLAWS

MARKER = re.compile(r"<<([A-Z])>>")
PUBLIC = Path(__file__).parent / "cards" / "public.yaml"


def _fill(text: str, slots: dict[str, str]) -> str:
    return MARKER.sub(lambda m: slots[m.group(1)], text).strip()


def expand(spec: dict, split: str) -> list[dict]:
    """One case per card: a pair becomes <id>-F (flawed) and <id>-C (clean); a decoy keeps its id."""
    cases = []
    for p in spec.get("pairs", []):
        common = {"pair": p["id"], "split": split, "domain": p["domain"], "voice": p["voice"], "why": p["why"]}
        cases.append({"id": f"{p['id']}-F", "role": "flawed", "verdict": "misleading", "flaws": [p["flaw"]],
                      "acceptable": list(p.get("acceptable", [])), "evidence": list(p["evidence"]),
                      "text": _fill(p["text"], p["flawed"]), **common})
        cases.append({"id": f"{p['id']}-C", "role": "clean", "verdict": "trustworthy", "flaws": [],
                      "acceptable": [], "evidence": [], "text": _fill(p["text"], p["clean"]), **common})
    for d in spec.get("decoys", []):
        cases.append({"id": d["id"], "pair": None, "role": "decoy", "verdict": "trustworthy", "flaws": [],
                      "acceptable": [], "evidence": [], "text": d["text"].strip(), "split": split,
                      "domain": d["domain"], "voice": d["voice"], "why": d["why"], "cue": d["cue"]})
    return cases


def load(path: Path = PUBLIC, split: str = "public") -> list[dict]:
    import yaml
    return expand(yaml.safe_load(Path(path).read_text(encoding="utf-8")), split)


def fingerprint(path: Path = PUBLIC) -> str:
    """SHA-256 of the card file, recorded with every result so a score can be tied to the exact cards."""
    return hashlib.sha256(Path(path).read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def problems(cases: list[dict]) -> list[str]:
    """Everything that would make a card unfit to score. Empty when the set is sound."""
    out = []
    ids = [c["id"] for c in cases]
    if len(ids) != len(set(ids)):
        out.append("duplicate ids")
    by_pair: dict[str, dict[str, dict]] = {}
    for c in cases:
        if MARKER.search(c["text"]):
            out.append(f"{c['id']}: unfilled marker")
        out += [f"{c['id']}: unknown flaw {f}" for f in c["flaws"] + c["acceptable"] if f not in FLAWS]
        words = len(c["text"].split())
        if not 30 <= words <= 320:
            out.append(f"{c['id']}: {words} words")
        if c["pair"]:
            by_pair.setdefault(c["pair"], {})[c["role"]] = c
    for pid, twins in by_pair.items():
        if set(twins) != {"flawed", "clean"}:
            out.append(f"{pid}: incomplete pair")
            continue
        out += [f"{pid}: evidence not in flawed text: {e!r}" for e in twins["flawed"]["evidence"]
                if e not in twins["flawed"]["text"]]
        if all(e in twins["clean"]["text"] for e in twins["flawed"]["evidence"]):
            out.append(f"{pid}: every evidence sentence also appears in the clean twin")
    return out
