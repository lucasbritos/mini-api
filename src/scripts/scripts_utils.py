import json
import datetime
from jose import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from jwcrypto import jwk

def generate_jwt(private_key, username):
    # Define the JWT claims
    payload = {
        'iat': datetime.datetime.utcnow(),  # Issued at
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365),  # Expires in 1 year
        'sub': 'test-user',  # Add your subject here
        'token_use': 'access',
        'username': username
    }

    # Define the JWT headers with kid
    headers = {
        'kid': "test-kid"
    }

    # Generate the JWT
    jwt_token = jwt.encode(payload, private_key, algorithm='RS256', headers=headers)

    return jwt_token

# Function to generate private and public keys
def generate_rsa_keypair():
    # Generate an RSA private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Serialize private key to PEM format
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Get the public key from the private key
    public_key = private_key.public_key()

    # Serialize public key to PEM format
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem, public_pem

# Function to generate a JWKS from a public key
def generate_jwks(public_pem):
    public_key_jwk = jwk.JWK.from_pem(public_pem)

    public_key_jwk.kid = str("test-kid")
    # Create a JWKS (JSON Web Key Set)
    jwks = {
        "keys": [json.loads(public_key_jwk.export(private_key=False))]
    }

    return jwks