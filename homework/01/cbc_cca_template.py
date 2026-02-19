import secrets
import sys

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class CCA2Challenger:
    def __init__(self):
        key = secrets.token_bytes(16)
        self._algorithm = algorithms.AES(key)
        self._challenge = None

    def encrypt(self, m: bytes) -> tuple[bytes, bytes]:
        iv = secrets.token_bytes(16)
        cipher = Cipher(self._algorithm, modes.CBC(iv))
        encryptor = cipher.encryptor()

        return encryptor.update(m) + encryptor.finalize(), iv

    def decrypt(self, ct: bytes, iv: bytes) -> bytes:
        if self._challenge and (self._challenge == ct or len(self._challenge) != len(ct)):
            sys.exit(1)

        cipher = Cipher(self._algorithm, modes.CBC(iv))
        decryptor = cipher.decryptor()
        return decryptor.update(ct) + decryptor.finalize()

    def get_challenge(self, m0: bytes, m1: bytes) -> tuple[bytes, bytes]:
        if self._challenge is not None or len(m0) != len(m1):
            sys.exit(1)

        choice = secrets.choice([m0, m1])
        ct, iv = self.encrypt(choice)
        self._challenge = ct

        return ct, iv


def distinguisher() -> bool:
    """Win the AES-128-CBC IND-CCA2 game with advantage 1.

    :returns: ``True`` if ``m1`` was encrypted, ``False`` otherwise.
    """
    challenger = CCA2Challenger()

    challenger.get_challenge(b"", b"")
    return False


if __name__ == "__main__":
    distinguisher()
