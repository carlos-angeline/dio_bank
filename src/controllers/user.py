from http import HTTPStatus
from flask import Blueprint, request
from src.app import User, db

app = Blueprint('user', __name__, url_prefix='/users')

def _create_user():
    data = request.json
    user = User(username=data['username'])
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
		}
  for result in users
	]

#create user
@app.route('/', methods=['GET', 'POST'])
def handle_user():
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
    
    
    