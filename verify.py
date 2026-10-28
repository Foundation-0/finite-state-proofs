#!/usr/bin/env python3
"""Verify exact finite-state certificates for eleven published recurrences."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent


def horizontal(row):
    """Occupied horizontal edges in one binary row."""
    return (row & (row >> 1)).bit_count()


def build_model(width):
    """Return (states, outgoing edges, first-row counts) for <=1 edge."""
    states = [(used, row) for used in (0, 1) for row in range(1 << width)
              if horizontal(row) <= used]
    positions = {state: i for i, state in enumerate(states)}
    edges = []
    for used, row in states:
        outgoing = []
        for new_row in range(1 << width):
            extra = horizontal(new_row) + ((row >> 1) & new_row).bit_count()
            if used + extra <= 1:
                outgoing.append(positions[used + extra, new_row])
        edges.append(outgoing)
    initial = [int(used == horizontal(row)) for used, row in states]
    return states, edges, initial


def advance(vector, edges):
    """Multiply a column vector by the transition matrix, exactly."""
    result = [0] * len(vector)
    for i, value in enumerate(vector):
        for destination in edges[i]:
            result[destination] += value
    return result


def output(vector, states, mode):
    if mode == "at_most_one":
        return sum(vector)
    if mode == "exactly_one":
        return sum(value for value, (used, _) in zip(vector, states) if used == 1)
    raise ValueError(f"unknown output mode: {mode}")


def compute_certificate(sources):
    families = []
    for family in sources["families"]:
        width = family["width"]
        recurrence = family["recurrence_coefficients"]
        degree = len(recurrence)
        states, edges, initial = build_model(width)
        powers = [initial]
        for _ in range(degree):
            powers.append(advance(powers[-1], edges))
        # q(T)v, where q(t) = t^d - c1*t^(d-1) - ... - cd.
        residual = [powers[degree][i] - sum(
            coefficient * powers[degree - lag][i]
            for lag, coefficient in enumerate(recurrence, start=1)
        ) for i in range(len(states))]
        chain = [residual]
        # A nilpotent chain in a D-dimensional space reaches zero within D
        # steps. Refuse a polynomial without this stronger vector certificate.
        while any(chain[-1]) and len(chain) <= len(states):
            chain.append(advance(chain[-1], edges))
        if any(chain[-1]):
            raise ValueError(f"width {width}: residual chain does not reach zero")
        results = []
        for claim in family["claims"]:
            mode = claim["mode"]
            residuals = [output(vector, states, mode) for vector in chain]
            start = claim["recurrence_starts_at"]
            if start < degree + 1:
                raise ValueError("recurrence start refers to unprovided a(0) or negative indices")
            if any(value for j, value in enumerate(residuals) if degree + 1 + j >= start):
                raise ValueError(f"{claim['oeis_id']}: recurrence fails at its claimed start")
            expected_initial = claim["initial_terms"]
            counts = []
            vector = initial
            for _ in expected_initial:
                counts.append(output(vector, states, mode))
                vector = advance(vector, edges)
            if counts != expected_initial:
                raise ValueError(f"{claim['oeis_id']}: published initial terms do not match")
            results.append({
                "oeis_id": claim["oeis_id"], "mode": mode,
                "recurrence_starts_at": start,
                "initial_terms": counts,
                "residual_first_n": degree + 1,
                "residual_outputs": residuals,
            })
        families.append({
            "width": width, "states": states, "outgoing_edges": edges,
            "initial_vector": initial, "recurrence_coefficients": recurrence,
            "residual_vectors": chain, "claims": results,
        })
    return {"schema_version": 1, "families": families}


def encode(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="deliberately regenerate certificate.json")
    args = parser.parse_args(argv)
    try:
        sources = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
        certificate = encode(compute_certificate(sources))
        destination = ROOT / "certificate.json"
        if args.write:
            destination.write_bytes(certificate)
        elif destination.read_bytes() != certificate:
            raise ValueError("certificate.json differs from exact regeneration")
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    count = sum(len(family["claims"]) for family in sources["families"])
    print(f"PASS: {count} recurrence claims; all residual chains reach the zero vector.")
    print("certificate sha256: " + hashlib.sha256(certificate).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())
