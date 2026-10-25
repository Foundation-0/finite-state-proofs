# Finite-state proof of eleven strip-counting recurrences

Status: computer-assisted proof with exact integer certificates; independent
human review is pending. The recurrences themselves are existing empirical
formulas by R. H. Hardin. This note supplies a proof argument and finite witnesses;
it makes no claim to priority over an unlocated earlier proof.

## 1. Statement and source

For a binary array with n rows and w columns, call an edge occupied if both of its
endpoints are 1. Count each horizontal neighboring pair once and each
antidiagonal neighboring pair once. With columns numbered 0 through w−1,
antidiagonal edges join (r,c+1) to (r+1,c). Let E_w(n) count arrays with exactly
one occupied edge and B_w(n) count arrays with at most one.

The following eleven OEIS sequences have these interpretations:

| w | E_w(n) | B_w(n) | recurrence degree d | starting index s |
|---:|---|---|---:|---:|
| 2 | not claimed here | A268989 | 4 | 5 |
| 3 | A268881 | A268990 | 4 | 5 |
| 4 | A268882 | A268991 | 6 | 8 |
| 5 | A268883 | A268992 | 8 | 10 |
| 6 | A268884 | A268993 | 10 | 13 |
| 7 | A268885 | A268994 | 14 | 17 |

**Claim.** For every row of the table and each listed sequence a(n), the
coefficients c_1,...,c_d recorded in `sources.json` satisfy

    a(n) = c_1 a(n−1) + ... + c_d a(n−d)    for every integer n ≥ s.

For widths 2 and 3, s=d+1 is the first index at which the recurrence uses only
positive-index terms. For larger widths the exceptional early indices matter.
For example, the width-4 recurrence is

    a(n) = 16a(n−1) − 88a(n−2) + 200a(n−3)
           − 208a(n−4) + 96a(n−5) − 16a(n−6),  n ≥ 8.

The source ledger pins every entry to the OEIS Git export commit
`61a45ae71d35453a862da1bc68adfa6e4984411d`. Every cited recurrence is labelled
empirical in that snapshot. The coefficients and initial counts are source
facts credited to Hardin; they were not discovered in this project.

## 2. The finite state representation

Represent one row by the integer mask r, with bit c equal to its entry in column c.
Define

    h(r)   = popcount(r & (r >> 1)),
    d(r,s) = popcount((r >> 1) & s).

Here h(r) counts horizontal occupied edges of row r. The second expression
counts the antidiagonal edges from row r to the next row s.

A state is a pair (k,r), where k is either 0 or 1 and h(r)≤k. Its meaning is:
the partial array has last row r and exactly k occupied edges in all rows so far.
There are finitely many such states because 0≤r<2^w.

The first-row vector v has component

    v[(k,r)] = 1 if k=h(r), and 0 otherwise.

Each possible single-row array is counted once. Rows with more than one
horizontal occupied edge do not appear in any counted array.

Appending row s contributes h(s) horizontal edges and d(r,s) antidiagonal edges.
If k'=k+h(s)+d(r,s)≤1, there is one transition from (k,r) to (k',s); otherwise
there is no permitted transition. Let T be its matrix, with the **destination**
index first, so that state-count column vectors update by multiplication by T.
The machine-readable certificate stores each column as its list of destinations.

**Bijection.** An array with at most one occupied edge uniquely determines its
sequence of row masks and cumulative occupied-edge counts. These form a path
starting in v and following the stated transitions. Conversely, a path fixes
every row of an array; the transition rule counts exactly the newly added edges,
so the path's final k is precisely the array's occupied-edge count. No horizontal
or antidiagonal edge is omitted or counted twice, and no edge joins nonconsecutive
rows. Thus the correspondence is one-to-one for every positive height n.

It follows by induction that the state counts for n rows are

    v_n = T^(n−1) v.

Let L_E sum components with k=1, and let L_B sum all components. The bijection
proves E_w(n)=L_E(v_n) and B_w(n)=L_B(v_n). This is a statement for arbitrary n,
not an inference from agreement with the first few sequence terms.

