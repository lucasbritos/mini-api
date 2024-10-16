import json
import requests
import time
from jose import jwt
from errors import AuthorizationError
import settings

def validate_token(token):
    try:

        header = jwt.get_unverified_header(token)
        kid = header.get('kid')
        key = get_key_from_cache(kid)

        payload = validate_jwt(token, key)

        if payload.get("token_use") != "access":
            raise AuthorizationError(f"Invalid token use")

        return payload

    except Exception as e:
        raise AuthorizationError("Credentials error") from e




def get_key_from_cache(kid):
    current_time = time.time()
    # Check if the key is in the cache and if it's still valid
    if kid in cache and (current_time - cache[kid]['timestamp']) < CACHE_TTL:
        return cache[kid]
    else:
        # Call gather_jwks to refresh the cache
        jwks = gather_jwks()
        refresh_cache(jwks)

        # Check if the kid is now in the updated jwks
        if kid in cache:
            return cache[kid]
        else:
            raise Exception(f"kid {kid} not found in jwks")





cache = {}
CACHE_TTL = 60 * 60  # Time-to-live in seconds
# Global dictionary to cache values

def refresh_cache(jwks):
    # store in cache
    cache.clear() # clean cache, if kid is not present it is considered invalid
    for key in jwks["keys"]:
        cache[key["kid"]] = { "key": key, "timestamp":time.time() }
    return cache

def gather_jwks(
        use_local_jwks: bool = settings.USE_LOCAL_JWKS, 
        local_jwks: str = settings.LOCAL_JWKS,
        remote_jwks_endpoint: str =  settings.REMOTE_JWKS_ENDPOINT
        ) -> dict:
    if use_local_jwks:
        with open(local_jwks, 'r') as file:
            jwks = json.load(file)
    else:
        response = requests.get(remote_jwks_endpoint)
        response.raise_for_status()

        jwks = response.json()

    return jwks

def validate_jwt(token: str, key: str) -> dict:
    # Validate the token using key
    decoded_payload = jwt.decode(token, key, algorithms=['RS256'])
    return decoded_payload


def validate_header(auth_header):
    # Check if the header is present
    if not auth_header:
        raise AuthorizationError("Authorization header not present")

    # Check if it starts with "Bearer " and has a token following it
    parts = auth_header.split()

    if not (len(parts) == 2):
        raise AuthorizationError("Scheme error")
    
    scheme = parts[0].lower()
    credentials = parts[1]

    if not credentials:
        raise AuthorizationError("Credentials error")


    if scheme == "bearer":
        bearer_payload = validate_token(credentials)
        username = bearer_payload.get("username")
    else:
        raise AuthorizationError("Scheme not supported")

    return username