import firebase_admin
from firebase_admin import credentials
from src.config.config import get_settings

SETTINGS = get_settings()

# Initialize Firebase Admin SDK
def initialize_firebase_admin():
    credentials_obj = {
        "type": SETTINGS.FIREBASE_TYPE,
        "project_id": SETTINGS.FIREBASE_PROJECT_ID,
        "private_key_id": SETTINGS.FIREBASE_PRIVATE_KEY_ID,
        "private_key": SETTINGS.FIREBASE_PRIVATE_KEY.replace(r'\n', '\n'),
        "client_email": SETTINGS.FIREBASE_CLIENT_EMAIL,
        "client_id": SETTINGS.FIREBASE_CLIENT_ID,
        "auth_uri": SETTINGS.FIREBASE_AUTH_URI,
        "token_uri": SETTINGS.FIREBASE_TOKEN_URI,
        "auth_provider_x509_cert_url": SETTINGS.FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
        "client_x509_cert_url": SETTINGS.FIREBASE_CLIENT_X509_CERT_URL,
    }

    cred = credentials.Certificate(credentials_obj)

    firebase_admin.initialize_app(cred)