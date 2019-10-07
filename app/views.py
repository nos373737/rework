import calendar

from flask_appbuilder import ModelView, MasterDetailView, MultipleView
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.sqla.filters import FilterEqual


from . import appbuilder, db
from .models import Contact, ContactGroup, Gender, PSA, Error, ErrorGroup, Rework, PartNumber, DefectPlace, DefectPosition, ReworkErrorInItem, BrigadeNum, StatusEnum, Operator, ReworkErrorOutItem


def fill_gender():
    try:
        db.session.add(Gender(name="Male"))
        db.session.add(Gender(name="Female"))
        db.session.commit()
    except Exception:
        db.session.rollback()


class ContactModelView(ModelView):
    datamodel = SQLAInterface(Contact)

    list_columns = ["name", "personal_celphone", "birthday", "contact_group.name"]

    base_order = ("name", "asc")

    show_fieldsets = [
        ("Summary", {"fields": ["name", "gender", "contact_group"]}),
        (
            "Personal Info",
            {
                "fields": [
                    "address",
                    "birthday",
                    "personal_phone",
                    "personal_celphone",
                ],
                "expanded": False,
            },
        ),
    ]

    add_fieldsets = [
        ("Summary", {"fields": ["name", "gender", "contact_group"]}),
        (
            "Personal Info",
            {
                "fields": [
                    "address",
                    "birthday",
                    "personal_phone",
                    "personal_celphone",
                ],
                "expanded": False,
            },
        ),
    ]

    edit_fieldsets = [
        ("Summary", {"fields": ["name", "gender", "contact_group"]}),
        (
            "Personal Info",
            {
                "fields": [
                    "address",
                    "birthday",
                    "personal_phone",
                    "personal_celphone",
                ],
                "expanded": False,
            },
        ),
    ]


class GroupModelView(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]


class ContactChartView(GroupByChartView):
    datamodel = SQLAInterface(Contact)
    chart_title = "Grouped contacts"
    label_columns = ContactModelView.label_columns
    chart_type = "PieChart"

    definitions = [
        {"group": "contact_group", "series": [(aggregate_count, "contact_group")]},
        {"group": "gender", "series": [(aggregate_count, "contact_group")]},
    ]


def pretty_month_year(value):
    return calendar.month_name[value.month] + " " + str(value.year)


def pretty_year(value):
    return str(value.year)


class ContactTimeChartView(GroupByChartView):
    datamodel = SQLAInterface(Contact)

    chart_title = "Grouped Birth contacts"
    chart_type = "AreaChart"
    label_columns = ContactModelView.label_columns
    definitions = [
        {
            "group": "month_year",
            "formatter": pretty_month_year,
            "series": [(aggregate_count, "group")],
        },
        {
            "group": "year",
            "formatter": pretty_year,
            "series": [(aggregate_count, "group")],
        },
    ]
#views reworks
class PSAModelView(ModelView):
    datamodel = SQLAInterface(PSA)
    list_columns = ["description"]

class PartNumberModelView(ModelView):
    datamodel = SQLAInterface(PartNumber)
    list_columns = ["description"]

class BrigadeNumModelView(ModelView):
    datamodel = SQLAInterface(BrigadeNum)
    list_columns = ["description"]

class DefectPositionModelView(ModelView):
    datamodel = SQLAInterface(DefectPosition)
    list_columns = ["description"]

class DefectPlaceModelView(ModelView):
    datamodel = SQLAInterface(DefectPlace)
    list_columns = ["description"]

class OperatorModelView(ModelView):
    datamodel = SQLAInterface(Operator)
    list_columns = ["description"]

class ErrorGroupModelView(ModelView):
    datamodel = SQLAInterface(ErrorGroup)
    list_columns = ["description", "symbol_code"]

class ErrorModelView(ModelView):
    datamodel = SQLAInterface(Error)
    list_columns = ["description", "symbol_code", "error_group.description"]
    
