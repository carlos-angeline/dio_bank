from http import HTTPStatus
from flask import Blueprint, request
from sqlalchemy import inspect
from src.app import User, db
from flask_jwt_extended import jwt_required, get_jwt_identity

app = Blueprint('user', __name__, url_prefix='/users')

def _create_user():
    data = request.json
    user = User(
        username=data['username'],
        password=data['password'],
        role_id=data['role_id']
        )
    db.session.add(user)
    db.session.commit()

#list users    
def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [
		{
            "id": result.id,
            "username": result.username,
            "role": {
				"id": result.role.id,
            	"name": result.role.name,
			},
		}
  for result in users
	]

#create user
@app.route('/', methods=['GET', 'POST'])
@jwt_required()
def list_or_create_user():
    # user_id = (get_jwt_identity())
    # user = db.get_or_404(User, user_id)
    
    # if user.role.name != 'admin':
    #     return {'message': 'User dont have acess!'}, HTTPStatus.FORBIDDEN

    if request.method == 'POST':
        _create_user()
        return {'message': 'User Created!'}, HTTPStatus.CREATED
    else:
        return {'users': _list_users()} 

#list user por id    
@app.route('/<int:user_id>')
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return {
		"id": user.id,
        "username": user.username,
	}
    
    
#update user por id    
@app.route('/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json
    
    # if 'username' in data:
    #     user.username = data['username']
    #     db.session.commit()
    
    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
            db.session.commit()
    
    return {
		"id": user.id,
        "username": user.username,
	}

#delete user id
@app.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    
    return {'message': f'User {user_id} deleted successfully'}, HTTPStatus.CREATED   