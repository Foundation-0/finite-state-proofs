#!/usr/bin/env python3
"""Recheck the recurrences with a separate, unreduced cell-tuple model.

No code or transition data from verify.py is used. The stored certificate's
recurrence claims and output residuals are compared with independent arithmetic;
its compact matrix is checked by verify.py, not used as evidence here.
"""

import itertools
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
SOURCE_COMMIT = "61a45ae71d35453a862da1bc68adfa6e4984411d"
# Audited against the pinned source entries, independently of verify.py.
RECURRENCES = {
    2: [6, -11, 6, -1],
    3: [10, -31, 30, -9],
    4: [16, -88, 200, -208, 96, -16],
    5: [26, -241, 994, -2060, 2218, -1201, 290, -25],
    6: [42, -665, 5138, -21972, 55274, -83769, 76202, -40273, 11304, -1296],
    7: [68, -1804, 24560, -195400, 974752, -3171360, 6871936,
        -9999248, 9740096, -6250176, 2552576, -621824, 79872, -4096],
}
STARTS = {2: 5, 3: 5, 4: 8, 5: 10, 6: 13, 7: 17}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def indexed(records, key):
    result = {}
    for record in records:
        value = record[key]
        require(value not in result, f"duplicate {key}: {value}")
        result[value] = record
    return result


def build(width):
    rows = list(itertools.product((0, 1), repeat=width))
    moves = []
    initial = []
    # All last-row patterns are kept, including unreachable states. This is
    # a different matrix of size 2^(width+1), not the reduced certificate matrix.
    for used in (0, 1):
        for old in rows:
            initial.append(int(used == sum(old[c] * old[c+1] for c in range(width-1))))
            outgoing = []
            for new_index, new in enumerate(rows):
                extra = sum(new[c] * new[c+1] for c in range(width-1))
                extra += sum(old[c+1] * new[c] for c in range(width-1))
                if used + extra <= 1:
                    outgoing.append((used + extra) * len(rows) + new_index)
            moves.append(outgoing)
    return moves, initial


def step(vector, moves):
    following = [0] * len(vector)
    for source, value in enumerate(vector):
        for destination in moves[source]:
            following[destination] += value
    return following


def count(vector, mode):
    if mode == "exactly_one":
        return sum(vector[len(vector)//2:])
    require(mode == "at_most_one", f"unknown mode: {mode}")
    return sum(vector)


def brute(height, width):
    """Direct cell enumeration; no row states or transition rules are used."""
    exact = at_most = 0
    for board in itertools.product((0, 1), repeat=height*width):
        occupied = 0
        for row in range(height):
            for column in range(width-1):
                occupied += board[row*width+column] * board[row*width+column+1]
                if row+1 < height:
                    occupied += board[row*width+column+1] * board[(row+1)*width+column]
        exact += occupied == 1
        at_most += occupied <= 1
    return exact, at_most


def verify(sources, certificate):
    require(sources["source_export_commit"] == SOURCE_COMMIT, "unexpected source pin")
    require(certificate["schema_version"] == 1, "unexpected certificate schema")
    families = indexed(sources["families"], "width")
    recorded = indexed(certificate["families"], "width")
    require(set(families) == set(RECURRENCES) == set(recorded), "expected all six widths")
    claim_count = board_count = 0
    for width, expected_recurrence in RECURRENCES.items():
        family, stored = families[width], recorded[width]
        recurrence = family["recurrence_coefficients"]
        require(all(type(x) is int for x in recurrence), f"width {width}: noninteger coefficient")
        require(recurrence == expected_recurrence == stored["recurrence_coefficients"],
                f"width {width}: recurrence differs from the audited formula")
        claims = indexed(family["claims"], "oeis_id")
        stored_claims = indexed(stored["claims"], "oeis_id")
        expected = {f"A{268987+width}": "at_most_one"}
        if width >= 3:
            expected[f"A{268878+width}"] = "exactly_one"
        require(set(claims) == set(expected) == set(stored_claims), f"width {width}: incorrect claims")
        degree = len(recurrence)
        moves, initial = build(width)
        vectors = [initial]
        last = max(degree+1, 4, *(len(claim["initial_terms"]) for claim in claims.values()))
        for _ in range(1, last):
            vectors.append(step(vectors[-1], moves))
        residual = [vectors[degree][i] - sum(
            coefficient * vectors[degree-lag][i]
            for lag, coefficient in enumerate(recurrence, 1)
        ) for i in range(len(initial))]
        chain = [residual]
        while any(chain[-1]) and len(chain) <= len(initial):
            chain.append(step(chain[-1], moves))
        require(not any(chain[-1]), f"width {width}: residual vector does not vanish")
        for seqid, mode in expected.items():
            claim, recorded_claim = claims[seqid], stored_claims[seqid]
            require(claim["mode"] == mode and claim["offset"] == 1, f"{seqid}: wrong definition metadata")
            require(claim["source_url"] == f"https://github.com/oeis/oeisdata/blob/{SOURCE_COMMIT}/seq/A268/{seqid}.seq",
                    f"{seqid}: wrong provenance URL")
            start = claim["recurrence_starts_at"]
            require(start == STARTS[width], f"{seqid}: unexpected recurrence threshold")
            terms = claim["initial_terms"]
            require(terms and all(type(x) is int for x in terms), f"{seqid}: missing/inexact initial counts")
            require(terms == [count(v, mode) for v in vectors[:len(terms)]], f"{seqid}: initial count mismatch")
            outputs = [count(v, mode) for v in chain]
            require(all(value == 0 for j, value in enumerate(outputs) if degree+1+j >= start),
                    f"{seqid}: recurrence fails during the transient")
            require(recorded_claim == {
                "oeis_id": seqid, "mode": mode, "recurrence_starts_at": start,
                "initial_terms": terms, "residual_first_n": degree+1,
                "residual_outputs": outputs,
            }, f"{seqid}: stored claim differs from independent reconstruction")
            claim_count += 1
        for height in range(1, 5):
            if height*width <= 16:
                actual = tuple(count(vectors[height-1], mode) for mode in ("exactly_one", "at_most_one"))
                require(actual == brute(height, width), f"{height} by {width}: direct enumeration mismatch")
                board_count += 1
    return claim_count, board_count


def main():
    try:
        sources = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
        certificate = json.loads((ROOT / "certificate.json").read_text(encoding="utf-8"))
        claims, boards = verify(sources, certificate)
    except (OSError, ValueError, KeyError, TypeError, IndexError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {claims} independent recurrence proofs; {boards} exhaustive board controls.")
    print("Larger cell-tuple matrices reproduce all recorded initial counts and transient outputs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
