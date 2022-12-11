from flask import Flask, request
from flask import render_template
from datetime import datetime

from config import DevelopmentConfig
from models import db
from models import Alumno, Maestro, Grupo, Grupo_Alumno, Inasistencia, TimeSlot
import forms

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)
 

@app.route('/',  methods=['GET', 'POST'])
def index():
    alumnos = None
    filterForm = forms.FilterForm(request.form)
    if  request.method == 'POST':
        grupo_id= filterForm.grupo.data
        matricula = filterForm.matricula.data
        if matricula is not None:
            alumno = Alumno.query.filter_by(matricula=matricula)
            return render_template('index.html', alumnos=alumno, form=filterForm)
        if grupo_id is not None:
            grupo_alumnos = Grupo_Alumno.query.filter_by(grupo_id=grupo_id)
            lista_alumnos = []
            for alumno in grupo_alumnos:
                alumno = Alumno.query.filter_by(matricula=alumno.matricula).first()
                lista_alumnos.append(alumno)
            return render_template('index.html', alumnos=lista_alumnos, form=filterForm)
    return render_template('index.html', alumnos=alumnos, form=filterForm)


@app.route('/graficaAlumnos',  methods=['GET', 'POST'])
def graficaAlumnos():
    filterFormm = forms.FilterFormm(request.form)
    if  request.method == 'POST':
        grupo_id= filterFormm.grupo.data
        if grupo_id is not None:
            inasistencias = Inasistencia.query.filter_by(grupo_id=grupo_id)
            lista_matriculas = list()
            print(type(inasistencias))
            for inasistencia in inasistencias:
                lista_matriculas.append(inasistencia.matricula)
            my_dict = {matricula:lista_matriculas.count(matricula) for matricula in lista_matriculas}
            print (my_dict) 
            labels = list()
            values = list()
            for key in my_dict:
                labels.append(key)
                values.append(my_dict[key])
            print(labels)
            print(values)
            return render_template('graficaAlumnos.html', form=filterFormm, labels=labels, values=values)
    return render_template('graficaAlumnos.html', form=filterFormm)


@app.route('/insertFalta',  methods=['GET', 'POST'])
def insertFalta():
    args = request.args
    grupo = args.get("grupo")
    matricula = int(args.get("matricula"))
    datee = datetime.now()
    print(grupo)
    print(matricula)
    print(datee)
    falta = Inasistencia(matricula=matricula, grupo_id=grupo, fecha_hora = datee)
    db.session.add(falta)
    db.session.commit()
    return "done"









if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port="5049")


