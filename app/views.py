import calendar
import requests
import barcode

from flask import flash, render_template, redirect, url_for
from flask_appbuilder import SimpleFormView
from flask_appbuilder.baseviews import BaseFormView
from flask_appbuilder import ModelView, MasterDetailView, MultipleView
from flask_appbuilder.models.group import aggregate_count
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.sqla.filters import FilterEqual
from flask_appbuilder.fieldwidgets import Select2AJAXWidget, Select2ManyWidget, Select2Widget
from flask_appbuilder.fields import AJAXSelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from flask_appbuilder.actions import action
from .forms import OperatorForm, OperatorAddForm, all_errors
from .widgets import MyFormWidget, MyShowWidget
from escpos.printer import Usb



from . import appbuilder, db
from .models import PSA, Error, ErrorGroup, Rework, PartNumber, DefectPlace, DefectPosition, BrigadeNum, StatusEnum, Employee, EmployeeGroupEnum, OperatorZone

#views reworks
class PSAModelView(ModelView):
    datamodel = SQLAInterface(PSA)
    
    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket")
    def muldelete(self, items):
        if isinstance(items, list):
            self.datamodel.delete_all(items)
            self.update_redirect()
        else:
            self.datamodel.delete(items)
        return redirect(self.get_redirect())

class PartNumberModelView(ModelView):
    datamodel = SQLAInterface(PartNumber)

    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket")
    def muldelete(self, items):
        if isinstance(items, list):
            self.datamodel.delete_all(items)
            self.update_redirect()
        else:
            self.datamodel.delete(items)
        return redirect(self.get_redirect())

class BrigadeNumModelView(ModelView):
    datamodel = SQLAInterface(BrigadeNum)

    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket")
    def muldelete(self, items):
        if isinstance(items, list):
            self.datamodel.delete_all(items)
            self.update_redirect()
        else:
            self.datamodel.delete(items)
        return redirect(self.get_redirect())

class DefectPositionModelView(ModelView):
    datamodel = SQLAInterface(DefectPosition)

    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket")
    def muldelete(self, items):
        if isinstance(items, list):
            self.datamodel.delete_all(items)
            self.update_redirect()
        else:
            self.datamodel.delete(items)
        return redirect(self.get_redirect())

class DefectPlaceModelView(ModelView):
    datamodel = SQLAInterface(DefectPlace)

    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket")
    def muldelete(self, items):
        if isinstance(items, list):
            self.datamodel.delete_all(items)
            self.update_redirect()
        else:
            self.datamodel.delete(items)
        return redirect(self.get_redirect())

class EmployeeModelView(ModelView):
    datamodel = SQLAInterface(Employee)

    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket")
    def muldelete(self, items):
        if isinstance(items, list):
            self.datamodel.delete_all(items)
            self.update_redirect()
        else:
            self.datamodel.delete(items)
        return redirect(self.get_redirect())

class ErrorGroupModelView(ModelView):
    datamodel = SQLAInterface(ErrorGroup)

    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket")
    def muldelete(self, items):
        if isinstance(items, list):
            self.datamodel.delete_all(items)
            self.update_redirect()
        else:
            self.datamodel.delete(items)
        return redirect(self.get_redirect())

class ErrorModelView(ModelView):
    datamodel = SQLAInterface(Error)
    list_columns = ["description", "symbol_code", "error_group.description"]

    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket")
    def muldelete(self, items):
        if isinstance(items, list):
            self.datamodel.delete_all(items)
            self.update_redirect()
        else:
            self.datamodel.delete(items)
        return redirect(self.get_redirect())
    
# class ReworkErrorInItemModelView(ModelView):
#     datamodel = SQLAInterface(ReworkErrorInItem)
#     list_columns = ['error', 'defect_position', 'defect_cell']

# class ReworkErrorOutItemModelView(ModelView):
#     datamodel = SQLAInterface(ReworkErrorOutItem)
#     list_columns = ['error', 'defect_position', 'defect_cell']
 


class ReworkModelView(ModelView):
    datamodel = SQLAInterface(Rework)
    list_columns = ["id", "psa", "part_number", "brigade_num", "defect_position", "defect_place", "error", "red_ticket_date", "brigade_chief_name" ]
    add_form_query_rel_fields = {'brigade_chief_name': [['group', FilterEqual, EmployeeGroupEnum.operator]]}
    base_order = ("id", "asc")
    list_template = 'list_barcode.html'
    add_template = 'add_rework.html'
    show_template = 'my_show.html'
    add_widget = MyFormWidget
    show_widget = MyShowWidget

    show_fieldsets = [
        ("Summary", {"fields": ["id","psa", "part_number", "rework_created", "brigade_num", "defect_position", "defect_place", "error", "red_ticket_date", "brigade_chief_name", "status" ]}),
    ]

    add_fieldsets = [
        ("Add New Rework", {"fields": ["psa", "part_number", "brigade_num", "defect_position", "defect_place", "error", "red_ticket_date", "brigade_chief_name" ]}),
    ]

    # edit_fieldsets = [
    #     ("Edit Rework", {"fields": ["psa", "part_number", "red_ticket_date", "brigade_num", "defect_place"]}),
    # ]

    def post_add(self, item):
        stroka = str()
        len_id = len(str(item.id))
        const_len = 9
        while(len_id < const_len):
            stroka += '0'
            len_id += 1
        stroka += str(item.id)
        p = Usb(0x1d90,0x2060,0,0x81,0x02)
        p.barcode(stroka,'CODE39',250,3,'','')
        p.cut()
        p.barcode(stroka,'CODE39',250,3,'','')
        p.cut()

