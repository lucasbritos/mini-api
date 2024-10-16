import sys
import os
from scripts.scripts_utils import generate_jwt

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_jwt.py <path_to_private_key.pem> <user>")
        sys.exit(1)

    private_key_path = sys.argv[1]
    username = sys.argv[2]

    if not os.path.exists(private_key_path):
        print(f"Error: The file '{private_key_path}' does not exist.")
        sys.exit(1)

    with open(private_key_path, 'r') as file:
        private_key_pem = file.read()

    token = generate_jwt(private_key_pem, username)
    
    if token:
        print(token)
