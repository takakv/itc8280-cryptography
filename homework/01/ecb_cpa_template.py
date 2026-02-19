def challenger(m0: bytes, m1: bytes) -> bytes | None:
    """Return an AES-256-ECB IND-CPA challenge.

    The challenger generates a 256-bit AES key, (crypto) randomly selects
    which of the two messages to encrypt, encrypts it with AES-ECB,
    and returns the ciphertext. If the IND-CPA game or AES functional
    requirements are unsatisfied, the challenger returns `None`.

    :param m0: adversary's first message
    :param m1: adversary's second message
    :returns: ``Enc(m0)`` or ``Enc(m1)``; ``None`` if aborted.
    """
    pass


def distinguisher() -> bool:
    """Win the AES-256-ECB IND-CPA game with advantage 1.

    The distinguisher does not have access to the encryption oracle.
    :returns: ``True`` if ``m1`` was encrypted, ``False`` otherwise.
    """
    pass


if __name__ == "__main__":
    distinguisher()
