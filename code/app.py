import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort
import hashlib


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()

    print("resutat du post :", post)
    if post is None:
        abort(404)
    return post

def get_user(user_id) :
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM userdata WHERE id = ?',
                        (user_id,)).fetchone()
    conn.close()

    print("resutat du post :", user)
    if user is None:
        abort(404)
    return user



@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


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
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')



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

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))






#user crud 
@app.route('/usersList')
def usersList():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM userdata').fetchall()
    conn.close()
    return render_template('/user/userList.html', users=users)


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        if not username:
            flash('Title is username!')
        elif not password:
            flash('Content is password!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO userdata (username, password) VALUES (?, ?)',
                         (username, password))
            conn.commit()
            conn.close()

            print("insertion user")
            flash('User in the database!')
            return redirect(url_for('usersList'))
    return render_template('/user/registerForm.html')

@app.route('/<int:id>/editUser/', methods=('GET', 'POST'))
def editUser(id):
    user = get_user(id)

    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
 
        if not username:
            flash('username is required!')

        elif not password:
            flash('password is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE userdata SET username = ?, password = ?'
                         ' WHERE id = ?',
                         (username, password, id))
            conn.commit()
            conn.close()
            return redirect(url_for('usersList'))

    return render_template('/user/editUser.html', user=user)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)