class ReworkErrorInItemModelView(ModelView):
    datamodel = SQLAInterface(ReworkErrorInItem)
    list_columns = ['error', 'defect_position', 'defect_cell']

class ReworkErrorOutItemModelView(ModelView):
    datamodel = SQLAInterface(ReworkErrorOutItem)
    list_columns = ['error', 'defect_position', 'defect_cell']

class ReworkModelView(ModelView):
    datamodel = SQLAInterface(Rework)
    related_views = [ReworkErrorInItemModelView]

    show_template = 'appbuilder/general/model/show_cascade.html'
    edit_template = 'appbuilder/general/model/edit_cascade.html'
    add_template = 'add_rework.html' 

    list_columns = ["psa", "part_number", "rework_created", "red_ticket_number", "red_ticket_date", "brigade_num", "defect_place", "status"]

    base_order = ("id", "asc")

    show_fieldsets = [
        ("Summary", {"fields": ["psa", "part_number", "rework_created", "red_ticket_number", "red_ticket_date", "brigade_num", "defect_place"]}),
    ]

    add_fieldsets = [
        ("Add New Rework", {"fields": ["psa", "part_number", "red_ticket_number", "red_ticket_date", "brigade_num", "defect_place"]}),
    ]

    edit_fieldsets = [
        ("Edit Rework", {"fields": ["psa", "part_number", "red_ticket_number", "red_ticket_date", "brigade_num", "defect_place", "status"]}),
    ]

class ReworkYellowModelView(ModelView):
    datamodel = SQLAInterface(Rework)
    list_columns = ["psa", "part_number", "rework_created", "red_ticket_number", "red_ticket_date", "brigade_num", "defect_place"]
    base_filters = [['status', FilterEqual, StatusEnum.yellow]]
    #base_permissions = ['can_add']
    related_views = [ReworkErrorOutItemModelView]

    show_template = 'appbuilder/general/model/show_cascade.html'
    edit_template = 'appbuilder/general/model/edit_cascade.html'
    add_template = 'add_rework.html' 

    base_order = ("id", "asc")

    show_fieldsets = [
        ("Summary", {"fields": ["psa", "part_number", "rework_created", "red_ticket_number", "red_ticket_date", "brigade_num", "defect_place", "yellow_ticket_number", "rework_period", "kw", "responsible" ]}),
    ]

    edit_fieldsets = [
        ("Edit Rework", {"fields": ["yellow_ticket_number", "rework_period", "kw", "responsible", "status"]}),
    ]



class ReworkWithErrorModelView(MultipleView):
    views = [ReworkModelView, ReworkErrorInItemModelView]


db.create_all()
fill_gender()

appbuilder.add_view(
    ReworkWithErrorModelView, "Test Rework View", icon="fa-envelope", category="Test Rework View"
)
appbuilder.add_view(
    GroupModelView,
    "List Groups",
    icon="fa-folder-open-o",
    category="Contacts",
    category_icon="fa-envelope",
)
appbuilder.add_view(
    ContactModelView, "List Contacts", icon="fa-envelope", category="Contacts"
)

appbuilder.add_view(
    PSAModelView, "List PSA", icon = "fa-envelope", category = "Add/Edit Data" 
)

appbuilder.add_view(
    OperatorModelView, "List Responsible Person", icon = "fa-envelope", category = "Add/Edit Data" 
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
    "Rework Yellow List",
    icon = "fa-envelope",
    category = "Rework" 
)

appbuilder.add_view_no_menu(ReworkErrorInItemModelView)

appbuilder.add_view_no_menu(ReworkErrorOutItemModelView)

appbuilder.add_separator("Contacts")
appbuilder.add_view(
    ContactChartView,
    "Contacts Chart",
    icon="fa-dashboard",
    category="Contacts",
)
appbuilder.add_view(
    ContactTimeChartView,
    "Contacts Birth Chart",
    icon="fa-dashboard",
    category="Contacts",
)
