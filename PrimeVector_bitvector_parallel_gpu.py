import cupy as cp


def _chunks(n, num_chunks):
    """Split [0, n) into up to num_chunks contiguous (start, end) pieces,
    as evenly sized as possible. Empty pieces (when num_chunks > n) are
    dropped rather than yielded as zero-length ranges."""
    base = n // num_chunks
    rem = n % num_chunks
    bounds = []
    start = 0
    for i in range(num_chunks):
        size = base + (1 if i < rem else 0)
        end = start + size
        if size > 0:
            bounds.append((start, end))
        start = end
    return bounds


def gpu_bitvector_prime_detector(kmax, num_streams=12):
    """
    Pure bit/bool-flag GPU composite detector. Composites are marked by
    scattering True directly into boolean flag arrays at their algebraic
    backbone index (no composite-value arrays, cp.unique, or cp.isin).

    Index derivations (j is the backbone index, i.e. B1(j)=6j+1, B5(j)=6j-1):
      square feedback:      (6c-1)^2 = 6j+1, j = 6c^2 - 2c   -> B1
                             (6c+1)^2 = 6j+1, j = 6c^2 + 2c   -> B1
      same-branch feedback: (6a+1)(6b+1) = 6j+1, j = 6ab+a+b -> B1
                             (6a-1)(6b-1) = 6j+1, j = 6ab-a-b -> B1
      cross-branch feedback:(6a-1)(6b+1) = 6j-1, j = 6ab+a-b -> B5

    The (a,b) work is sharded along 'a' into `num_streams` chunks, each
    dispatched on its own CUDA stream so the independent feedback
    computations run concurrently on the GPU instead of back-to-back.
    Concurrent writes into the same flags array are safe here because
    every write sets the identical constant (True) -- overlapping writes
    from different streams can never disagree on the value being stored.
    """
    k_full = cp.arange(1, kmax + 1, dtype=cp.int64)

    composite_B1 = cp.zeros(kmax + 1, dtype=cp.bool_)
    composite_B5 = cp.zeros(kmax + 1, dtype=cp.bool_)

    def mark(flags, idx):
        idx = idx.ravel()
        valid = (idx >= 1) & (idx <= kmax)
        flags[idx[valid]] = True

    streams = [cp.cuda.Stream(non_blocking=True) for _ in range(num_streams)]
    k_chunks = _chunks(kmax, num_streams)

    # --- 1. Square feedback -> B1, sharded over k -----------------------
    for i, (s, e) in enumerate(k_chunks):
        with streams[i % num_streams]:
            kc = k_full[s:e]
            mark(composite_B1, 6 * kc * kc - 2 * kc)   # (6c-1)^2
            mark(composite_B1, 6 * kc * kc + 2 * kc)   # (6c+1)^2

    # --- 2/3. Same-branch and cross-branch, sharded over 'a' ------------
    b_full = k_full[None, :]
    for i, (s, e) in enumerate(k_chunks):
        with streams[i % num_streams]:
            a_chunk = k_full[s:e][:, None]
            mark(composite_B1, 6 * a_chunk * b_full + a_chunk + b_full)  # (6a+1)(6b+1)
            mark(composite_B1, 6 * a_chunk * b_full - a_chunk - b_full)  # (6a-1)(6b-1)
            mark(composite_B5, 6 * a_chunk * b_full + a_chunk - b_full)  # (6a-1)(6b+1)

    cp.cuda.Device().synchronize()  # wait for all streams before reading results

    # --- Prime flags (bool, GPU-resident, no value arrays) --------------
    prime_B1 = ~composite_B1[1:]
    prime_B5 = ~composite_B5[1:]

    B1 = 6 * k_full + 1
    B5 = 6 * k_full - 1

    return B1, B5, composite_B1[1:], composite_B5[1:], prime_B1, prime_B5


# Example (host-side print)
if __name__ == "__main__":
    B1, B5, comp_B1, comp_B5, prime_B1, prime_B5 = gpu_bitvector_prime_detector(20000)
    print("Primes B1:", cp.asnumpy(B1[prime_B1]))
    print("Primes B5:", cp.asnumpy(B5[prime_B5]))
    print(len(B1), len(B5))
