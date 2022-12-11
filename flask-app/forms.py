from wtforms import Form
from wtforms import StringField, IntegerField


class FilterForm(Form):
	grupo = StringField('Grupo')
	matricula = IntegerField("Matricula")

class FilterFormm(Form):
	grupo = StringField('Grupo')