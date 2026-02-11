from lib02 import xor


def generate_meaningful_keys(messages: list[bytes], ct: bytes) -> list[bytes]:
    keys = []
    for msg in messages:
        keys.append(xor(ct, msg))

    return keys


def main():
    ciphertext = bytes.fromhex("4E6B06D677435E8B2F88D744821E")
    strings = ["Attack at dawn", "Attack at noon", "Do not attack!", "Give me kohuke"]

    messages = [m.encode() for m in strings]

    keys = generate_meaningful_keys(messages, ciphertext)
    for key in keys:
        print(key.hex().upper())


if __name__ == "__main__":
    main()
