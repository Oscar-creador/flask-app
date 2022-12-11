from flask import Flask, request
from flask import render_template
from datetime import datetime

from config import DevelopmentConfig
from models import db
from models import Alumno, Maestro, Grupo, Grupo_Alumno, Inasistencia, TimeSlot, ClasesActivas, AlumnosClaseActiva
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


"""AQUI EMPIEZA LO DEL BACKEND----------------------------------------------"""

@app.route('/recibirRequest',  methods=['GET', 'POST'])
def recibirRequest():
    args = request.args
    rfid = args.get("rfid")
    dia = args.get("dia")
    hora = args.get("hora")
    macAddress = args.get("mac")
    imgBase64 = args.get("img64")

    maestro = Maestro.query.filter_by(rfid=rfid).first()

    if maestro is not None:
        time_slot = TimeSlot.query.filter_by(dia=dia, hora=hora, maestro=maestro.maestro_id)
        if time_slot is not None:
            claseActiva = ClasesActivas.query.filter_by(macAddress = macAddress)
            if claseActiva is None:
                """abrir la tabla temporal de los alumnos (una lista o lo que sea) esa lista su llave deberia ser el grupo_id o la mac address de la esp."""
                claseActiva = ClasesActivas(macAddress=macAddress, maestro_id=maestro.maestro_id, activa=True)
                db.session.add(claseActiva)
                db.session.commit()
            else:
                grupo_alumnos = Grupo_Alumno.query.filter_by(grupo_id=time_slot.grupo_id)
                for alumno in grupo_alumnos:
                    alumnoClaseActiva = AlumnosClaseActiva.query.filter_by(matricula = alumno.matricula)
                    if alumnoClaseActiva is None:
                        datee = datetime.now()
                        falta = Inasistencia(matricula=alumno.matricula, grupo_id=time_slot.grupo_id, fecha_hora = datee)
                        db.session.add(falta)
                        db.session.commit()
                    else:
                        """borrar el registro del alumno en la tabla  AlumnosClaseActiva para no llenar la base de datos"""
                        AlumnosClaseActiva.query.filter_by(matricula=alumno.matricula).delete()
                        db.session.commit()
                """borrar el registro de la mac address en la tabla ClasesActivas"""   
                ClasesActivas.query.filter_by(macAddress=macAddress).delete()
                db.session.commit()

        else:
            "No tienes clase a esta hora profesor"  
    else:
        alumno = Alumno.query.filter_by(rfid=rfid).first()
        grupo_alumnos = Grupo_Alumno.query.filter_by(matricula=alumno.matricula)
        for grupo_alumno in grupo_alumnos:
            time_slot = TimeSlot.query.filter_by(dia=dia, hora=hora, grupo_id=grupo_alumno.grupo_id)
            if time_slot is not None:
                claseActiva = ClasesActivas.query.filter_by(macAddress = macAddress)
                if claseActiva is not None:
                    """convertir imgBase64 a imagen y enviar a telegramAlumno"""
                    telegramAlumno = alumno.telegram_id
                    """poner la asistencia temporal del alumno"""
                    alumnoClaseActiva = AlumnosClaseActiva(macAddress=macAddress, matricula=alumno.matricula)
                    db.session.add(alumnoClaseActiva)
                    db.session.commit()
            else:
                return "No tienes clases a esta hora alumno"
             
    return 200





