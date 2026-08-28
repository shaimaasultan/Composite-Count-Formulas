"""
Back-tree of the K8 cell network, rooted at A.

Idea: put the input square A at the root and let the network's forcing relations grow the
tree. Because the eight border cells have only TWO degrees of freedom (A, D), the tree is
shallow by necessity:

    root  A                       (chosen square input)
      |-- I = 2k^2 - A            (forced by A alone: the companion)
      |-- D = d^2   (branch)      (the ONE remaining free choice)
             |-- F = 2k^2 - D     (forced by D alone)
             |-- C = A + D - k^2  \\
             |-- G = 3k^2 - A - D  |  (forced by A and D together)
             |-- B = 4k^2 - 2A - D |
             |-- H = 2A + D - 2k^2/

So the depth is 2: choose A (root), choose D (one branching level), everything else is
forced -- a direct picture of the 2-DOF coupling. Each leaf is a full grid; we score it by
the number of distinct perfect-square cells. Branches with a non-positive or repeated cell
are pruned. This VISUALISES the forcing; it does not out-search the O(n^2) pair method,
because after A and D there is nothing left to branch on.
"""
from math import isqrt


def is_sq(v):
    r = isqrt(v) if v >= 0 else -1
    return v >= 0 and r * r == v


def tag(v):
    r = isqrt(v) if v >= 0 else -1
    return f"{r}^2" if v >= 0 and r * r == v else f"{v}*"   # * = not a square


def d_candidates(k, both_square_only=True):
    """Free-knob choices D = d^2. If both_square_only, restrict to D whose companion
    2k^2 - D is also square (keeps F square) -- the productive branches."""
    two = 2 * k * k
    out = []
    d = 1
    while d * d < two:
        D = d * d
        if not both_square_only or is_sq(two - D):
            out.append(D)
        d += 1
    return out


def build_tree(k, A, both_square_only=True):
    """Return (root_dict, leaves) where each leaf is (score, grid-dict)."""
    e = k * k
    I = 2 * e - A                                   # forced by A alone
    root = {"A": A, "I": I, "branches": []}
    leaves = []
    for D in d_candidates(k, both_square_only):
        F = 2 * e - D
        C = A + D - e
        G = 3 * e - A - D
        B = 4 * e - 2 * A - D
        H = 2 * A + D - 2 * e
        grid = {"A": A, "B": B, "C": C, "D": D, "F": F, "G": G, "H": H, "I": I}
        if any(v <= 0 for v in grid.values()):
            continue                                # prune: non-positive cell
        if len(set(list(grid.values()) + [e])) != 9:
            continue                                # prune: repeated cell
        s = sum(is_sq(v) for v in grid.values())
        root["branches"].append((D, {"F": F, "C": C, "G": G, "B": B, "H": H}, s))
        leaves.append((s, grid))
    leaves.sort(key=lambda t: -t[0])
    return root, leaves


def print_tree(k, A, max_branches=6):
    root, leaves = build_tree(k, A)
    a = isqrt(A)
    print(f"root A = {a}^2 = {A}   (centre k={k}, k^2={k*k})")
    print(f"  |-- I = 2k^2-A = {tag(root['I'])}   [forced by A alone]")
    print(f"  |-- D branches (each forces F,C,G,B,H): {len(root['branches'])} valid")
    for D, forced, s in sorted(root["branches"], key=lambda t: -t[2])[:max_branches]:
        print(f"       |-- D = {isqrt(D)}^2   -> score {s}/8 border squares (=> {s+1}/9)")
        line = "   ".join(f"{n}={tag(v)}" for n, v in forced.items())
        print(f"       |       {line}")
    if leaves:
        s, g = leaves[0]
        print(f"\nbest leaf: {s}/8 (=> {s+1}/9)")
        for r in ("A B C", "D E F", "G H I"):
            row = "  ".join(tag(g[x]) if x != "E" else f"{k}^2" for x in r.split())
            print("   " + row)


if __name__ == "__main__":
    print_tree(425, 23 * 23)     # root at the 425 record's A = 373^2
    # print_tree(425, 205 * 205)     # root at the 425 record's A = 205^2
    # print_tree(5900, 4012 * 4012)     # root at the 5900 record's A = 4012^2
    # print_tree(5900, 8260 * 8260)     # root at the 5900 record's A = 8260^2
    # print_tree(5915, 3367 * 3367)     # root at the 5900 record's A = 4012^2
    # print_tree(5915, 7189 * 7189)     # root at the 5900 record's A = 8260^2
    # print_tree(5915, 8099 * 8099)     # root at the 5900 record's A = 8260^2
