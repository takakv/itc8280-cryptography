def generate_meaningful_keys(messages: list[bytes], ct: bytes) -> list[bytes]:
    keys = []

    # TODO: implement the function here

    return keys


def main():
    ciphertext = bytes.fromhex("4E6B06D677435E8B2F88D744821E")
    strings = ["Attack at dawn", "Attack at noon", "Do not attack!", "Give me kohuke"]

    # TODO: call the key generation function, and print the keys


if __name__ == "__main__":
    main()
