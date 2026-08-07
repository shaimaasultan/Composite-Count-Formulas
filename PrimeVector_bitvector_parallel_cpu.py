import os
import numpy as np
from concurrent.futures import ProcessPoolExecutor


def _row_blocks(n, block_size):
    """Split [0, n) into contiguous (start, end) pieces of size block_size
    (last piece may be shorter)."""
    bounds = []
    start = 0
    while start < n:
        end = min(start + block_size, n)
        bounds.append((start, end))
        start = end
    return bounds


def _square_worker(payload):
    """One row-block of the square-feedback formulas -> B1 indices."""
    kmax, s, e = payload
    k = np.arange(s + 1, e + 1, dtype=np.int64)
    idx = np.concatenate([6 * k * k - 2 * k, 6 * k * k + 2 * k])  # (6c-1)^2, (6c+1)^2
    return idx[(idx >= 1) & (idx <= kmax)]


def _pair_worker(payload):
    """One (a-block, b-block) tile of the same-branch/cross-branch formulas.
    Blocking both dimensions keeps peak memory at block_size^2 regardless
    of kmax, instead of the kmax*block_size a single row-shard would need."""
    kmax, a_s, a_e, b_s, b_e = payload
    a = np.arange(a_s + 1, a_e + 1, dtype=np.int64)[:, None]
    b = np.arange(b_s + 1, b_e + 1, dtype=np.int64)[None, :]

    def filt(x):
        x = x.ravel()
        return x[(x >= 1) & (x <= kmax)]

    j_b1 = np.concatenate([
        filt(6 * a * b + a + b),   # (6a+1)(6b+1) = 6j+1
        filt(6 * a * b - a - b),   # (6a-1)(6b-1) = 6j+1
    ])
    j_b5 = filt(6 * a * b + a - b)  # (6a-1)(6b+1) = 6j-1
    return j_b1, j_b5


def cpu_bitvector_prime_detector(kmax, block_size=2000, num_workers=None):
    """
    CPU-only counterpart to gpu_bitvector_prime_detector (no cupy/GPU
    required). Same pure bit/bool-flag design -- composites are marked by
    scattering True directly into boolean flag arrays at their algebraic
    backbone index, never building composite-value arrays:

      square feedback:      (6c-1)^2 = 6j+1, j = 6c^2 - 2c   -> B1
                             (6c+1)^2 = 6j+1, j = 6c^2 + 2c   -> B1
      same-branch feedback: (6a+1)(6b+1) = 6j+1, j = 6ab+a+b -> B1
                             (6a-1)(6b-1) = 6j+1, j = 6ab-a-b -> B1
      cross-branch feedback:(6a-1)(6b+1) = 6j-1, j = 6ab+a-b -> B5

    The GPU version shards this work across CUDA streams on one device;
    here the O(kmax^2) (a,b) work is tiled into block_size x block_size
    blocks and distributed across CPU worker processes (ProcessPoolExecutor)
    to use all cores, with peak memory per task bounded by block_size^2
    regardless of how large kmax gets.

    Runtime is dominated by the O(kmax^2) pairwise formulas -- expect this
    to be noticeably slower than the GPU version at large kmax (a rough
    reference point: kmax=10000 took ~3s with 8 workers on a typical
    desktop CPU; kmax=80000 is roughly 64x the pair count, so budget a
    couple of minutes).
    """
    if num_workers is None:
        num_workers = os.cpu_count() or 12

    composite_B1 = np.zeros(kmax + 1, dtype=bool)
    composite_B5 = np.zeros(kmax + 1, dtype=bool)

    row_blocks = _row_blocks(kmax, block_size)

    square_tasks = [(kmax, s, e) for (s, e) in row_blocks]
    pair_tasks = [
        (kmax, a_s, a_e, b_s, b_e)
        for (a_s, a_e) in row_blocks
        for (b_s, b_e) in row_blocks
    ]

    with ProcessPoolExecutor(max_workers=num_workers) as pool:
        for idx in pool.map(_square_worker, square_tasks):
            composite_B1[idx] = True
        for j_b1, j_b5 in pool.map(_pair_worker, pair_tasks):
            composite_B1[j_b1] = True
            composite_B5[j_b5] = True

    k = np.arange(1, kmax + 1, dtype=np.int64)
    B1 = 6 * k + 1
    B5 = 6 * k - 1
    prime_B1 = ~composite_B1[1:]
    prime_B5 = ~composite_B5[1:]

    return B1, B5, composite_B1[1:], composite_B5[1:], prime_B1, prime_B5


# Example (must be guarded by __main__ -- ProcessPoolExecutor re-imports
# this module in each worker process on Windows)
if __name__ == "__main__":
    B1, B5, comp_B1, comp_B5, prime_B1, prime_B5 = cpu_bitvector_prime_detector(80000)
    print("Primes B1:", B1[prime_B1])
    print("Primes B5:", B5[prime_B5])
    print(len(B1), len(B5))
