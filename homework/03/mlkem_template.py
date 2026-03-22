import argparse
import subprocess

from cryptography.hazmat.primitives.kdf.hkdf import HKDF


def exchange(args):
    subprocess.run(["openssl"])


def decrypt(args):
    shared_secret = open(args.s, "rb").read()
    hkdf = HKDF()


def main():
    parser = argparse.ArgumentParser(description="ML-KEM key exchange and decryption")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ex_parser = subparsers.add_parser("exchange", help="encapsulate a shared secret")
    ex_parser.add_argument("-k", required=True, help="recipient's ML-KEM public key (PEM)")
    ex_parser.add_argument("-s", required=True, help="output file for shared secret")
    ex_parser.add_argument("-c", required=True, help="output file for ML-KEM capsule")

    dec_parser = subparsers.add_parser("decrypt", help="decrypt AES-GCM ciphertext")
    dec_parser.add_argument("-s", required=True, help="shared secret file")
    dec_parser.add_argument("-i", required=True, help="encrypted input file (IV + ciphertext)")
    dec_parser.add_argument("-o", required=True, help="decrypted output file")

    args = parser.parse_args()

    if args.command == "exchange":
        exchange(args)
    elif args.command == "decrypt":
        decrypt(args)


if __name__ == "__main__":
    main()
