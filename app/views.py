from flask import render_template, url_for, request, session, redirect, flash
from app import app, mongo, lm
from .user import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os
from os.path import dirname, join
 

ALLOWED_EXTENSIONS = set(['bmp', 'png', 'jpg', 'jpeg', 'gif'])


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
		existing_user = mongo.db.users.find_one({'username': request.form['username']})

		if existing_user is None:
			hashed = generate_password_hash(request.form['pass'])

			mongo.db.users.insert({'username': request.form['username'],\
						  'password': hashed, \
						  'email': request.form['email'], \
						  'name': request.form['name'], \
						  'lastname': request.form['lastname'], \
						  'imgurl': '/static/uploads/avatar.gif',\
						  'desc': ''})

			return redirect(url_for('home'))

		return render_template('registrar_cuenta.html', title='Registrarse') #'<h1>ERROR!</h1>'#

	return render_template('registrar_cuenta.html', title='Registrarse',user_warning='user-repeat-warning')


@app.route('/login', methods=['GET'])
def login():
	return render_template('iniciar_sesion.html', title='Login')

@app.route('/logmein', methods=['POST'])
def logmein():
	users = mongo.db.users
	user = users.find_one({"username": request.form['username']})

	if (not user) or (not check_password_hash(user['password'], request.form['pass'])):
		return "<h1>Usuario o contraseña incorrecta!</h1>"
	
	act_user = User(user['username'],user['password'],user['email'],user['name'],user['lastname'],user['imgurl'],user['desc'])
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
	elif (user['username'] == current_user.username):
		return render_template('perfil.html',title="Mi perfil",user=user, edit='');

	return render_template('perfil.html',title="Ver perfil",user=user, edit='no-btn')


# Funcion para verificar que los archivos tienen la terminacion correcta
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/editarPerfil',methods=['POST', 'GET'])
@login_required
def editarPerfil():
	if request.method == 'POST':
		#Aqui manejaremos el upload de los avatares. 
		file = request.files['file']
		#Si se subio una imagen se modifica todo los campos pertinentes en la base de dato si no se deja de lado la img.
		if file and allowed_file(file.filename):
			user = mongo.db.users.find_one({"username": current_user.username})
			#Nombramos al archivo cargado con el username del usuario activo.
			filename = user['username'] + "_" + secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			img = "/static/uploads/" + filename
			#Modificamos los datos del usuario en la base de datos
			mongo.db.users.update({"username":current_user.username},\
								  {'$set': {'name': request.form['name'],\
								  		    'lastname': request.form['lastname'],\
								  		 	'desc': request.form['desc'],\
								  		 	'imgurl': img}\
								  })

		#Modificamos los datos del usuario en la base de datos
		mongo.db.users.update({"username":current_user.username},\
							  {'$set': {'name': request.form['name'],\
							  		    'lastname': request.form['lastname'],\
							  		 	'desc': request.form['desc']}\
							  })

		return redirect(url_for('perfil', userid=current_user.username))

	return render_template('modificar_perfil.html', title="Editar perfil", user = current_user)

@lm.user_loader
def load_user(username):
	users = mongo.db.users
	u = users.find_one({"username": username})
	if not u:
		return None
	return User(u['username'],u['password'],u['email'],u['name'],u['lastname'],u['imgurl'],u['desc'])




