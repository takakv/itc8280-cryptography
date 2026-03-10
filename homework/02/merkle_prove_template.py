import base64
import json
from dataclasses import dataclass
from pathlib import Path
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
    the inclusion proof is `[("right", l4), ("left", x1)]`.

    :param tree: the full Merkle tree
    :param leaf_index: the leaf index (0-indexed)
    :return: the needed nodes as a list of (position, hash) pairs
    """
    # Example:
    # proof = []
    # proof.append(("right", hashes[i]))
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


def main():
    data = ""

    leaf_id = 1
    leaf_index = leaf_id - 1  # List indices start at 0.

    domain = "https://ahel.kastike.ee"

    hashes = fetch_entries(domain)
    leaf = hashes[leaf_index]

    # The recomputed leaf should match the leaf in the tree
    assert leaf == get_leaf_hash(data.encode()), (
        f"Leaf {leaf_id} hash mismatch: expected {get_leaf_hash(data.encode()).hex()}, got {leaf.hex()}"
    )

    print("Leaf id  :", leaf_id)
    print("Leaf hash:", leaf.hex())
    print()

    head, leaf_count = fetch_tree_head(domain)

    print(f"Current root: {head.hash.hex()}")
    print(f"Leaf count  : {leaf_count}")
    print(f"Level count : {ilog2(leaf_count)}")
    print()

    root, tree = build_merkle_tree(hashes)

    # The rebuilt tree root should match the returned root
    assert head.hash == root, (
        f"Root mismatch: server returned {head.hash.hex()}, rebuilt {root.hex()}"
    )

    # The lowest level of the tree should contain all leaves
    assert len(tree[0]) == leaf_count, (
        f"Leaf count mismatch: expected {leaf_count}, got {len(tree[0])}"
    )

    proof = get_merkle_proof(tree, leaf_index)

    verified = verify_merkle_proof(leaf, proof, root)
    print("Merkle proof verified:", verified)

    save_proof(data, leaf_id, leaf, proof, head)


if __name__ == "__main__":
    main()


@dataclass
class TreeHead:
    hash: bytes
    signature: bytes
    timestamp: str

    def to_dict(self) -> dict:
        return {
            "hash": self.hash.hex(),
            "signature": base64.b64encode(self.signature).decode(),
            "timestamp": self.timestamp,
        }


def save_proof(
        data: str,
        leaf_id: int,
        leaf_hash: bytes,
        proof: list[tuple[Literal["left", "right"], bytes]],
        head: TreeHead,
        path: Path = Path("proof.json"),
) -> None:
    proof_doc = {
        "index": leaf_id,
        "data": data,
        "leaf_hash": leaf_hash.hex(),
        "proof": [{"position": pos, "hash": h.hex()} for pos, h in proof],
        "head": head.to_dict(),
    }
    path.write_text(json.dumps(proof_doc, indent=2), encoding="utf-8")


def fetch_entries(domain: str) -> list[bytes]:
    entries = requests.get(f"{domain}/entries")
    entries.raise_for_status()
    return [bytes.fromhex(e["leaf_hash"]) for e in entries.json()]


def fetch_tree_head(domain: str) -> tuple[TreeHead, int]:
    resp = requests.get(f"{domain}/tree/head")
    resp.raise_for_status()
    data = resp.json()
    head = TreeHead(
        hash=bytes.fromhex(data["root_hash"]),
        signature=bytes.fromhex(data["signature"]),
        timestamp=data["created_at"],
    )
    return head, data["num_leaves"]
