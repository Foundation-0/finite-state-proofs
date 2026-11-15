#!/usr/bin/env python3
"""Run the prover again on named entries and compare its output with the stored certificate.

Usage: python3 reprove.py A268622 A268888 ...     (needs NumPy)
The prover reads the name, the coefficients and the printed terms from proofs/<id>.json and rebuilds everything
else. The output must equal the stored fields. Exit status 1 on any difference.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sqprove import prove  # noqa: E402

FIELDS = (("sqrt_poly", "sqrt_poly"), ("extra_x_plus_1", "extra_x_plus_1"), ("nilpotency_s", "nilp_s"),
          ("primes_hypothesis", "primes_hyp"), ("primes_window", "primes_win"), ("theorem_index", "theorem_index"),
          ("start", "start"), ("omega0", "omega0"), ("omega1", "omega1"), ("rho_rows", "rho_rows"),
          ("rho_cols", "rho_cols"))


def main(ids):
    if not ids:
        raise SystemExit(__doc__)
    bad = 0
    for name in ids:
        with open(os.path.join(HERE, "proofs", name + ".json"), encoding="utf-8") as handle:
            stored = json.load(handle)
        result = prove(stored["name"], stored["coefficients"], stored["data_terms"], log=lambda *a: None)
        differences = [mine for mine, theirs in FIELDS if result.get(theirs) != stored[mine]]
        if result.get("status") != "proved" or result.get("data_match") is not True:
            differences.append("status or data match")
        print(name, "same as stored certificate" if not differences else "DIFFERS in " + ", ".join(differences))
        bad += bool(differences)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
