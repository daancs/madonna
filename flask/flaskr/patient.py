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
    study = find_study(key_id)
    study_info = study[0]

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

    return render_template('patient/patientview.html', result=result, patientColNames=patientColNames, casesColNames=casesColNames, cases_inf=cases_inf, study=study_info[0], study_col_names=study[1], survey_nmbr=study[2], survey_q=study[3], survey_ans=study[4])
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
                            request.form['zipcode'], key_id)
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
    query = """SELECT * FROM Patients 
                LEFT JOIN Cases ON patients.key_id=cases.patient 
                LEFT JOIN MedicalHistory ON patients.key_id=MedicalHistory.key_id
                WHERE Patients.key_id =(%s)"""
    cur.execute(query, (key_id,))
    conn.commit()

    global formColNames # Sets formColNames as a global variable for use in editPatient()
    formColNames = [desc[0] for desc in cur.description]

    return cur.fetchall()

def find_study(key_id):
    conn = db.get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query_study = """SELECT * FROM Studies WHERE Studies.patient=(%s)"""
    cur.execute(query_study, (key_id,))
    conn.commit()
    study_info = cur.fetchall()
    study_info = study_info[0]
    studynmbr = study_info[0]

    if studynmbr == 1:
        query = """ SELECT * FROM Study1 WHERE Study1.studyID=(%s) AND Study1.patient=(%s)"""
    elif studynmbr == 2:
        query = """SELECT * FROM Study2 WHERE Study2.studyID=(%s) AND Study2.patient=(%s)"""
    cur.execute(query,(studynmbr,study_info[1],))
    conn.commit()
    study_col_names = [desc[0] for desc in cur.description]

    survey = get_surveys(key_id, studynmbr)
    print(survey)
    survey = survey[0]

    return cur.fetchall(),study_col_names, survey[1], survey[3], survey[4]

def get_surveys(key_id, studynmbr):
    conn = db.get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = """ SELECT * FROM Surveys WHERE Surveys.study=(%s) AND Surveys.patient=(%s)"""
    cur.execute(query,(studynmbr,key_id,))
    conn.commit()
    return cur.fetchall()
