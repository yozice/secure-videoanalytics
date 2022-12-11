from functools import wraps

import jwt
from backend.models import Component
from config import Config
from flask import jsonify, make_response, request


# token decorator
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # pass jwt-token in headers
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:  # throw error if no token provided
            return make_response(jsonify({"message": "A valid token is missing!"}), 401)
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user = Component.query.filter_by(
                public_id=data["public_id"]
            ).first()
        except:
            return make_response(jsonify({"message": "Invalid token!"}), 401)

        return f(*args, **kwargs)

    return decorator
