from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import binascii
import hashlib


from block4 import protect_data4
# Function to load keys from files
def load_keys():
    with open("private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )

    with open("public_key.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )

    return private_key, public_key
# Load keys from files



def protect_data3(hashcode_data):

                

                # Password to be hashed
                voted_party = str(hashcode_data)
                #print(voted_party)
                # Create a new SHA-512 hash object
                sha512_hash = hashlib.sha512()

                # Update the hash object with the password bytes
                sha512_hash.update(voted_party.encode('utf-8'))

                # Get the hexadecimal representation of the hashed password
                hashed_password = sha512_hash.hexdigest()

                # Print the hashed password
                print("SHA-512 Hashed Password:", hashed_password)
               # print(voted_details[0:3])


                print(hashed_password)

                loaded_private_key, loaded_public_key = load_keys()
                #message =hashed_password
                message =hashed_password.encode()  # Convert string to bytes

                # Encrypt using loaded public key
                ciphertext = loaded_public_key.encrypt(
                    message,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )

                # Decrypt using loaded private key
                plaintext = loaded_private_key.decrypt(
                    ciphertext,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )

                print("block 1 results are complete ", message.decode())



                ciphertext=protect_data4(ciphertext)




                return   ciphertext
                #print("Decrypted message:", plaintext.decode())