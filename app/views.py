import calendar
import barcode

from flask import flash, render_template, redirect, url_for, request
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
from .widgets import MyFormWidget, MyShowWidget, MyReFormWidget
from escpos.printer import Usb



from . import appbuilder, db
from .models import PSA, Error, ErrorGroup, Rework, PartNumber, DefectPlace, DefectPosition, BrigadeNum, StatusEnum, Employee, EmployeeGroupEnum, OperatorZone, Out, Test

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
    list_columns = ["description", "timesheet_number"]
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
    list_columns = ["description", "symbol_code"]
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
 
class ReworkYellowModelView(ModelView):
    datamodel = SQLAInterface(Rework)
    base_permissions = ['can_list', 'can_show']
    list_title = 'List of cable that already repair by operators'
    list_columns = ["id", "psa", "part_number", "brigade_num", "defect_position", "defect_place", "error_str", "red_ticket_date", "employee_rework.description" ]
    base_order = ("id", "asc")
    base_filters = [['status', FilterEqual, StatusEnum.yellow]]

class ReworkOutModelView(ModelView):
    datamodel = SQLAInterface(Rework)
    base_permissions = ['can_list', 'can_show']
    list_title = 'List of cable that dispatch to district master'
    list_columns = ["id", "psa", "part_number", "brigade_num", "defect_position", "defect_place", "error_str", "red_ticket_date", "employee_rework.description" ]
    base_order = ("id", "asc")
    base_filters = [['status', FilterEqual, StatusEnum.done]]

class ReworkModelView(ModelView):
    datamodel = SQLAInterface(Rework)
    list_columns = ["id", "psa", "part_number", "brigade_num", "defect_position", "defect_place", "error_str", "red_ticket_date", "employee_rework.description" ]
    add_form_query_rel_fields = {'employee_rework': [['group', FilterEqual, EmployeeGroupEnum.operator]]}
    base_order = ("id", "asc")
    base_filters = [['status', FilterEqual, StatusEnum.red]]
    list_title = 'List of cable that hit to rework'
    add_title = 'Add new cable on rework'
    show_title = 'Cable that added on rework'
    list_template = 'list_barcode.html'
    add_template = 'add_rework.html'
    show_template = 'my_show.html'
    add_widget = MyFormWidget
    show_widget = MyShowWidget

    show_fieldsets = [
        ("Summary", {"fields": ["id","psa", "part_number", "rework_created", "brigade_num", "defect_position", "defect_place", "error_str", "red_ticket_date", "employee_rework", "status" ]}),
    ]

    add_fieldsets = [
        ("Add New Rework", {"fields": ["psa", "part_number", "brigade_num", "defect_position", "defect_place", "error_str", "red_ticket_date", "employee_rework" ]}),
    ]

    # edit_fieldsets = [
    #     ("Edit Rework", {"fields": ["psa", "part_number", "red_ticket_date", "brigade_num", "defect_place"]}),
    # ]
    add_form_extra_fields = {
        'error_str':  QuerySelectMultipleField(
                            'List Error',
                            query_factory=all_errors,
                            widget=Select2ManyWidget()
                       )
    }

    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket")
    def muldelete(self, items):
        if isinstance(items, list):
            self.datamodel.delete_all(items)
            self.update_redirect()
        else:
            self.datamodel.delete(items)
        return redirect(self.get_redirect())

    def pre_add(self, item):
          item.error_str = ';'.join(str(x) for x in item.error_str)

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
    form_title = "Please scan the barcode of cable that you already repair"
    #message = "My rework id is: "
    
    def form_post(self, form):
        result = form.cable_barcode.data
        rework_to_change = db.session.query(Rework).get(int(result))
        rework_to_change.status = StatusEnum.yellow
        db.session.commit()
        #flash(self.message + " " + "{}".format(int(result)) + " " + str(rework_to_change), 'info')
        return redirect(url_for('OperatorZoneModelView.add', id = int(result)))

class OperatorZoneModelView(ModelView):
    datamodel = SQLAInterface(OperatorZone)
    list_title = 'List of cable that operator already repair on stand'
    add_title = 'Add cable after operator repair it on stand'
    show_title = 'Cable that operator already repair on stand'
    list_columns = ["rework", "error", "defect_position", "defect_cell", "operator"]
    list_template = 'list_barcode.html'
    message = "My operator select field is: "
    #add_form = OperatorAddForm
    add_template = 'add_after_rework.html'
    add_form_query_rel_fields = {'operator': [['group', FilterEqual, EmployeeGroupEnum.operator]]}
    add_fieldsets = [
        ("Add Cable after rework", {"fields": ["rework", "error", "defect_position", "defect_cell", "operator"]}),
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

    add_form_extra_fields = {
        'error':  QuerySelectMultipleField(
                            'List of errors',
                            query_factory=all_errors,
                            widget=Select2ManyWidget()
                       )
    }
        
    def pre_add(self, item):
          item.error = ';'.join(str(x) for x in item.error)

   
class BrigadeChiefFormView(ModelView):
    datamodel = SQLAInterface(Out)
    list_title = 'List of cable that go trew rework with done status'
    add_title = 'Add status "Done" to the cable'
    show_title = 'Cable that go threw rework process to the end'
    list_columns = ["cable_barcode", "brigade_chief", "done_date"]
    #list_template = 'list_barcode.html'
    message = "Rework id that go threw process is: "
    add_form_query_rel_fields = {'brigade_chief': [['group', FilterEqual, EmployeeGroupEnum.brigade_chief]]}
    add_fieldsets = [
        ("Add Cable after rework", {"fields": ["cable_barcode", "brigade_chief"]}),
    ]
    def post_add(self, item):
        result = item.cable_barcode
        rework_to_change = db.session.query(Rework).get(int(result))
        rework_to_change.status = StatusEnum.done
        db.session.commit()
        flash(self.message + " " + "{}".format(int(result)) + " " + str(rework_to_change), 'info')
        return redirect(url_for('ReworkModelView.list'))

class TestModelView(ModelView):
    datamodel = SQLAInterface(Test)
    list_columns = ["id", "cable_barcode", "rework", "employee", "error", "recycling_date"]
    list_title = 'List of re-rework cable'
    show_title = 'Cable that was re-rework'
    add_title = 'Add cable that going on rework again'
    add_template = 'add_rework.html'
    add_fieldsets = [("Add Cable on Re-rework", {"fields": ["cable_barcode", "rework", "employee", "error", "recycling_date"]})]
    add_form_extra_fields = {
        'error':  QuerySelectMultipleField(
                            'List of errors',
                            query_factory=all_errors,
                            widget=Select2ManyWidget()
                       )
    }
    add_widget = MyReFormWidget

    def pre_add(self, item):
          item.error = ';'.join(str(x) for x in item.error)

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
    ReworkYellowModelView,
    "Cable On Rework List",
    icon = "fa-envelope",
    category = "Rework" 
)
appbuilder.add_view(
    ReworkOutModelView,
    "Cable Done Rework List",
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
    "Operator Zone Model",
    icon="fa-group",
    label=("Operator Zone Model"),
    category="Operator Zone Model",
    category_icon="fa-cogs",
)

#appbuilder.add_view_no_menu(OperatorZoneModelView)

appbuilder.add_view(
    BrigadeChiefFormView,
    "Issuance to the district master",
    icon="fas fa-check-square",
    label=("Issuance to the district master"),
    category="Delivery/Re-Rework",
    category_icon="fa-calendar-check",
)

appbuilder.add_view(
    TestModelView, "Re-Rework", icon = "fas fa-check-square", category = "Delivery/Re-Rework" 
)

