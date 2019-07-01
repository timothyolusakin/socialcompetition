import os
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from flask_login import UserMixin,AnonymousUserMixin
from app import db,login_manager
from datetime import datetime,date
import jwt
from werkzeug.security import generate_password_hash,check_password_hash
from time import time


"""
An assocciation table between Creatives and Skill
"""
skills = db.Table('skills',
                 db.Column('creatives_id',db.Integer,db.ForeignKey('creatives.id')),
                 db.Column('skills_id',db.Integer,db.ForeignKey('skill.id'))
                 )

class Creatives(UserMixin,db.Model):
    """
    This is the table for creatives which is the base for the platform
    It consist of basic information such as email,name,instagram_account
    also consist of links with other tables partaining the task
    """
    __tablename__ = 'creatives'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer, unique=True)
    create_date = db.Column(db.DateTime(), default=datetime.now())
    name = db.Column(db.String(100))
    password_hash = db.Column(db.String(20))
    email = db.Column(db.String(100))
    active = db.Column(db.String(100))
    instagram_account = db.Column(db.String(100))
    skill = db.relationship('Skill',secondary=skills,lazy='subquery', backref=db.backref('skill',lazy=True))
    competiton_creative = db.relationship('Competition_Creatives', backref='competition_creatives')
    competiton_attendee = db.relationship('Competiton_Attendee', backref='competition_attendee')
    competiton_winners = db.relationship('Competiton_Winners',backref='competiton_winners')
    competiton_upload = db.relationship('Competition_Upload', backref='competition_upload')

    """
        SET PASSWORD HASHING FOR CREATIVES 
        AND VERIFY PASSWORDS FOR CREATIVES 
    """
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_activation_token(self, expires_in=86400):
        return jwt.encode(
            {'activation': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_accept_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['activation']
        except:
            return
        return Creatives.query.filter_by(id=id).first()

class Skill(db.Model):
    """
        This is the table for skill/category for the platform
        also consist of links with other tables partaining the task
        inser_values: inserts values into the table/ database when called from the python command line using
        Skill.insert_values(
        """
    __tablename__ = 'skill'
    id = db.Column(db.Integer, primary_key=True)
    skills = db.Column(db.String(100))
    competiton_skills = db.relationship('Competition_Skills', backref='competition_skills')
    competiton_creatives = db.relationship('Competition_Creatives', backref='competition_creative')
    competiton_attendee = db.relationship('Competiton_Attendee', backref='competition_attendeent')
    competiton_winners = db.relationship('Competiton_Winners', backref='competition_winners')


    """This part adds new skill/category when the function is called wwhen starting the software for the first time"""
    @staticmethod
    def insert_values():
        check = Skill.query.all()
        if check:
            pass
        else:
            skills = ['Photography (DSLR)','Photography (Mobile)', 'Videography' , 'Videography (Mobile)', 'Make Up Artist', 'Model',
                      'Creative Director', 'Painting']
            for skill in skills:
                skill = Skill(
                    skills = skill
                )
                db.session.add(skill)
                db.session.commit()

class Competition_Information(db.Model):
    """
    Competiton information contains the competition task inserted by the admin of the site and can't be edited afterwards

    """
    __tablename__ = 'competition_information'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(256))
    location_of_task = db.Column(db.String(100))
    time_and_date_of_task = db.Column(db.String(100))
    duration_of_task = db.Column(db.String(100))
    time_of_creation = create_date = db.Column(db.DateTime(), default=date.today())
    competition_skills = db.relationship('Competition_Skills', backref='competition_skill')
    competiton_creatives = db.relationship('Competition_Creatives', backref='competition_creativee')
    competiton_attendee = db.relationship('Competiton_Attendee', backref='competition_attendeeed')
    competiton_winners = db.relationship('Competiton_Winners', backref='competition_winnerst')
    competiton_upload = db.relationship('Competition_Upload', backref='competition_uploadt')

class Competition_Skills(db.Model):
    __tablename__ = 'competition_skills'
    id = db.Column(db.Integer, primary_key=True)
    skills_id = db.Column(db.Integer, db.ForeignKey('skill.id'))
    no_needed = db.Column(db.Integer())
    competition_id = db.Column(db.Integer, db.ForeignKey('competition_information.id'))

class Competition_Creatives(db.Model):
    __tablename__ = 'competition_creatives'
    id = db.Column(db.Integer, primary_key=True)
    creatives_id  = db.Column(db.Integer, db.ForeignKey('creatives.id'))
    accepted = db.Column(db.String(100))
    skills_id = db.Column(db.Integer, db.ForeignKey('skill.id'))
    competiton_id = db.Column(db.Integer, db.ForeignKey('competition_information.id'))

class Competiton_Attendee(db.Model):
    __tablename__ = 'competition_attendee'
    id = db.Column(db.Integer, primary_key=True)
    creatives_id = db.Column(db.Integer, db.ForeignKey('creatives.id'))
    competition_id = db.Column(db.Integer, db.ForeignKey('competition_information.id'))
    skills_id = db.Column(db.Integer, db.ForeignKey('skill.id'))

class Competiton_Winners(db.Model):
    __tablename__ = 'competition_Winners'
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition_information.id'))
    creatives_id = db.Column(db.Integer, db.ForeignKey('creatives.id'))
    skills_id = db.Column(db.Integer, db.ForeignKey('skill.id'))
    screenshot =db.Column(db.String(100))
    date_entered = db.Column(db.DateTime(), default=date.today())

class Competition_Upload(db.Model):
    __tablename__ = "competion_upload"
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(100))
    competition_id = db.Column(db.Integer, db.ForeignKey('competition_information.id'))
    creatives_id = db.Column(db.Integer, db.ForeignKey('creatives.id'))