class OperatorFormView(SimpleFormView):
    form = OperatorForm
    form_template = 'operator.html'
    form_title = "Please scan barcode from cable"
    message = "My rework id is: "
    
    def form_post(self, form):
        result = form.cable_barcode.data
        rework_to_change = db.session.query(Rework).get(int(result))
        rework_to_change.status = StatusEnum.yellow
        db.session.commit()
        flash(self.message + " " + "{}".format(int(result)) + " " + str(rework_to_change), 'info')
        return redirect(url_for('OperatorZoneModelView.add', id = int(result)))

class OperatorZoneModelView(ModelView):
    datamodel = SQLAInterface(OperatorZone)
    list_columns = ["rework", "error", "defect_position", "defect_cell"]
    list_template = 'list_barcode.html'
    message = "My operator select field is: "
    add_form = OperatorAddForm
    add_template = 'add_after_rework.html'
    #add_form_query_rel_fields = {'rework': [['id', FilterEqual, [1,2,3]]]}
    add_fieldsets = [
        ("Add Cable after rework", {"fields": ["rework", "error", "defect_position", "defect_cell"]}),
    ]
    
    # add_form_extra_fields = {
    #     'error': AJAXSelectField(
    #                         'Error',
    #                         description='This will be populated with AJAX',
    #                         datamodel=datamodel,
    #                         col_name='error',
    #                         widget=Select2AJAXWidget(endpoint='/operatorzonemodelview/api/column/add/error')
    #                      ),
    # }

    # edit_form_extra_fields = {
    #     'error':  QuerySelectField(
    #                         'error',
    #                         query_factory=all_errors,
    #                         widget=Select2Widget()
    #                    )
    # }
        
    # def pre_add(self, item):
    #     result = get_redirect(self)
    #     flash(self.message + " " + "{}".format(result), 'info')

    # def form_get(self, form):
    #     flash(self.message + " " + "{}".format("Bitches"), 'info')

db.create_all()

@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template = appbuilder.base_template, appbuilder = appbuilder
        ),
        404,
    )


appbuilder.add_view(
    PSAModelView, "List PSA", icon = "fa-envelope", category = "Add/Edit Data" 
)

appbuilder.add_view(
    EmployeeModelView, "List Responsible Person", icon = "fa-envelope", category = "Add/Edit Data" 
)

appbuilder.add_view(
    DefectPositionModelView,
    "List Defect Position",
    icon = "fa-envelope",
    category = "Add/Edit Data", 
)

appbuilder.add_view(
    DefectPlaceModelView, "List Defect Place", icon = "fa-envelope", category = "Add/Edit Data" 
)

appbuilder.add_view(
    PartNumberModelView, "List PartNumber", icon = "fa-envelope", category = "Add/Edit Data" 
)
appbuilder.add_view(
    BrigadeNumModelView, 
    "List BrigadeNum",
    icon = "fa-envelope",
    category = "Add/Edit Data" 
)
appbuilder.add_view(
    ErrorGroupModelView, "List Error Group", icon = "fa-envelope", category = "Add/Edit Data" 
)

appbuilder.add_view(
    ErrorModelView, "List Error", icon = "fa-envelope", category = "Add/Edit Data" 
)

appbuilder.add_view(
    ReworkModelView,
    "Rework List",
    icon = "fa-envelope",
    category = "Rework" 
)

appbuilder.add_view(
    OperatorFormView,
    "Operator Zone",
    icon="fa-group",
    label=("Operator Zone"),
    category="Operator Zone",
    category_icon="fa-cogs",
)

appbuilder.add_view(
    OperatorZoneModelView,
    "Operator Zone with Error",
    icon="fa-group",
    label=("Operator Zone with Error"),
    category="Operator Zone with Error",
    category_icon="fa-rocket",
)

# appbuilder.add_view(
#     ReworkYellowModelView,
#     "Rework Yellow List",
#     icon = "fa-envelope",
#     category = "Rework" 
# )

# appbuilder.add_view_no_menu(ReworkErrorInItemModelView)

# appbuilder.add_view_no_menu(ReworkErrorOutItemModelView)


