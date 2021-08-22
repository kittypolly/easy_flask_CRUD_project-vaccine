# --------- 모듈 --------- #

import os
from forms import Patient_addform, Patient_delform, Vaccine_addform
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = 'AOA'

# --------- 데이터 베이스 --------- #

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

# --------- 모델 --------- #

class Patient(db.Model):

    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String)
    vaccine = db.relationship('Vaccine', backref = 'patient', uselist=False)

    def __init__(self, patient_name):
        self.patient_name = patient_name

    def __repr__(self):
        if self.vaccine:
            return f"환자의 이름은 {self.patient_name} 입니다. 백신은 {self.vaccine.vaccine_name}"
        else:
            return f"환자의 이름은 {self.patient_name} 입니다. 백신은 아직 등록되지 않았습니다."

class Vaccine(db.Model):    
    
    __tablename__ = 'vaccines'

    id = db.Column(db.Integer, primary_key=True)
    vaccine_name = db.Column(db.String)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))


    def __init__(self, vaccine_name, patient_id):
        self.vaccine_name = vaccine_name
        self.patient_id = patient_id

    def __repr__(self):
        return f"{self.vaccine_name}"



# --------- 뷰와 폼 --------- #

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_patient', methods=['GET','POST'])
def add_patient():

    form = Patient_addform()

    if form.validate_on_submit():

        add_patient = form.Patient_add.data
        new_patient = Patient(add_patient)
        db.session.add(new_patient)
        db.session.commit()

        return redirect(url_for('list'))

    return render_template('add_patient.html', form=form)

@app.route('/list')
def list():

    patients = Patient.query.all()
    return render_template('list.html', patients=patients) 


@app.route('/delete', methods=['GET','POST'])
def delete():

    form = Patient_delform()

    if form.validate_on_submit():

        del_patient = form.Patient_del.data
        deleted_patient = Patient.query.get(del_patient)
        db.session.delete(deleted_patient)
        db.session.commit()
    
        return redirect(url_for('list'))

    return render_template('delete.html', form=form)

@app.route('/add_vaccine', methods=['GET','POST'])
def add_vaccine():

    form = Vaccine_addform()

    if form.validate_on_submit():

        add_vaccine = form.Vaccine_add.data
        rel_patient_id = form.Patient_id.data
        new_vaccine = Vaccine(add_vaccine, rel_patient_id)
        db.session.add(new_vaccine)
        db.session.commit()
    
        return redirect(url_for('list'))

    return render_template('add_vaccine.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)