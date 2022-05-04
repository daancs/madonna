from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('home', __name__)

@bp.route('/home')
@login_required
def home():
    # if g.user is None:
        # return redirect(url_for('auth.login'))
    # else:
        return render_template('home/home.html')
