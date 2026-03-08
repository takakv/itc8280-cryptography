import json
from typing import Literal

import requests


# Helper function. You do not necessarily need to use it.
def ilog2(n: int) -> int:
    """Calculate the integer logarithm log2(n).

    E.g. ilog2(8) = 3 since 2^3 = 8, ilog2(10) = 3, since 2^3 <= 10 < 2^4.
    """
    return n.bit_length() - 1


# Helper function. You do not necessarily need to use it.
def is_even(n: int) -> bool:
    return n % 2 == 0


def get_leaf_hash(data: bytes) -> bytes:
    pass


def get_internal_hash(left: bytes, right: bytes) -> bytes:
    pass


def build_merkle_tree(leaves: list[bytes]) -> tuple[bytes, list[list[bytes]]]:
    pass


def get_merkle_proof(
        tree: list[list[bytes]],
        leaf_index: int
) -> list[tuple[Literal["left", "right"], bytes]]:
    """Return an inclusion proof as a list of (position, hash) pairs.

    E.g. for a tree `[[l1, l2, l3, l4], [x1, x2], [root]]` and leaf index 2 (l3),
    the inclusion proof is `[["right", l4], ["left", x1]]`.

    :param tree: the full Merkle tree
    :param leaf_index: the leaf index (0-indexed)
    :return: the needed nodes as a list of (position, hash) pairs
    """
    # Example:
    # proof = []
    # proof.append(["right", hashes[i]])
    pass


# You do not need to implement this function, although I strongly
# recommend that you verify your inclusion proof to check your work.
def verify_merkle_proof(
        leaf_hash: bytes,
        proof: list[tuple[Literal["left", "right"], bytes]],
        expected_root: bytes
) -> bool:
    """Verify an inclusion proof.

    :param leaf_hash: the leaf hash the proof is for
    :param proof: the proof as a list of (position, hash) pairs
    :param expected_root: the expected root hash
    :return: True if the proof verifies, False otherwise
    """
    pass


def save_proof(
        data: str,
        leaf_id: int,
        leaf_hash: bytes,
        proof: list[tuple[Literal["left", "right"], bytes]],
        root_hash: bytes,
        path: str = "proof.json",
) -> None:
    proof_json = {
        "index": leaf_id,
        "data": data,
        "leaf_hash": leaf_hash.hex(),
        "proof": [{"position": pos, "hash": h.hex()} for pos, h in proof],
        "root": root_hash.hex(),
    }
    with open(path, "w") as f:
        json.dump(proof_json, f, indent=2)


def main():
    data = ""

    leaf_id = 1
    leaf_index = leaf_id - 1  # List indices start at 0.

    domain = "https://ahel.kastike.ee"
    leaves_url = f"{domain}/entries"
    root_url = f"{domain}/tree/head"

    entries = requests.get(leaves_url).json()
    hashes = [bytes.fromhex(e.get("leaf_hash")) for e in entries]
    leaf = hashes[leaf_index]

    # The recomputed leaf should match the leaf in the tree
    assert leaf == get_leaf_hash(data.encode())

    print("Leaf id:", leaf_id)
    print("Leaf hash:", leaf.hex())
    print()

    current_root_resp = requests.get(root_url).json()
    current_root = bytes.fromhex(current_root_resp["root_hash"])
    leaf_count: int = current_root_resp["num_leaves"]

    print("Current root:", current_root.hex(), f"(perfect: {current_root_resp['is_perfect']})")
    print("Leaf count:", leaf_count)
    print("Level count:", ilog2(leaf_count))
    print()

    root, tree = build_merkle_tree(hashes)
    # The rebuilt tree root should match the returned root
    assert current_root == root

    # The lowest level of the tree should contain all leaves
    assert len(tree[0]) == leaf_count

    proof = get_merkle_proof(tree, leaf_index)
    verify_result = verify_merkle_proof(leaf, proof, root)

    print("Merkle proof verified:", verify_result)

    save_proof(data, leaf_id, leaf, proof, root)


if __name__ == "__main__":
    main()
