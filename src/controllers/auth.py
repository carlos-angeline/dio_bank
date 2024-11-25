from http import HTTPStatus
from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from src.models import db

app = Blueprint('auth', __name__, url_prefix='/auth')

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    if username != "test" or password != "test":
        return {"message": "Bad username or password"}, HTTPStatus.UNAUTHORIZED
    
    # user = db.select(User).where(User.username == username)
    
    # if not user or user.password != password:

    access_token = create_access_token(identity=username)
    return {"access_token": access_token}
