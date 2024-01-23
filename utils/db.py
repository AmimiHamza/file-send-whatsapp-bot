from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from enum import Enum as PythonEnum
from datetime import datetime



Base = declarative_base()

class MaterialType(PythonEnum):
    TP = 'TP'
    TD = 'TD'
    COURS = 'Cours'
    EXAM = 'Exam'
    DIVERS = 'Divers'


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    label = Column(String(10), nullable=False)
    study_materials = relationship('StudyMaterial', back_populates='course')




class StudyMaterial(Base):
    __tablename__ = 'study_materials'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255), nullable=True)
    link = Column(String(255), nullable=False, unique=True)
    type = Column(Enum(MaterialType), nullable=False)
    year = Column(Integer, nullable=False, default=datetime.now().year)
    part = Column(Integer, nullable=False,default=0)

    course_id = Column(Integer, ForeignKey('courses.id'))
    course = relationship('Course', back_populates='study_materials')

    def __str__(self):
        return f'{self.course.label}_{self.type.value.upper()}_{self.part}_{self.year}'





class AgentDB:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
    
    def get_study_material(self, course_label, type, year, part = 0):
        return self.session.query(StudyMaterial).join(Course).filter(Course.label==course_label, StudyMaterial.type==type, StudyMaterial.year==year, StudyMaterial.part==part).first()

    
        

    def add_study_material(self, course_id, type, year, part, link, description=None):
        study_material = StudyMaterial(course_id=course_id, type=type, year=year, part=part, link=link, description=description)
        self.session.add(study_material)
        self.session.commit()
        return study_material

    def get_courses(self):
        return self.session.query(Course).all()

    def get_course(self, label):
        return self.session.query(Course).filter_by(label=label).first()

    def add_course(self, label):
        course = Course(label=label)
        self.session.add(course)
        self.session.commit()
        return course

    def get_study_materials(self, course_id):
        return self.session.query(StudyMaterial).filter_by(course_id=course_id).all()

    def get_study_materials_by_type(self, course_id, type):
        return self.session.query(StudyMaterial).filter_by(course_id=course_id, type=type).all()

    def get_study_materials_by_year(self, course_id, year):
        return self.session.query(StudyMaterial).filter_by(course_id=course_id, year=year).all()

    def get_study_materials_by_part(self, course_id, part):
        return self.session.query(StudyMaterial).filter_by(course_id=course_id, part=part).all()

    def get_study_materials_by_year_and_part(self, course_id, year, part):
        return self.session.query(StudyMaterial).filter_by(course_id=course_id, year=year, part=part).all()

    






