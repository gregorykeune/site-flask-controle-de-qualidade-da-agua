#user.py
from models.db import db
from flask_login import UserMixin

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role')

    def is_admin(self):
        return self.role.name == 'Admin'
    
    def is_estatistico(self):
        return self.role.name == 'Estatistico'
    
    def is_operador(self):
        return self.role.name == 'Operador'
    
    def check_password(self, password):
        return self.password == password
    
    def getName(self):
        return self.username