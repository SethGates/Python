import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort, session

# DATABASE MANAGEMENT

app = Flask(__name__)
app.config['SECRET_KEY'] = 'NF$*SHB%FCJ*$^FN'

def get_db_connection():
    conn = sqlite3.connect('AlineFinancial.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

# ROUTING METHODS, REFERENCE /TEMPLATES

@app.route('/')
def index():
    return render_template('index.html')

# USER MANAGEMENT IN ROUTING

# # # # USER MANAGEMENT # # # #

# ADD FIRST, LAST NAME AND CREDIT CARD
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        if not username:
            flash('Username is required!')
        elif not password:
            flash('Password is required!')
        elif password != confirm_password:
            flash('Passwords do not match!')
        elif not email:
            flash('Email is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                         (username, password, email))
            conn.commit()
            conn.close()
            flash('Registration successful!')
            return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username:
            flash('Username is required!')
        elif not password:
            flash('Password is required!')
        else:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                                (username, password)).fetchone()
            conn.close()
            if user is None:
                flash('Invalid username or password!')
            else:
                session['username'] = username
                flash('Welcome, {}!'.format(username))
                return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout/')
def logout():
    session.clear()
    flash('You have been logged out!')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0, port = 80')

