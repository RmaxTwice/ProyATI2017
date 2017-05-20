from flask import render_template, url_for, request, session, redirect, flash
from app import app, mongo, lm
from .user import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash



@app.route('/')
def home():
	if current_user.is_authenticated :
		return render_template('index_autenticado.html',title="Welcome")

	return render_template('index.html', title='Home')

@app.route('/index')
@login_required
def index():
	return render_template('index_autenticado.html',title="Welcome")

@app.route('/register', methods=['POST', 'GET'])
def register():
	if request.method == 'POST':
		users = mongo.db.users
		existing_user = users.find_one({'username' : request.form['username']})

		if existing_user is None:
			hashed = generate_password_hash(request.form['pass'])

			users.insert({'username': request.form['username'],\
						  'password': hashed, \
						  'email': request.form['email'], \
						  'name': request.form['name'], \
						  'lastname': request.form['lastname'], \
						  'imgurl': 'avatar.gif'})

			return redirect(url_for('home'))

		return "<h1>That Username is already taken.</h1>"

	return render_template('registrar_cuenta.html', title='Registrarse')


@app.route('/login', methods=['GET'])
def login():
	return render_template('iniciar_sesion.html', title='Login')

@app.route('/logmein', methods=['POST'])
def logmein():
	users = mongo.db.users
	user = users.find_one({"username": request.form['username']})

	if (not user) or (not check_password_hash(user['password'], request.form['pass'])):
		return "<h1>Usuario o contraseña incorrecta!</h1>"
	
	act_user = User(user['username'],user['password'],user['email'],user['name'],user['lastname'],user['imgurl'])
	login_user(act_user)

	return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('home'))
	
@app.route('/perfil/<userid>')
@login_required
def perfil(userid):
	user = mongo.db.users.find_one({"username":userid})        
	if user == None:
		return redirect(url_for('index'))
	return render_template('perfil.html',user=user)


@lm.user_loader
def load_user(username):
	users = mongo.db.users
	u = users.find_one({"username": username})
	if not u:
		return None
	return User(u['username'],u['password'],u['email'],u['name'],u['lastname'],u['imgurl'])




