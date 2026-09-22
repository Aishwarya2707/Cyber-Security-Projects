import base64
import time
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
# ==========================================
# AES FUNCTIONS
# ==========================================
def generate_aes_key():
    return AESGCM.generate_key(bit_length=256)
def aes_encrypt(message, key):
    aes = AESGCM(key)
 # Random 12-byte nonce
    nonce = os.urandom(12)

    encrypted = aes.encrypt(
        nonce,
        message.encode(),
        None
    )

    # Store nonce + encrypted data together
    result = nonce + encrypted

    return base64.b64encode(result).decode()


def aes_decrypt(encrypted_message, key):
    aes = AESGCM(key)

    data = base64.b64decode(encrypted_message)

    nonce = data[:12]
    ciphertext = data[12:]

    decrypted = aes.decrypt(
        nonce,
        ciphertext,
        None
    )

    return decrypted.decode()


# ==========================================
# RSA FUNCTIONS
# ==========================================

def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    return private_key, public_key


def rsa_encrypt(message, public_key):
    encrypted = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return base64.b64encode(encrypted).decode()


def rsa_decrypt(encrypted_message, private_key):
    encrypted = base64.b64decode(encrypted_message)

    decrypted = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted.decode()


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():

    print("======================================")
    print("      DATA ENCRYPTION TOOL")
    print("======================================")

    # Generate keys
    aes_key = generate_aes_key()
    rsa_private_key, rsa_public_key = generate_rsa_keys()

    while True:

        print("\n--------------------------------------")
        print("1. AES Encryption")
        print("2. AES Decryption")
        print("3. RSA Encryption")
        print("4. RSA Decryption")
        print("5. Compare AES and RSA")
        print("6. Exit")
        print("--------------------------------------")

        choice = input("Enter your choice: ")

        # =================================
        # AES ENCRYPTION
        # =================================

        if choice == "1":

            message = input("Enter message: ")

            start = time.perf_counter()

            encrypted = aes_encrypt(
                message,
                aes_key
            )

            end = time.perf_counter()

            print("\nAES Encrypted Data:")
            print(encrypted)

            print(
                f"\nEncryption time: "
                f"{end - start:.6f} seconds"
            )

        # =================================
        # AES DECRYPTION
        # =================================

        elif choice == "2":

            encrypted = input(
                "Enter AES encrypted data: "
            )

            try:

                decrypted = aes_decrypt(
                    encrypted,
                    aes_key
                )

                print("\nDecrypted Message:")
                print(decrypted)

            except Exception:

                print(
                    "Decryption failed. "
                    "Make sure the encrypted data "
                    "was generated during this run."
                )

        # =================================
        # RSA ENCRYPTION
        # =================================

        elif choice == "3":

            message = input("Enter message: ")

            # RSA-2048 OAEP can only encrypt
            # relatively small messages directly.
            if len(message.encode()) > 190:

                print(
                    "\nMessage is too long for direct "
                    "RSA-2048 encryption."
                )

                print(
                    "Use AES for large messages/files."
                )

                continue

            start = time.perf_counter()

            encrypted = rsa_encrypt(
                message,
                rsa_public_key
            )

            end = time.perf_counter()

            print("\nRSA Encrypted Data:")
            print(encrypted)

            print(
                f"\nEncryption time: "
                f"{end - start:.6f} seconds"
            )

        # =================================
        # RSA DECRYPTION
        # =================================

        elif choice == "4":

            encrypted = input(
                "Enter RSA encrypted data: "
            )

            try:

                decrypted = rsa_decrypt(
                    encrypted,
                    rsa_private_key
                )

                print("\nDecrypted Message:")
                print(decrypted)

            except Exception:

                print(
                    "RSA decryption failed."
                )

        # =================================
        # COMPARISON
        # =================================

        elif choice == "5":

            message = input(
                "Enter a message for comparison: "
            )

            # AES test
            start = time.perf_counter()

            aes_result = aes_encrypt(
                message,
                aes_key
            )

            aes_time = time.perf_counter() - start

            # RSA test
            if len(message.encode()) <= 190:

                start = time.perf_counter()

                rsa_result = rsa_encrypt(
                    message,
                    rsa_public_key
                )

                rsa_time = time.perf_counter() - start

                print("\n========== COMPARISON ==========")

                print(
                    f"AES encryption time: "
                    f"{aes_time:.6f} seconds"
                )

                print(
                    f"RSA encryption time: "
                    f"{rsa_time:.6f} seconds"
                )

                print("\nGeneral observation:")

                if aes_time < rsa_time:
                    print("AES is faster for this test.")
                else:
                    print("RSA is faster for this test.")

                print(
                    "\nAES is normally preferred for "
                    "large amounts of data."
                )

                print(
                    "RSA is mainly used for keys, "
                    "small data, and digital signatures."
                )

            else:

                print(
                    "\nMessage is too large for direct "
                    "RSA-2048 encryption."
                )

                print(
                    f"AES encryption time: "
                    f"{aes_time:.6f} seconds"
                )

        # =================================
        # EXIT
        # =================================

        elif choice == "6":

            print("\nThank you for using the tool!")
            break

        else:

            print(
                "\nInvalid choice. "
                "Please select 1-6."
            )


if __name__ == "__main__":
    main()