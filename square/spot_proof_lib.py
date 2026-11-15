"""Name parser and row machine shared by the structure scripts. It shares no code with the builder or the verifier of the first method.
It reads a name, builds a row-by-row machine (state = last row and the number of qualifying pairs so far, capped)
and computes counts with exact integers."""
import json, re, sys, itertools, glob, os
WORDS = {"zero":0,"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10,"eleven":11,"twelve":12}
def parse(name):
    m = re.match(r"Number of\s+(n|\d+)\s*X\s*(n|\d+)\s+(binary|0\.\.(\d+)) arrays with some element plus some (.+?) adjacent neighbor totalling (\w+) (no more than once|not more than once|exactly once)\.?$", name)
    if not m: return None
    a, b, alpha, top, nb, tot, mode = m.groups()
    q = 2 if alpha == "binary" else int(top) + 1
    kinds = set()
    for w in re.split(r"[ ,]+", nb.replace(" or ", " ")):
        w = w.strip()
        if w == "horizontally": kinds.add("H")
        elif w == "vertically": kinds.add("V")
        elif w == "diagonally": kinds.add("D")
        elif w == "antidiagonally": kinds.add("A")
        elif w: return None
    if a == "n": k = int(b)                       # n rows, k columns
    else:                                         # k rows, n columns: transpose, which swaps H and V
        k = int(a); kinds = {{"H":"V","V":"H"}.get(x, x) for x in kinds}
    return dict(k=k, q=q, kinds=kinds, total=WORDS[tot], exact=(mode == "exactly once"))
