# The square law for strip counts, and 238 recurrences proved with it

Status: a theorem with a written proof, and 238 computer-assisted proofs with exact integer certificates.
Independent human review is pending. Nothing here is new as a method. The recurrences are existing empirical
formulas by R. H. Hardin. No wider literature search was made, and nothing was sent to the OEIS.

The repository's first result ([PROOF.md](PROOF.md)) proves eleven recurrences, one at a time, by finding a zero
vector. This note explains why the recurrences in this family have the shape they have, and uses that to prove 238
of them cheaply. It refers to the repository's issue 4.

## 1. What was noticed

The OEIS entries A268622 to A270054 count grids of fixed width in which a neighbouring pair with a given sum occurs
exactly once, or at most once. The first pass ([FIRST-PASS-211.md](FIRST-PASS-211.md)) proved 211 of their recurrences.
Their characteristic polynomials were then factored over the integers
([square/logs/structure_squares.out](square/logs/structure_squares.out)).

- 209 of the 211 are perfect squares. The other two, A268888 and A268997, are a square times (x + 1). No factor occurs more than twice.
- In all 88 families where both "exactly once" and "at most once" are proved, the two entries have the same polynomial.
- For the 170 entries small enough to test with a separate machine, the square root g is the minimal recurrence of the count with no such pair at all. In the two exceptions that recurrence is g (x + 1).

So the recurrence for "one pair" is the square of the recurrence for "no pair". Sections 2 to 7 state this as a theorem
and prove it.

## 2. Setting

Fix a width, an alphabet, a target sum and a set of neighbour kinds (horizontal, vertical, diagonal, antidiagonal).
A grid has n rows. A pair is two neighbouring cells, of a chosen kind, whose entries add to the target. Each pair is
counted once. A name of the form "k X n" is turned around first, which swaps horizontal and vertical.

- Omega0 is the set of rows with no pair inside the row. Omega1 is the set of rows with exactly one.
- cnt(a, b) is the number of pairs created between row a and the row b placed below it.
- A is the 0/1 matrix on Omega0 with A[a][b] = 1 when cnt(a, b) = 0. B1 is the same with cnt(a, b) = 1.
- C goes from Omega0 to Omega1 and D from Omega1 to Omega0, each with cnt = 0.
- z(n) counts grids of n rows with no pair. e(n) counts grids with exactly one pair, and e(n) = 0 for n <= 0.
  The OEIS sequence is e(n) ("exactly once") or z(n) + e(n) ("no more than once").
- Write 1 for the all-ones vector, R_r = A^r 1 and L_p = 1^T A^p. Then z(n) = 1^T A^(n-1) 1.

## 3. The theorem

**Theorem.** Let m be a monic integer polynomial of degree D with m(A) 1 = 0. Let m*(x) = x^D m(1/x) and
Q = (m*)^2. Put N = 2D + 2 if Omega1 is not empty, and N = 2D + 1 if it is empty. Then for every n >= N, the
sequences z, e and z + e all satisfy the recurrence whose coefficients are those of Q:

    sum_(i=0)^(2D) Q_i e(n-i) = 0,   and the same for z and for z + e.

Write m = x^s h with h(0) not zero. Then m* is the reversal of h, and the recurrence has characteristic polynomial
h squared. The factor x^s does not change the recurrence. It does raise N, because D = deg h + s.

The only hypothesis used is m(A) 1 = 0 for some monic m. Nothing is assumed about minimality, about B1, C or D, or
about the alphabet, the width or the target.

## 4. The symmetry lemma

**Lemma 1.** Let P be the left-right reversal of a row. Then cnt(a, b) = cnt(rev b, rev a), and a row and its
reversal have the same number of pairs inside. So the transpose of A is P A P, and likewise for B1.

Proof. Turn the two stacked rows a (above) and b (below) through 180 degrees. The new upper row is rev b and the
new lower row is rev a. A vertical pair at position j becomes a vertical pair at position k-1-j. A diagonal pair
from position j above to j+1 below becomes a pair from k-2-j above to k-1-j below, which is diagonal again. An
antidiagonal pair stays antidiagonal in the same way. The sums do not change. So cnt is preserved, and A^T = P A P with
P a permutation matrix, P^2 = I and P 1 = 1. []

The proof of the theorem needs m(A) 1 = 0 and also 1^T m(A) = 0. Lemma 1 shows they are the same condition:
1^T m(A) = (m(A^T) 1)^T = (P m(A) P 1)^T = (P m(A) 1)^T. One hypothesis is enough. Also L_p = (P R_p)^T.

