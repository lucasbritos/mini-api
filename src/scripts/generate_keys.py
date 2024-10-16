import json
from scripts.scripts_utils import generate_rsa_keypair, generate_jwks


if __name__ == "__main__":
    # Generate the RSA keypair (private and public)
    private_pem, public_pem = generate_rsa_keypair()

    # Generate the JWKS
    jwks = generate_jwks(public_pem)

    # Save private key, public key, and JWKS in one block
    with open('private_key.pem', 'wb') as private_file, \
         open('public_key.pem', 'wb') as public_file, \
         open('jwks.json', 'w') as jwks_file:

        private_file.write(private_pem)
        public_file.write(public_pem)
        json.dump(jwks, jwks_file, indent=4)

    print("Private Key, Public Key, and JWKS saved.")