## 3. A finite certificate settles all later indices

For recurrence coefficients c_1,...,c_d, define

    q(t) = t^d − c_1 t^(d−1) − ... − c_d,
    z_0 = q(T)v,
    z_(j+1) = T z_j.

By expansion and the previous section, for either output L and any j≥0,

    L(z_j) = a(d+1+j) − Σ_(i=1)^d c_i a(d+1+j−i).

Therefore L(z_j) is exactly the recurrence residual at index n=d+1+j.

Suppose a finite calculation establishes z_m=0. Linearity gives z_j=0 for every
j≥m. If it also establishes L(z_j)=0 for the finitely many j<m with d+1+j≥s,
the recurrence holds at every n≥s. This conclusion requires a zero **vector**,
not merely a long run of zero scalar residuals or fitted initial terms.

The certificate contains the complete integer state graph, v, q's coefficients,
and z_0,...,z_m. `verify.py` independently regenerates these objects from the
state rule and confirms the last vector is exactly zero. It also confirms all
required scalar residuals and the attributed initial terms. Every operation
uses Python's unbounded integers; no floating-point computation, numerical
tolerance, or probabilistic polynomial test occurs.

## 4. Exact witnesses and exceptional indices

The regenerated objects have these sizes:

| w | states | transitions | d | m, first zero vector |
|---:|---:|---:|---:|---:|
| 2 | 7 | 21 | 4 | 0 |
| 3 | 12 | 56 | 4 | 1 |
| 4 | 21 | 152 | 6 | 2 |
| 5 | 36 | 398 | 8 | 2 |
| 6 | 62 | 1051 | 10 | 3 |
| 7 | 106 | 2734 | 14 | 3 |

The scalar residual pairs below are (L_E(z_j),L_B(z_j)); the width-2 E output is
computed by the model but is not one of the eleven source claims.

| w | first residual index | residual pairs from j=0 through m |
|---:|---:|---|
| 2 | 5 | (0,0) |
| 3 | 5 | (0,0), (0,0) |
| 4 | 7 | (4,4), (0,0), (0,0) |
| 5 | 9 | (148,168), (0,0), (0,0) |
| 6 | 11 | (110232,117036), (−6480,−6480), (0,0), (0,0) |
| 7 | 15 | (12431616,13271680), (−633600,−675072), (0,0), (0,0) |

In every row, the scalar residuals vanish from s onward, and the chain then
reaches the zero vector. Section 3 proves the claimed recurrences for all n≥s.
For widths 4 through 7 the immediately preceding residual is nonzero, so the
listed starting index cannot be moved back one step for these coefficients.

## 5. Verification and limits

Run, from this directory:

```sh
python3 verify.py
python3 verify_independent.py
python3 -m unittest discover -s tests -v
sha256sum -c SHA256SUMS
```

The tests enumerate binary boards cell by cell, count each allowed pair directly,
and compare to the transfer model for widths 2 through 7 and heights up to
min(4,floor(16/w)). In particular, all 65,536 width-4 height-4 boards are checked.
The first four width-4 counts are E: 5,54,501,4133 and B: 13,103,805,6009.
This separate enumeration catches state-interpretation errors on small boards;
the bijection in Section 2 provides the general argument.

Other tests change recurrence coefficients, initial counts, claimed start indices,
and certificate contents. The verifier rejects each corrupted instance.

The second program, `verify_independent.py`, constructs a different matrix from
cell tuples, keeping all last-row patterns: it has 8, 16, 32, 64, 128 and 256
states for widths 2 through 7. It independently establishes the zero-vector
identities and the required transient output equalities, matches the attributed
initial counts, and checks 19 small boards by exhaustive cell enumeration. It
does not import the first program or consume its transition graph as evidence.

This proof is not formally checked in Lean or another proof assistant. It relies
on the stated interpretation, the written bijection and the correctness of the
integer computation. It proves the cited formulas; it does not claim their
recurrence orders are minimal, establish priority, or constitute an OEIS
editorial acceptance. Human review remains open.
