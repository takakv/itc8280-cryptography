import argparse

# tinyec may be used instead of fastecdsa. Adapt imports accordingly
from fastecdsa.curve import Curve
from fastecdsa.point import Point


def octets_to_point(octets: bytes, curve: Curve) -> Point:
    pass


def point_to_octets(point: Point) -> bytes:
    pass


def main(u_hex: str, v_hex: str, f_pk: str):
    u_new = ...
    v_new = ...

    print(point_to_octets(u_new).hex())
    print(point_to_octets(v_new).hex())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Token refresher")
    parser.add_argument("-u", required=True, help="first ciphertext component (hex-encoded EC point)")
    parser.add_argument("-v", required=True, help="second ciphertext component (hex-encoded EC point)")
    parser.add_argument("-k", required=True, help="PEM-encoded public key file")
    args = parser.parse_args()

    main(args.u, args.v, args.k)
