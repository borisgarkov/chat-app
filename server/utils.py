from flask import make_response
from flask import request, jsonify

import jwt


def get_not_authorized_response():
    return make_response(
        'Could not verify',
        401,
        {'WWW-Authenticate': 'Basic realm="Login required!"'}
    )


