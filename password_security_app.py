import sqlite3
import hashlib
import uuid
from flask import Flask, request

app = Flask(__name__)
db_name = 'examen_db.db'

@app.route('/')
def index():
    return 'Bienvenido al sitio web de autenticacion segura!'

@app.route('/signup', methods=['POST'])
def signup():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USERS_HASHED
                 (USERNAME  TEXT    PRIMARY KEY NOT NULL,
                  HASH      TEXT    NOT NULL,
                  SALT      TEXT    NOT NULL);''')
    conn.commit()
    try:
        username = request.form['username']
        password = request.form['password']

        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha256(salt.encode() + password.encode()).hexdigest()

        c.execute("INSERT INTO USERS_HASHED (USERNAME, HASH, SALT) "
                  "VALUES ('{0}', '{1}', '{2}')".format(username, hashed_password, salt))
        conn.commit()
        print(f'Usuario: {username}, Contraseña (raw): {password}, Hash: {hashed_password}, Salt: {salt}')
        return "registro exitoso"
    except sqlite3.IntegrityError:
        return "el usuario ya esta registrado."
    except Exception as e:
        return f"Error en el registro: {e}"
    finally:
        conn.close()

def verify_password(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    query = f"SELECT HASH, SALT FROM USERS_HASHED WHERE USERNAME = '{username}'"
    c.execute(query)
    record = c.fetchone()
    conn.close()

    if not record:
        return False

    stored_hash = record[0]
    stored_salt = record[1]

    hashed_input_password = hashlib.sha256(stored_salt.encode() + password.encode()).hexdigest()

    return hashed_input_password == stored_hash

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_password(username, password):
            return "inicio de sesion exitoso"
        else:
            return "Usuario o contraseña invalidos"
    return "Metodo invalido o acceso no autorizado"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7500, ssl_context='adhoc')
