from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.forms import DynamicForm
from wtforms import StringField 
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms.validators import DataRequired
from wtforms.fields import DateTimeField, DateField
from .models import Rework, OperatorZone, Error, DefectPosition, Employee
from . import db


class OperatorForm(DynamicForm):
    
    cable_barcode = StringField(
        ("Cable Barcode"), id="cable-barcode", description=("Field for scaning barcode"), widget=BS3TextFieldWidget())

class ReportForm(DynamicForm):
    start = DateTimeField(format='%Y-%m-%d', description = "Format of date is: YYYY-MM-DD")
    end = DateTimeField(format='%Y-%m-%d', description = "Format of date is: YYYY-MM-DD")

  

# def all_employee():
#     return db.session.query(Employee).all()

# class BrigadeChiefForm(DynamicForm):
    
#     cable_barcode = StringField(
#         ("Cable Barcode"), id="cable-barcode", description=("Field for scaning barcode"), widget=BS3TextFieldWidget())
#     brigade_chief = QuerySelectField(query_factory=all_employee, allow_blank=False)

def all_reworks():
    return db.session.query(Rework).all()

def all_errors():
    return db.session.query(Error).all()

def all_defects():
    return db.session.query(DefectPosition).all()    

class OperatorAddForm(DynamicForm):
    rework = QuerySelectField(query_factory=all_reworks, allow_blank=True)
    error_str = QuerySelectMultipleField(query_factory=all_errors, allow_blank=True)
    defect_position = QuerySelectField(query_factory=all_defects, allow_blank=True)
    defect_cell = StringField(
        ("Defects Cell"), description=("Field defects cell"), widget=BS3TextFieldWidget()
        )
    operator_rework_done  = DateTimeField(format='%Y-%m-%d %H:%M:%S')

    # def edit_rework(request, id):
    #     form = OperatorAddForm()
    #     form.rework.query = db.session.query(Rework).get(id)
