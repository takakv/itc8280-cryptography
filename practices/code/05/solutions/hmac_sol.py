import hmac
import secrets


def verify_tag(message: bytes, tag: bytes, key: bytes) -> bool:
    verif = hmac.digest(key, message, "sha256")
    return hmac.compare_digest(verif, tag)


def main():
    message = b"This is a message"
    fake_message = b"This is not a message"

    key = secrets.token_bytes(32)

    tag = hmac.digest(key, message, "sha256")

    print("Verify correct HMAC:", verify_tag(message, tag, key))
    print("Verify invalid HMAC:", verify_tag(fake_message, tag, key))


if __name__ == "__main__":
    main()
