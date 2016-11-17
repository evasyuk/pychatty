import jwt

secret = "swordfish"


def encode_token(json_payload=None):
    if json_payload is None:
        raise StandardError("json_payload could not be None")

    return jwt.encode(json_payload, secret, algorithm='HS256')


def decode_token(encoded_payload=None):
    if encoded_payload is None:
        raise StandardError("json_payload could not be None")

    return jwt.decode(encoded_payload, secret, algorithms=['HS256'])