## 5. One side as a generating function

**Lemma 2.** If m(A) 1 = 0, let R(x) be the series with coefficients R_r. Then m*(x) R(x) = N_R(x), where N_R is
a polynomial of degree at most D - 1 with vector coefficients. The same holds on the left: m*(x) L(x) = N_L(x).

Proof. The coefficient of x^j in m*(x) R(x) is the sum over i of m_(D-i) R_(j-i), taken for i from 0 to min(j, D).
For j >= D this equals A^(j-D) m(A) 1, which is zero. The left side is the same, using 1^T m(A) = 0 from Lemma 1. []

## 6. The five cases, the series, and the degree count

A grid with exactly one pair has one pair, so exactly one of these cases holds.

1. The pair is between rows i and i+1. All rows are in Omega0 and all other steps have cnt = 0. The count is L_(i-1) B1 R_(n-i-1). Summed over i this is the sum over p + r = n - 2 of L_p B1 R_r.
2. The pair is inside a middle row i, with 2 <= i <= n-1. That row is in Omega1, the rest are in Omega0, all steps have cnt = 0. The sum is over p + r = n - 3 of L_p C D R_r.
3. The pair is inside the first row. The count is u A^(n-2) 1, where u is the row vector 1^T D taken over Omega1.
4. The pair is inside the last row. The count is 1^T A^(n-2) c, where c is the vector C 1 taken over Omega1.
5. There is one row only, and the count is the size of Omega1.

A sum over p + r = constant is a product of series. With E(x) the series of e(n):

    E = x^2 L B1 R + x^3 L C D R + x^2 u R + x^2 L c + |Omega1| x.

Multiply by (m*)^2 and use Lemma 2:

    (m*)^2 E = x^2 N_L B1 N_R + x^3 N_L C D N_R + x^2 (u N_R) m* + x^2 (N_L c) m* + |Omega1| x (m*)^2.

The N's have degree at most D - 1 and m* has degree at most D. So the five terms have degree at most
2D, 2D + 1, 2D + 1, 2D + 1 and 2D + 1. If Omega1 is empty, only the first term remains, and the degree is at most 2D.

The coefficient of x^n on the left is the recurrence applied to e at n, with e(n-i) = 0 for n - i <= 0. It vanishes once
n is larger than the degree of the right side. That is n >= 2D + 2, or n >= 2D + 1 when Omega1 is empty. This is the
index N of the theorem.

For z, the series is x 1^T R(x). So (m*)^2 Z = x (1^T N_R) m*, of degree at most 2D. Then z obeys the recurrence from
2D + 1 on, and z + e obeys it from N on. This ends the proof. []

## 7. Two corrections found by running it

The first guess was that the square root g of the listed polynomial itself kills the vector 1. That is false.

- g(A) 1 is not zero in 67 of the 211 entries. What kills 1 is x^s g, that is, A^s g(A) 1 = 0, with s from 0 to 6. The values of s are 0 in 144 entries, 1 in 45, 2 in 10, 3 in 4, 4 in 6 and 6 in 2. Some rows cannot be continued for long without creating a pair, and the vector 1 has a part on them. So the theorem uses m = x^s g, with D = deg g + s and N = 2 deg g + 2s + 2 (or + 1 when Omega1 is empty).
- The index N is sharp. In 111 of the 211 entries the recurrence fails at N - 1 and holds from N. In the other 100, cancellation puts the true start 1 to 5 places earlier. No bound that depends only on D and on whether Omega1 is empty can be lower.

The table of every entry is [square/table.csv](square/table.csv).

## 8. The two entries with an extra factor

For A268888 and A268997 the listed polynomial is P = g^2 (x + 1). The vector 1 is killed by m = g (x + 1) with
s = 0, D = 5 and N = 11. The theorem then gives the recurrence for P (x + 1), at every n >= N.

One more line proves the listed recurrence. Let r(n) be its residual. The residual of the recurrence for P (x + 1)
is r(n) + r(n-1). It vanishes for n >= N, so r(n) = -r(n-1) from N on. A single checked value r(N) = 0 then makes r
vanish for every n >= N - 1. The verifier checks r(N) = 0, and the start index of both entries is 10 = N - 1.

## 9. From the theorem to a proof of one recurrence

For an entry, the prover takes its name and its listed coefficients and does the following.

