from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import psycopg2.extras

bp = Blueprint('blog', __name__)

def get_post(id, check_author=True):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """SELECT posts.id, title, body, created, author_id, username
        FROM posts JOIN users ON posts.author_id = users.id
        WHERE posts.id = %s""",
        (id,)
    )
    post = cur.fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    
    return post

@bp.route('/', methods=('GET', 'POST'))
def index():
    session.clear()

    return redirect(url_for('blog.login'))
    # conn = get_db()
    # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # cur.execute(
    #     """SELECT posts.id, title, body, created, author_id, username
    #      FROM posts JOIN users  ON posts.author_id = users.id
    #      ORDER BY created DESC"""
    # )
    # posts = cur.fetchall()

@bp.route('/img', methods=('GET', 'POST'))
def img():
    if g.user is None:
        return redirect(url_for('blog.login'))
    else:
        return redirect(url_for('blog.home'))

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        session.clear()
        session['user_id'] = "tjo"
        return redirect(url_for('blog.home'))
        #return render_template('home/start.html')
    # conn = get_db()
    # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # cur.execute(
    #     """SELECT posts.id, title, body, created, author_id, username
    #      FROM posts JOIN users  ON posts.author_id = users.id
    #      ORDER BY created DESC"""
    # )
    # posts = cur.fetchall()
    return render_template('login.html')

@bp.route('/home')
@login_required
def home():
    return render_template('home/start.html')

@bp.route('/search')
@login_required
def search():
    return render_template('search/search.html')

@bp.route('/studies')
@login_required
def studies():
    return render_template('study/studies.html')

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)

        else:
            conn = get_db()
            cur = conn.cursor()

            query = "INSERT INTO posts (title, body, author_id) VALUES (%s,%s,%s)"
            cur.execute(query, (title, body, g.user['id']))
            conn.commit()

            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is requiered.'

        if error is not None:
            flash(error)
        else:
            conn = get_db()
            cur = conn.cursor()
            query = "UPDATE posts SET title = %s, body = %s WHERE id = %s"
            cur.execute(query,(title, body, id))

            conn.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM posts WHERE id = %s', (id,))
    conn.commit()
    return redirect(url_for('blog.index'))