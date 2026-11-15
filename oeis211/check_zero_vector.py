#!/usr/bin/env python3
"""For each of the 211 certificates, does the residual chain z_0 = q(M) v, z_(j+1) = M z_j reach the zero vector?

The zero-vector test of the repository's own proof (PROOF.md, section 3) is sufficient for a recurrence. It is not
necessary. If z_j is nonzero for j = 0..D, where D is the number of states, then z_j is nonzero for every j, because
a vector killed by M^j is already killed by M^D (Cayley-Hamilton). This program runs the chain for D + 1 steps on
every certificate and lists the ones whose chain never reaches zero. For those the weaker test applies: D
consecutive zero residuals, which verify_all.py checks.

Usage: python3 -I check_zero_vector.py [certs_dir]    (standard library only)
Exit status 1 if the list differs from the eight entries stated in the documentation.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import verify_all as V

EXPECTED = ["A268627", "A268636", "A268748", "A268763", "A268771", "A268778", "A268909", "A268976"]


def reaches_zero(cert):
    spec, coef, data = cert["spec"], cert["recurrence"]["coefficients"], cert["data_terms"]
    labels, edges, init, accept = V.build(spec)
    D, d = len(labels), len(coef)
    vecs = [init]
    for _ in range(d):
        vecs.append(V.step(vecs[-1], edges))
    z = [vecs[d][i] - sum(coef[l - 1] * vecs[d - l][i] for l in range(1, d + 1)) for i in range(D)]
    for _ in range(D + 1):
        if not any(z):
            return True, D
        z = V.step(z, edges)
    return (not any(z)), D


def main(argv):
    cdir = argv[1] if len(argv) > 1 else os.path.join(HERE, "certs")
    never = []
    total = 0
    for name in sorted(os.listdir(cdir)):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(cdir, name), encoding="utf-8") as handle:
            cert = json.load(handle)
        zero, D = reaches_zero(cert)
        total += 1
        if not zero:
            never.append(cert["oeis_id"])
            print("never reaches zero: %s (%d states)" % (cert["oeis_id"], D))
    print("%d certificates; %d never reach the zero vector" % (total, len(never)))
    if never != EXPECTED:
        print("DIFFERS from the expected list", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
