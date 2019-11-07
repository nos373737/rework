from flask_appbuilder.widgets import FormWidget, ShowWidget


class MyFormWidget(FormWidget):
     template = 'widgets/my_form.html'

class MyShowWidget(ShowWidget):
     template = 'widgets/my_show.html'

class MyReFormWidget(FormWidget):
     template = 'widgets/my_reform.html'