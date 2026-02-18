import secrets

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


def main():
    key = ChaCha20Poly1305.generate_key()
    aead = ChaCha20Poly1305(key)
    nonce = secrets.token_bytes(12)

    words = ["...", "..."]
    assert all(len(word) == len(words[0]) for word in words)

    for word in words:
        ciphertext = aead.encrypt(nonce, word.encode(), None)
        print(ciphertext.hex())


if __name__ == "__main__":
    main()
