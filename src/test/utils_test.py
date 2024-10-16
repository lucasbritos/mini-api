import pytest
from app import app
from webtest import TestApp
from scripts.scripts_utils import generate_rsa_keypair, generate_jwks, generate_jwt



private_pem, public_pem = generate_rsa_keypair()
jwks = generate_jwks(public_pem)

@pytest.fixture(scope="session")
def test_app():
    mp = pytest.MonkeyPatch()
    mp.setattr("auth.gather_jwks", lambda: jwks)
    return TestApp(app)


@pytest.fixture(scope="session")
def get_valid_token():
    def _create_get_valid_token(username):
        token = generate_jwt(private_pem, username)  # Use the global private_pem
        return token

    return _create_get_valid_token
