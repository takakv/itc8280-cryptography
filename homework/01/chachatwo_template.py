import argparse
from typing import Set


def recover(c1: bytes, c2: bytes, candidates: Set[bytes]) -> tuple[str, str] | None:
    pass


def main():
    args = parse_args()

    try:
        authed_ct1 = bytes.fromhex(args.ct1)
        authed_ct2 = bytes.fromhex(args.ct2)
    except ValueError:
        raise SystemExit("Error: ciphertext arguments must be valid hex strings")

    # TODO: implement your solution

    result = recover(...)
    if result is None:
        print("[-] Failed to recover words")

    m1, m2 = result
    print(m1)
    print(m2)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recover ChaCha20-Poly1305 encrypted words"
    )

    parser.add_argument(
        "ct1",
        type=str,
        help="Authenticated ciphertext (hex string)"
    )
    parser.add_argument(
        "ct2",
        type=str,
        help="Another authenticated ciphertext (hex string)"
    )

    parser.add_argument(
        "-w", "--wordlist",
        type=str,
        default="wordlist.txt",
        help="Path to wordlist file (default: wordlist.txt)"
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
