import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

cred = credentials.Certificate("./fluent-webbing-257713-firebase-adminsdk-ks6cb-2dd1be74c4.json")
firebase_admin.initialize_app(cred)


def verifyIdToken(idToken):
    try:
        decoded_token = auth.verify_id_token(idToken)
        return decoded_token
    except:
        return None