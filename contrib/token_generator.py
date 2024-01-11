import secrets
import string

from accounts.models import token as token_model

def generate_token(length=50):
    characters = string.ascii_letters + string.digits
    token = ''
    # get already existing tokens
    existing_tokens = [t.token for t in token_model.objects.all()]

    # generate a token that doesn't already exist
    while token in existing_tokens or token == '':
        token = ''.join(secrets.choice(characters) for _ in range(length))
    return token

