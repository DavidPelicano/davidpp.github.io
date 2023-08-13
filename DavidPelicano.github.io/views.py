from flask import request, redirect, url_for, session, Flask, Blueprint, render_template, jsonify
import sqlite3


views = Blueprint(__name__, "views")

@views.route("/")
def inicial():
    # Assuming you want a default username if not set in the session
    username = session.get('name', 'Guest')
    return render_template("home.html", name=username)

@views.route("/<username>")
def home(username):
    return render_template("index.html", name=username)

@views.route("/profile/<username>")
def profile(username):
    return render_template("index.html", name=username)

@views.route("/json")
def get_json():
    return jsonify({'name': 'david', 'age': 18})

@views.route("/go-to-home")
def go_to_home():
    return redirect(url_for("views.home"))


@views.route('/go-to-contact')
def go_to_contact():
    if session.get('name', 'Guest') == 'Guest':
        return redirect(url_for('views.login'))
    return redirect(url_for("views.contact"))

@views.route('/biografhy')
def biografhy():
    return render_template("david.html")

@views.route('/redes')
def redes():
    return render_template("redes.html")


@views.route('/set_phone/<username>', methods=['POST'])
def set_phone(username):
    phone_number = request.form.get('phone')
    
    if not phone_number.isdigit() or len(phone_number) != 9 or not phone_number.startswith('9'):
        return redirect(url_for('views.contact', username=username))

    session[username] = phone_number
    return redirect(url_for('views.contact', username=username))



@views.route('/set_name', methods=['POST'])
def set_name():
    name = request.form.get('name')
    # Update the username in the session
    session['name'] = name
    return redirect(url_for('views.home', username=name))




def username_is_valid(username, password):
    # Check if the username is not empty
    if not username:
        return False

    # Check if the password meets the minimum length requirement
    min_password_length = 6
    if len(password) < min_password_length:
        return False

    # If both checks pass, the username and password are considered valid
    return True





@views.route("/logout", methods=['GET', 'POST'])
def logout():
    # Remover o nome do usuário da sessão para indicar que o usuário está desconectado
    session.pop('name', None)
    return redirect(url_for('views.login'))


@views.route("/naodeuLogin")
def naodeuLogin():
    return redirect(url_for('views.login'))


@views.route("/contact")
def contact():
    if 'name' not in session:
        return redirect(url_for('views.login'))  # Redirecionar para a página de registro
    username = session['name']
    phone_number = session.get(username)
    return render_template("contacto.html", name=username, phone_number=phone_number)

@views.route("/services")
def services():
    if 'name' not in session:
        return redirect(url_for('views.login'))  # Redirecionar para a página de registro
    username = session['name']
    return render_template("services.html", name=username)

@views.route("/about")
def about():
    if 'name' not in session:
        return redirect(url_for('views.login'))  # Redirect to the registration page
    username = session['name']
    return render_template("about.html", name=username)


def initialize_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Function to insert a new user into the database
def insert_user(name, email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, password))
    conn.commit()
    conn.close()

# Function to check if a user with the given email already exists in the database
def user_exists(email):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = c.fetchone()
    conn.close()
    return user is not None

initialize_database()

@views.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if not user_exists(email):
            insert_user(name, email, password)
            return render_template("fazLogin.html")
        else:
            error="User with this email already exists. Please try a different email."
            return render_template("register.html",error=error)

    return render_template('register.html')

def get_user_by_email(email):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = c.fetchone()
    conn.close()
    return user



@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = get_user_by_email(email)
        if user is not None and user[3] == password:
            session['name'] = user[1]  # Set the 'name' in the session upon successful login
            return redirect(url_for('views.home', username=user[1]))  # Redirect to the home page with the logged-in username
        else:
            error = "Invalid email or password. Please try again."
            return render_template("login.html", error=error)

    return render_template('login.html')

@views.route('/check_email')
def check_email():
    email = request.args.get('email')
    exists = user_exists(email)
    return jsonify({"exists": exists})

