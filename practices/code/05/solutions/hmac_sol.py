import hmac
import secrets

KEY = secrets.token_bytes(16)


def verify(message: bytes, tag: bytes) -> bool:
    verif = hmac.digest(KEY, message, "sha256")
    return hmac.compare_digest(verif, tag)


def authenticate(message: bytes) -> bytes:
    return hmac.digest(KEY, message, "sha256")


def main():
    message = b"This is a message"
    fake_message = b"This is not a message"

    tag = authenticate(message)

    print("Verify correct HMAC:", verify(message, tag))
    print("Verify invalid HMAC:", verify(fake_message, tag))


if __name__ == "__main__":
    main()