1. It takes the integer square root g of the listed polynomial, or of the polynomial divided by (x + 1).
2. It finds the smallest s with A^s g(A) 1 = 0. This is an identity between integers. It is checked modulo enough primes below 2^31 that their product exceeds twice a proved bound on the entries. The bound is the sum of |g_i| rho^(i+s), with rho the largest row or column sum of A.
3. It applies A one column at a time and never stores it. The largest case has 279,936 rows.
4. It computes the count a(n) for n up to N, exactly. The counts are recovered from residues by the Chinese remainder theorem, with a proved bound on their size.
5. It sets the start index to one more than the last n up to N at which the recurrence fails. By the theorem the recurrence then holds for every n from that start.

The verifier [square/verify.py](square/verify.py) redoes steps 2 to 5 with its own dense matrices. It uses the
prover's matrix-free engine only where the dense matrices do not fit. That is four entries: A269765, A269766, A269900
and A270057. Every failed check raises an error, so `python -O` behaves the same.

## 10. Results

| | |
|---|---|
| Entries of the first pass proved again | 211 of 211, same starting index in every one |
| Entries the first method did not prove, proved here | 27 of 27 |
| Entries proved in all | 238 (these include the repository's own eleven, redone as controls) |
| Starting index for the 27 | equal to the start the OEIS states, in all 27 |
| Corrupted inputs rejected | 73 of 73, also under `python -O` |

Every one of the 27 recurrences is a perfect square, and none needed the (x + 1) factor. The first method gave up
on them for size. One of them took 158 million transitions there and takes 1.4 seconds here. The slowest entry,
A269766, has a strip with 93,750 rows in Omega0 and takes about six and a half minutes to verify. The other 237 take about
three minutes together ([square/logs/verify_all.log](square/logs/verify_all.log)).

The first pass is a separate proof of the 211 by a different argument, with separately written code, and the two
agree on every starting index ([FIRST-PASS-211.md](FIRST-PASS-211.md)). Four of the 27 are checked only with the
prover's own engine, because the dense form of the verifier is too large for them.

## 11. How far the law goes, and what is not proved

For grids with exactly j pairs, the same counting on 12 narrow strips gives the power j + 1 of g for j up to 3, in 48
of 48 cases ([square/logs/task4.log](square/logs/task4.log) and [square/logs/task4b.log](square/logs/task4b.log)).
That is a test. It is not a proof.

- The law for two or more pairs is not proved. For j of 2 or more the middle factors act on other subspaces, and a proof needs the minimal polynomial of A there.
- The tie between each OEIS name and its machine rests on matching the printed terms (7 to 19 per entry) and on brute force for small cases. It is not a formal proof of how the name is read.
- No claim is made that g is the minimal polynomial of z, or that any recurrence has the smallest possible order.
- The four largest verifier runs use the prover's engine, which was cross-checked against dense matrices on 40 random specifications ([square/check_engine.py](square/check_engine.py)).
- The proof is not formalised in a proof assistant.

## 12. What a specialist would think

That one marked defect squares the denominator of a transfer-matrix count is a standard kind of fact. A specialist
will not be surprised by it. No statement of it for these OEIS entries was found. The entries list their recurrences
one by one without noting that they are squares. No wider literature search was made, so this is not a claim of
priority. Nothing was sent to the OEIS.

## 13. Check it yourself

Python 3.10 or newer. The verifier needs NumPy. The structure scripts and the tests of the law for j pairs need
python-flint. From this directory:

```sh
python3 square/verify.py square/proofs/A2*.json     # all 238; the largest entry alone takes about 7 minutes
python3 -O square/test_corrupt.py                    # 73 corrupted inputs, all rejected
python3 square/test_theory.py                        # the symmetry lemma and the five-case count
python3 square/check_engine.py | tail -3
python3 square/structure_squares.py oeis211/certs
python3 -m unittest discover -s tests -v
sha256sum -c SHA256SUMS
```

`test_theory.py` checks Lemma 1 entry by entry for the 202 certificates with at most 700 rows in Omega0. It also checks the five-case count of e(n) exactly for n from 1 to 9 on the 136 certificates with at most 60.
[square/reprove.py](square/reprove.py) runs the prover again on a named entry and compares the result with the stored
certificate. Saved outputs are in [square/logs/](square/logs/).

## Credit

The counted families and the empirical recurrences are by R. H. Hardin, from the OEIS entries listed in
[sources.json](sources.json) and, for the rest of the family, in the certificates themselves. The OEIS export is
maintained by The OEIS Foundation Inc. under CC BY-SA 4.0. Each certificate carries the entry's name, a few of its
terms and its formula line, as attributed source facts.
