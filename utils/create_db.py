from flask import Flask
from models import *

def create_db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        admin_role = Role(name='Admin')
        estatistico_role = Role(name='Estatistico')
        operador_role = Role(name='Operador')
        db.session.add(admin_role)
        db.session.add(estatistico_role)
        db.session.add(operador_role)
        db.session.commit()
        
        admin_user = User(
            username='admin',
            email='admin@email.com',
            password='123',
            role=admin_role
        )
        estatistico_user = User(
            username='estatistico',
            email='estatistico@email.com',
            password='123',
            role=estatistico_role
        )
        operador_user = User(
            username='operador',
            email='operador@email.com',
            password='123',
            role=operador_role
        )



        db.session.add(admin_user)
        db.session.add(estatistico_user)
        db.session.add(operador_user)
        db.session.commit()
        
        print("Banco criado com sucesso com usuário admin, estatístico e operador.")
