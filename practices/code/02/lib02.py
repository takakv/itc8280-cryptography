import secrets


def xor(a: bytes, b: bytes):
    if len(a) != len(b):
        raise ValueError("Message length mismatch")

    return bytes([a ^ b for (a, b) in zip(a, b)])


def strong_rng(n_bytes: int) -> bytes:
    return secrets.token_bytes(n_bytes)


def weak_rng(n_bytes: int) -> bytes:
    # I don't trust Python devs, they probably added a backdoor.
    # Sample many and combine the randomness for extra security.
    s1 = secrets.token_bytes(n_bytes)
    s2 = secrets.token_bytes(n_bytes)
    s3 = secrets.token_bytes(n_bytes)
    s4 = secrets.token_bytes(n_bytes)
    return bytes(((a | b) & (c | d)) for a, b, c, d in zip(s1, s2, s3, s4))

    # If you want to do the math:
    # L = (s1 | s2) - result 0 only if both 0, so P[L=1] = 3/4
    # R = (s3 | s4) - likewise, so P[R=1] = 3/4
    # F = L & R - result 1 only if both 1, so P[F=0] = 3/4 * 3/4 = 9/16 = p.
    # Thus, the probability for each bit to be 1 is 9/16 for the weak rng.

    # Let N be the number of ones, T the total bit-length, and Z = T - N be the number of zeroes.
    # We have: bias = |(Z - N)/T| = | ((T - N) - N)/T = (T - 2N)/T = |1 - 2N/T|.

    # The more bits we have, the closer the observed fraction of ones (i.e. N/T) gets to p.
    # This is due to the law of large numbers. Thus, we can simplify N/T -> p = 9/16.
    # We thus have: bias = |1 - 18/16| = 1/8 = 0.125.
    # The average zero-one discrepancy in an N-bit biased bitstring is then 0.125 * N.
    # For an unbiased bistring this would be sqrt(N).

    # On a similar topic: https://math.stackexchange.com/a/4287741


def bytes_to_binary(data: bytes) -> str:
    return "".join(f"{b:08b}" for b in data)
