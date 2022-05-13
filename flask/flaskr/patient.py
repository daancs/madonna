from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
import psycopg2, psycopg2.extras

from flaskr.auth import login_required
from . import db

bp = Blueprint('patient', __name__)

patientColNames = ['Key-ID', 'Personnummer', 'Namn', 'Ålder', 'Kön', 'Vikt', 'BMI', 'Nikotin', 'Avliden', 'Adress', 'Stad','Postnummer']
casesColNames = ['Case-ID', 'Patient', 'Komplikation', 'Granskad av', 'Granskningsdatum', 'Studie avslutad']

@bp.route('/patient/<key_id>', methods=['GET'])
def patient(key_id):

    result = getPatientData(key_id)
    print(result)

    # return "foo"

    # result = cur.fetchall()
    result = result[0]
    patient_inf = []
    cases_inf = []

    for i in range(len(result)):
        if i < len(patientColNames):
            patient_inf.append(result[i])
        else:
            cases_inf.append(result[i])

    return render_template('patient/patientview.html', result=result, patientColNames=patientColNames, casesColNames=casesColNames, cases_inf=cases_inf)
    # return render_template('patient/patientview.html', patient_inf=patient_inf, cases_inf=cases_inf, patient_col_names=patient_col_names, cases_col_names=cases_col_names)

@bp.route('/patient/<key_id>/edit', methods=['GET', 'POST'])
def editPatient(key_id):
    if request.method == 'POST':
        print(key_id)
        conn = db.get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = """ UPDATE Patients SET
                    idnr = %s,
                    name = %s,
                    age = %s,
                    gender = %s,
                    weight = %s,
                    bmi = %s,
                    nicotine = %s,
                    deceased = %s,
                    adress = %s,
                    city = %s,
                    zipcode = %s
                    WHERE key_id = %s
                """

        cur.execute(query, (request.form['idnr'], request.form['name'],
                            request.form['age'], request.form['gender'],
                            request.form['weight'], request.form['bmi'],
                            request.form['nicotine'], request.form['deceased'],
                            request.form['adress'], request.form['city'],
                            request.form['zipcode'], request.form['key_id'])
                    )

        conn.commit()
        return redirect(url_for('patient.patient', key_id=key_id))

    result = getPatientData(key_id)
    return render_template('patient/editPatient.html', result=result[0], formColNames=formColNames, patientColNames=patientColNames, casesColNames=casesColNames)

def exit():
    return redirect(url_for('guiQuery.index'))

def getPatientData(key_id):
    conn = db.get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECT * FROM Patients LEFT JOIN Cases ON patients.key_id=cases.patient WHERE Patients.key_id =(%s)"
    cur.execute(query, (key_id,))
    conn.commit()

    global formColNames # Sets formColNames as a global variable for use in editPatient()
    formColNames = [desc[0] for desc in cur.description]

    return cur.fetchall()
