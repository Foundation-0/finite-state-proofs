# The method of this repository run on 211 recurrences

Status: computer-assisted proofs with exact integer certificates, accepted by a verifier and by a separately written
spot proof. Independent human review is pending. The recurrences are existing empirical formulas by R. H. Hardin.
No literature search was made for earlier proofs, and nothing was sent to the OEIS. It refers to the repository's issue 4.

[PROOF.md](PROOF.md) proves eleven recurrences by following a counting machine until a residual vector is zero. This
note records the same method run on the OEIS entries A268622 to A270054, and one finding about the test PROOF.md uses.
[SQUARE-LAW.md](SQUARE-LAW.md) proves all 211 again by a different argument.

## 1. What was run

Each of the 211 sequences counts grids of fixed width, with entries from a small alphabet, in which a neighbouring
pair adding up to a given total occurs exactly once, or at most once. One reading of the OEIS wording fits every
printed term of all 211 entries: unordered neighbouring pairs, each counted once.

| | |
|---|---|
| Entries proved | 211, in the range A268622 to A270054 |
| Families | 34: alphabets of 2 to 7 values, four kinds of neighbour, strip widths 1 to 7, both orientations |
| Recurrence order | 2 to 68 |
| States in the machine | 7 to 2,048 |
| The repository's own eleven | included as controls, marked in the last columns of [oeis211/table.csv](oeis211/table.csv) |

Of the 211, 200 are not in the repository's first result. None of the 211 listed recurrences turned out to be false.
The list is [oeis211/table.md](oeis211/table.md), and each entry has a certificate in [oeis211/certs/](oeis211/certs/).

## 2. Why a finite check proves it for every n

Rows are added one at a time. A state is the last row together with the number of counted pairs so far. That gives a
matrix M of size D, and the count is a(n) = u M^(n-1) v. For a claimed recurrence, let r(n) be the amount by which it
fails at n. Then r(n) is itself of the form u M^j w.

By the Cayley-Hamilton theorem such a sequence obeys a recurrence of order D. So if r(n) is zero for D consecutive
values of n, it is zero for every later n. The terms printed at the OEIS (11 to 31 per entry) are never enough for
that. The terms come from the machine. The printed terms only confirm that the definition was read correctly.

## 3. The zero-vector test is sufficient and not necessary

[PROOF.md](PROOF.md), section 3, asks for the vector z_m = M^m q(M) v to reach zero. If it does, every later residual
is zero. That test is sufficient. It is not necessary.

The residual is r_j = L(z_j), where L reads off the counted states. It can vanish for every j while z_j stays nonzero,
when z_0 has a part that L cannot see. The weaker test is then enough: D consecutive zero residuals, where D is the
number of states. By Cayley-Hamilton that forces all later residuals to be zero.

Eight true recurrences never reach a zero vector. They are A268627, A268636, A268748, A268763, A268771, A268778,
A268909 and A268976. For them the chain is nonzero at every one of the first D + 1 steps, and so it is nonzero
forever, because a vector killed by a power of M is already killed by M^D. [oeis211/check_zero_vector.py](oeis211/check_zero_vector.py)
runs the chain on all 211 certificates and lists exactly these eight
([oeis211/logs/check_zero_vector.out](oeis211/logs/check_zero_vector.out)). Their certificates have the kind
`scalar_window`, and the other 203 have the kind `vector_chain`.

The first method therefore proves them by the weaker test. The repository's own `verify.py` is not changed, and it
handles the eleven it was written for.

## 4. How it was checked

- [oeis211/verify_all.py](oeis211/verify_all.py) rebuilds every machine from the definition and checks all 211 certificates in exact integers. It reads no graph from the certificate. It takes about 25 seconds, with and without `-O`, and uses only the standard library.
- [oeis211/test_corrupt.py](oeis211/test_corrupt.py) changes six certificates in 105 ways in memory (a coefficient, a data term, the start index, the graph digest, the state count, the total, the neighbours, the mode, a residual and more). It rejects 105 of 105, with and without `-O`.
- The verifier also counts every small grid cell by cell, with no machine, and matches the machine and the printed terms.
- [oeis211/spot_proof.py](oeis211/spot_proof.py) is a third program, written without reading the builder or the verifier. It builds its own machine straight from the OEIS wording and proves 46 of the entries again, one from each combination of neighbour kind, alphabet, condition and orientation. All 46 give the same starting index as the certificates ([oeis211/logs/spot_proof.out](oeis211/logs/spot_proof.out)).
- The proofs of [SQUARE-LAW.md](SQUARE-LAW.md) use a different argument and separately written code. The starting index agrees in all 211.

Two programs written apart, using different arguments, agree on every starting index of the 211, and a third proves 46
of them again. That is the review's VERIFIED.

## 5. Findings on the way

1. In 121 entries the OEIS states a range such as "for n>7". In every one of the 121, that range equals the proved starting index.
2. In 61 entries the recurrence has more terms than the OEIS prints. The printed data cannot test those at all.
3. The test of PROOF.md is stricter than it needs to be. Section 3 above gives the eight entries it would miss.

## 6. What stops the method

The number of states grows by about 1.7 times per extra column for two values, and much faster for larger alphabets.
27 entries of this family were left unproved by this method for that reason, and the largest has 24,192 states. They
are proved by the method of [SQUARE-LAW.md](SQUARE-LAW.md).

Square grids and tables with two free parameters have no fixed width, so the method does not apply to them. Other
families by the same contributor are also finite-state, and each would need its own parser.

## 7. Check it yourself

Python 3.10 or newer, standard library only. From this directory:

```sh
python3 -O oeis211/verify_all.py            # all 211 certificates
python3 -O oeis211/test_corrupt.py          # corrupted certificates are rejected
python3 -I oeis211/spot_proof.py oeis211/certs
python3 -I oeis211/check_zero_vector.py     # the eight entries of section 3
python3 -m unittest discover -s tests -v
sha256sum -c SHA256SUMS
```

Saved outputs are in [oeis211/logs/](oeis211/logs/). The builder that wrote the certificates is not included, because
it reads local copies of the OEIS pages. The verifier shares no code with it.

## 8. Not verified

- The match between grids and paths through the machine is argued, not machine-checked.
- Whether any of these recurrences has been proved elsewhere.
- Whether the listed orders are the smallest possible.

## Credit

The counted families and the empirical recurrences are by R. H. Hardin, from the OEIS entries named in the
certificates. The OEIS export is maintained by The OEIS Foundation Inc. under CC BY-SA 4.0. Each certificate carries
the entry's name, a few of its terms and its formula line, as attributed source facts, with the address and the date
read.
