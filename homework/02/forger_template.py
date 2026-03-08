import hashlib
import secrets

from naive_auth import Authenticator


# You do not have access to the key.
def secret_setup():
    key = secrets.token_bytes(16)
    authenticator = Authenticator(key)

    user_nonce = secrets.token_bytes(16)
    # MAC = SHA256(key||data)
    user_mac = hashlib.sha256(key + user_nonce).digest()
    # Log in as a valid user.
    authenticator.authenticate(user_nonce, user_mac)

    return authenticator, user_nonce, user_mac


def adversary(message: bytes, tag: bytes) -> tuple[bytes, bytes]:
    """Forge a MAC tag given a (message, tag) pair.

    :param message: a known message
    :param tag: a known and valid tag on the message
    :return: a forgery (message, tag)
    """
    pass


def main():
    authenticator, intercepted_nonce, intercepted_mac = secret_setup()

    print()
    print("Logging in with intercepted/replayed credentials")
    ok, msg = authenticator.authenticate(intercepted_nonce, intercepted_mac)
    print(msg)

    forged_nonce, forged_mac = adversary(intercepted_nonce, intercepted_mac)

    print()
    print("Logging in with forged credentials")
    ok, msg = authenticator.authenticate(forged_nonce, forged_mac)
    print(msg)


if __name__ == "__main__":
    main()
