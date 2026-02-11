import secrets

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms


def main():
    with open("plaintext.txt", "rb") as f:
        pt = f.read()

    key = secrets.token_bytes(32)
    nonce = secrets.token_bytes(8)

    # The current ChaCha20 standard is https://datatracker.ietf.org/doc/html/rfc8439
    # The previous standard is still often referred to: https://datatracker.ietf.org/doc/html/rfc7539
    # Both differ from Bernstein's original ChaCha20 ‘spec’ which used a 64-bit counter and nonce.
    # The RFC versions use a 32-bit counter and 96-bit nonce.
    # For both, the initial counter is often set to 0, (or to 1 for the ChaCha20-Poly1305 version).
    # NB! The counter is in little-endian (LSB), not big-endian (MSB).
    counter = 0

    # The pyca/crypto doc gives this example: full_nonce = struct.pack("<Q", counter) + nonce
    # struct.pack converts integers into bytestrings.
    # ‘<’ indicates little-endian (LSB) ordering, ‘Q’ a 64-bit (8 Byte) unsigned integer.
    # I think the following is simpler to understand, however:
    full_nonce = counter.to_bytes(8, byteorder="little") + nonce

    algorithm = algorithms.ChaCha20(key, full_nonce)
    cipher = Cipher(algorithm, mode=None)

    encryptor = cipher.encryptor()
    ct = encryptor.update(pt)

    print("Key:", key.hex())
    print("Nonce:", full_nonce.hex())

    with open("key.hex", "w") as f:
        f.write(f"{key.hex()}\n")

    with open("ciphertext.bin", "wb") as f:
        f.write(ct)


if __name__ == "__main__":
    main()
