from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required

bp = Blueprint('patient', __name__)

@bp.route('/patient')
def patient():
    return render_template('patient/patientview.html')