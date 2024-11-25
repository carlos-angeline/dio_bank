from http import HTTPStatus
from flask import Blueprint, request
from sqlalchemy import inspect
from src.app import Role, db

app = Blueprint('role', __name__, url_prefix='/roles')

#create role
@app.route('/', methods=['POST'])
def create_role():
    data = request.json
    role = Role(name=data['name'])
    db.session.add(role)
    db.session.commit()
          
    return {'message': "role created!"}, HTTPStatus.CREATED 