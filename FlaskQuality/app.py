# Quality Assignment

import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET HERE'

# Message with dict for 'index.html'

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]

# # # # DATABASE # # # #


def get_db_connection():
    conn = sqlite3.connect('users.db')
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

# # # # ROUTING METHODS # # # #

# Home page, shows the posts from the DB.


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts, messages=messages)

# Create page, allows user 'POST' and 'GET' to access and publish their post, with 'POST'!


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
                flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            flash('Post created successfully')
        return redirect(url_for('index'))
    return render_template('create.html')
@app.route('/about/')
def about():
    return render_template('about.html')

# Edit page that allows users to edit an original post. This is appended to the post, and thus
# requires the post to exist by default


@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')

        elif not content:
            flash('Content is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

# Delete method which deletes from not only the webpage, but also the DB in the same session.


@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

# # # # USER MANAGEMENT # # # #


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

# # # # ADMIN METHODS # # # #


@app.route('/admin/login/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        admin = conn.execute(
            'SELECT * FROM admin WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if admin:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('admin_login.html')


@app.route('/admin/dashboard/')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    users = conn.execute('SELECT id, email FROM users').fetchall()
    conn.close()
    return render_template('admin_dashboard.html', users=users)


@app.route('/logout/')
def logout():
    session.clear()
    flash('You have been logged out!')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0, port = 80')
