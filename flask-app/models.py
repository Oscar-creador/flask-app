from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import ForeignKey, ForeignKeyConstraint

db = SQLAlchemy()



class Alumno(db.Model):

    __tablename__ = 'alumnos'
    matricula = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(25))
    telegram_id = db.Column(db.Integer)
    rfid = db.Column(db.String(30))
   


class Maestro(db.Model):
    __tablename__ = 'maestros'
    maestro_id = db.Column(db.Integer, primary_key=True)
    nombre_maestro = db.Column(db.String(40))
    rfid = db.Column(db.String(30))
    grupo = db.relationship('Grupo')


class Grupo(db.Model):
    __tablename__ = 'grupos'

    grupo_id = db.Column(db.String(12), primary_key=True)
    nombre_materia = db.Column(db.String(25))
    maestro_id = db.Column(db.Integer, primary_key=True)
    creditos = db.Column(db.String(30))
    """timeSlot = db.relationship('TimeSlot')"""
    __table_args__ = (ForeignKeyConstraint([maestro_id], [Maestro.maestro_id]),)

   

class Grupo_Alumno(db.Model):
    __tablename__ = 'grupoAlumnos'


    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.Integer)
    grupo_id = db.Column(db.String(12))


  


class Inasistencia(db.Model):
    __tablename__ = 'inasistencias'


    matricula = db.Column(db.Integer, primary_key=True)
    grupo_id = db.Column(db.String(12), primary_key=True)
    fecha_hora = db.Column(db.DateTime, primary_key=True)

    __table_args__ = (ForeignKeyConstraint([matricula], [Alumno.matricula]),ForeignKeyConstraint([grupo_id], [Grupo.grupo_id]),)

  


class TimeSlot(db.Model):
    __tablename__ = 'timeslots'


  
    dia = db.Column(db.Integer, primary_key=True)
    hora = db.Column(db.Integer, primary_key=True)
    grupo_id = db.Column(db.String(12), primary_key=True)
    grupo = db.relationship('Grupo')
    maestro_id = db.Column(db.Integer)

    __table_args__ = (ForeignKeyConstraint([grupo_id], [Grupo.grupo_id]),)



class ClasesActivas(db.Model):
    __tablename__ = 'clasesActivas'


    macAddress = db.Column(db.String(30), primary_key=True)
    grupo_id = db.Column(db.String(12))
    maestro_id = db.Column(db.Integer)
    activa = db.Column(db.Boolean)



    
class AlumnosClaseActiva(db.Model):
    __tablename__ = 'alumnosClaseActiva'


    macAddress = db.Column(db.String(30))
    matricula = db.Column(db.Integer, primary_key=True)
    claseActiva = db.relationship('ClasesActivas')

    __table_args__ = (ForeignKeyConstraint([macAddress], [ClasesActivas.macAddress]),)


   

     
