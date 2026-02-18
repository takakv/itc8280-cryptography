import secrets

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


def main():
    key = ChaCha20Poly1305.generate_key()
    aead = ChaCha20Poly1305(key)
    nonce = secrets.token_bytes(12)

    word1 = "..."
    word2 = "..."

    assert len(word1) == len(word2)
    assert word1 != word2

    for word in [word1, word2]:
        ciphertext = aead.encrypt(nonce, word.encode(), None)
        print(ciphertext.hex())


if __name__ == "__main__":
    main()
