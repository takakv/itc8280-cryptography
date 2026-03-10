import base64

from Crypto.Protocol import HPKE
from Crypto.PublicKey import ECC


def main():
    with open("pub.pem") as f:
        ephemeral = ECC.import_key(f.read())

    capsule = base64.b64decode(...)
    ct = base64.b64decode(...)

    decryptor = HPKE.new(receiver_key=ephemeral,
                         aead_id=HPKE.AEAD.AES128_GCM,
                         enc=capsule,
                         info="ITC8280 week 6".encode())
    print(decryptor.unseal(ct).decode())


if __name__ == "__main__":
    main()
