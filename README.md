# Finite-state proofs

Exact, replayable proofs of counting formulas that were discovered empirically.
The first result treats binary rectangular arrays containing exactly one, or at
most one, occupied horizontal or antidiagonal edge. It supplies finite
certificates for **eleven published recurrences**, for strip widths 2 through 7.

**Status:** proposed computer-assisted proofs, checked by exact integer code and
small exhaustive enumeration; awaiting human review. These are proofs of
existing formulas, not new sequences or a claim to have found the first proofs.
No OEIS submission has been made.

## First result

| Width | Exactly one | At most one | Recurrence order | Valid from |
|---:|---|---|---:|---:|
| 2 | — | [A268989](https://oeis.org/A268989) | 4 | n = 5 |
| 3 | [A268881](https://oeis.org/A268881) | [A268990](https://oeis.org/A268990) | 4 | n = 5 |
| 4 | [A268882](https://oeis.org/A268882) | [A268991](https://oeis.org/A268991) | 6 | n = 8 |
| 5 | [A268883](https://oeis.org/A268883) | [A268992](https://oeis.org/A268992) | 8 | n = 10 |
| 6 | [A268884](https://oeis.org/A268884) | [A268993](https://oeis.org/A268993) | 10 | n = 13 |
| 7 | [A268885](https://oeis.org/A268885) | [A268994](https://oeis.org/A268994) | 14 | n = 17 |

These formulas are credited to R. H. Hardin. The pinned OEIS export still calls
them empirical. Our contribution is an explicit state model and an exact
certificate explaining why each recurrence holds for every later index.
The method also checks the exceptional early indices: for example, applying the
width-4 recurrence one term too soon gives an error of 4 in both sequences.

## Check it yourself

Python 3.10+; standard library only. No downloads or proof-system installation:

```sh
python3 verify.py
python3 verify_independent.py
python3 -m unittest discover -s tests -v
sha256sum -c SHA256SUMS
```

`verify.py` rebuilds all state graphs and exact integer residual vectors, checks
the recurrences and initial counts, and compares the regenerated certificate
byte for byte with `certificate.json`. It reads paths relative to itself.
To deliberately regenerate the stored certificate, use `python3 verify.py --write`.

`verify_independent.py` uses larger matrices built from cell tuples, with no
imports or transition data from the first program. It independently verifies
all eleven recurrences and 19 exhaustive board controls. CI runs both algorithms
and the regression tests on Python 3.10 and 3.14.

The [proof](PROOF.md) explains why the finite calculation proves the recurrence
for infinitely many indices. Tests independently enumerate all small boards,
and deliberately corrupt coefficients, initial counts, onset indices and the
stored certificate to ensure those mistakes are rejected.

## Files and limits

- [PROOF.md](PROOF.md): combinatorial model and all-indices argument.
- [sources.json](sources.json): eleven source links pinned to an OEIS export
  commit, recurrence coefficients, published initial counts and onset indices.
- [certificate.json](certificate.json): state graphs, initial vectors and exact
  residual chains, ending in zero vectors.
- [verify.py](verify.py): original generator and verifier.
- [verify_independent.py](verify_independent.py): independently constructed model
  and exact verification.
- [tests/test_verify.py](tests/test_verify.py): independent enumeration and
  deliberately broken inputs.
- [NOTICE.md](NOTICE.md): source attribution and licensing scope.
- [SHA256SUMS](SHA256SUMS): hashes of both verifiers, source ledger and certificate.

The proof still depends on the state model correctly expressing the original
counting problem. Exhaustive tests check small cases; the written bijection
covers arbitrary height. This is not a Lean formalization. A search for the
sequence IDs with “proof” and “transfer matrix” found no earlier explicit proof,
but that search is not an exhaustive priority assessment.

## Credit

R. H. Hardin defined the counted families and supplied the empirical recurrences;
Colin Barker supplied generating functions for several entries. OpenAI Codex
(GPT-6), working for Ahraz Arifuddin (@ahrazzle), constructed this state model,
computed the certificates and wrote the proof and tests. Human sign-off is
pending. See [NOTICE.md](NOTICE.md).
