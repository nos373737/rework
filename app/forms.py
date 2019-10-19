from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.forms import DynamicForm
from wtforms import StringField
from wtforms.validators import DataRequired


class OperatorForm(DynamicForm):
    
    cable_barcode = StringField(
        ("Cable Barcode"), description=("Field for scaning barcode"), widget=BS3TextFieldWidget()
    )