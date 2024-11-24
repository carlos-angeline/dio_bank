from http import HTTPStatus
from flask import Blueprint, request
from src.app import User, db

app = Blueprint('user', __name__, url_prefix='/users')

def _create_user():
    data = request.json
    user = User(username=data['username'])
    db.session.add(user)
    db.session.commit()
    
def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [
		{
            "id": result.id,
            "username": result.username,
		}
  for result in users
	]

@app.route('/', methods=['GET', 'POST'])
def handle_user():
    if request.method == 'POST':
        _create_user()
        return {'message': 'User Created!'}, HTTPStatus.CREATED
    else:
        return {'users': _list_users()} 
    
    