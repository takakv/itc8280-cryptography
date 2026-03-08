import time

import requests


def l0_bits(bs: bytes) -> int:
    """Return the number of leading 0 bits.

    :param bs: the byte string
    :return: the number of leading 0 bits
    """
    pass


def bruteforce(seed: bytes, difficulty: int = 0) -> tuple[int, bytes]:
    """Find a 4-byte nonce such that the hash starts with >= x 0-bits.

    :param seed: the seed of the hash function
    :param difficulty: the minimum number of expected 0-bits
    :return: the suitable nonce and the corresponding SHA-512/256 hash
    """
    pass


def main():
    domain = "https://ahel.kastike.ee"
    leaf_url = f"{domain}/entries"

    data = ""
    uni_id = ""

    start = time.perf_counter()
    nonce, value = bruteforce(data.encode() + uni_id.encode(), 25)
    end = time.perf_counter()

    elapsed = end - start
    minutes, seconds = divmod(elapsed, 60)
    print(f"Time taken: {int(minutes)} minutes {seconds:.2f} seconds")

    post_payload = {
        "data": data,
        "student_id": uni_id,
        "nonce": nonce,
    }
    post_response = requests.post(leaf_url, json=post_payload)

    print("Status:", post_response.status_code)
    print("Response:", post_response.text)

    print()

    leaf_response = requests.get(f"{leaf_url}/{post_response.json().get('id')}")
    print("Leaf:", leaf_response.text)

    root_response = requests.get(f"{domain}/tree/head")
    print("Root:", root_response.text)


if __name__ == "__main__":
    main()
