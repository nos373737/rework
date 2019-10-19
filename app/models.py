import datetime

from flask import Markup, url_for
from flask_appbuilder import Model
import enum
from sqlalchemy import Column, Date, ForeignKey, Integer, String, DateTime, Enum, Sequence
from sqlalchemy.orm import relationship

mindate = datetime.date(datetime.MINYEAR, 1, 1)

#Enumeration in Rework
class StatusEnum(enum.Enum):
    red = "Red"
    yellow = "Yellow"
    done = "Done"
    broken = "Broken"

#Group for Employee
class EmployeeGroupEnum(enum.Enum):
    operator = "Operator"
    brigade_chief = "Brigade Chief"

class PSA(Model):
    id = Column(Integer, primary_key = True)
    description = Column(String(30), nullable = False)

    def __repr__(self):
        return self.description

class PartNumber(Model):
    id = Column(Integer, primary_key = True)
    description = Column(String(30), nullable = False)

    def __repr__(self):
        return self.description

class BrigadeNum(Model):
    id = Column(Integer, primary_key = True)
    description = Column(String(30), nullable = False)

    def __repr__(self):
        return self.description

class DefectPosition(Model):
    id = Column(Integer, primary_key = True)
    description = Column(String(30), nullable = False)

    def __repr__(self):
        return self.description

class DefectPlace(Model):
    id = Column(Integer, primary_key = True)
    description = Column(String(30), nullable = False)

    def __repr__(self):
        return self.description


class Employee(Model):
    id = Column(Integer, primary_key = True)
    description = Column(String(30), nullable = False)
    group = Column(Enum(EmployeeGroupEnum), nullable = False)

    def __repr__(self):
        return "({0}, {1})".format(self.group.value, self.description)


class ErrorGroup(Model):
    id = Column(Integer, primary_key = True)
    description = Column(String(30), nullable = False)
    symbol_code = Column(String(2), nullable = False)

    def __repr__(self):
        return "({0}, {1})".format(self.symbol_code, self.description)

class Error(Model):
    id = Column(Integer, primary_key = True)
    description = Column(String(50), nullable = False)
    symbol_code = Column(String(4), nullable = False)
    error_group_id = Column(Integer, ForeignKey("error_group.id"), nullable=False)
    error_group = relationship("ErrorGroup")

    def __repr__(self):
        return "({0}, {1})".format(self.symbol_code, self.description)

class Rework(Model):
    id = Column(Integer, primary_key = True)
    psa_id = Column(Integer, ForeignKey("PSA.id"), nullable = False)
    psa = relationship("PSA")
    part_number_id = Column(Integer, ForeignKey("part_number.id"), nullable = False)
    part_number = relationship("PartNumber")
    rework_created = Column(DateTime, default = datetime.datetime.utcnow(), nullable = False)
    brigade_num_id = Column(Integer, ForeignKey("brigade_num.id"), nullable = False)
    brigade_num = relationship("BrigadeNum")
    defect_position_id = Column(Integer, ForeignKey("defect_position.id"), nullable = False)
    defect_position = relationship("DefectPosition") 
    defect_place_id = Column(Integer, ForeignKey("defect_place.id"), nullable = False)
    defect_place = relationship("DefectPlace")
    error_code_id = Column(Integer, ForeignKey("error.id"), nullable = False)
    error = relationship("Error")
    red_ticket_date = Column(DateTime, nullable = False)
    status = Column(Enum(StatusEnum), nullable = False, default = StatusEnum.red)
    employee_id = Column(Integer, ForeignKey("employee.id"))
    brigade_chief_name = relationship("Employee") 

    def __repr__(self):
        return "({0}, {1})".format(self.id, self.psa, self.status)

class OperatorZone(Model):
    id = Column(Integer, primary_key = True)
    rework_id = Column(Integer, ForeignKey("rework.id"), nullable = False)
    rework = relationship("Rework")
    error_code_id = Column(Integer, ForeignKey("error.id"), nullable = False)
    error = relationship("Error")
    defect_position_id = Column(Integer, ForeignKey("defect_position.id"), nullable = False)
    defect_position = relationship("DefectPosition")
    defect_cell = Column(String(30))
    operator_rework_done = Column(DateTime, default = datetime.datetime.utcnow(), nullable = False)

    def search(self):
        return Markup(
        '<div id = "rework-barcode-search-field"><input type = "text" placeholder = "Scan barcode">'
        + '<button type="submit"><i class="fa fa-search"></i></button>'
        + '</div>'
        )

        
# class ReworkErrorOutItem(Model):
#     id = Column(Integer, primary_key = True)
#     rework_id = Column(Integer, ForeignKey("rework.id"), nullable = False)
#     rework = relationship("Rework")
#     error_code_id = Column(Integer, ForeignKey("error.id"), nullable = False)
#     error = relationship("Error")
#     defect_position_id = Column(Integer, ForeignKey("defect_position.id"), nullable = False)
#     defect_position = relationship("DefectPosition")
#     defect_cell = Column(String(30))

