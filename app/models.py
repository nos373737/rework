import datetime

from flask_appbuilder import Model
from sqlalchemy import Column, Date, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

mindate = datetime.date(datetime.MINYEAR, 1, 1)


class ContactGroup(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Gender(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Contact(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    address = Column(String(564))
    birthday = Column(Date, nullable=True)
    personal_phone = Column(String(20))
    personal_celphone = Column(String(20))
    contact_group_id = Column(Integer, ForeignKey("contact_group.id"), nullable=False)
    contact_group = relationship("ContactGroup")
    gender_id = Column(Integer, ForeignKey("gender.id"), nullable=False)
    gender = relationship("Gender")

    def __repr__(self):
        return self.name

    def month_year(self):
        date = self.birthday or mindate
        return datetime.datetime(date.year, date.month, 1) or mindate

    def year(self):
        date = self.birthday or mindate
        return datetime.datetime(date.year, 1, 1)

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
    rework_created = Column(DateTime, default = datetime.datetime.utcnow, nullable = False)
    red_ticket_number = Column(String(30), nullable = False)
    red_ticket_date = Column(Date)
    defect_place_id = Column(Integer, ForeignKey("defect_place.id"), nullable = False)
    defect_place = relationship("DefectPlace")

class ReworkErrorInItem(Model):
    id = Column(Integer, primary_key = True)
    rework_id = Column(Integer, ForeignKey("rework.id"), nullable = False)
    rework = relationship("Rework")
    error_code_id = Column(Integer, ForeignKey("error.id"), nullable = False)
    error = relationship("Error")
    defect_position_id = Column(Integer, ForeignKey("defect_position.id"), nullable = False)
    defect_position = relationship("DefectPosition")
    defect_cell = Column(String(30))

