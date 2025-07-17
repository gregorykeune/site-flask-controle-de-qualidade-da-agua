#app_controller.py
from flask import Flask, render_template, request, jsonify
from flask import flash, redirect, url_for
from models.db import db, instance
from controller.sensors_controller import sensor_
from controller.actuator_controller import actuator_
from controller.reads_controller import read
from controller.write_controller import write
from flask_login import LoginManager

from flask_socketio import SocketIO
import json
from flask_mqtt import Mqtt

from models.iot.read import Read
from models.iot.write import Write
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


salinidade= 10
ph = 10
ph_angulo = 0
sal_angulo = 0
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, 
                template_folder="./views/", 
                static_folder="./static/",
                root_path="./")

    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = instance
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'user_bp.login'

    from controller.user_controller import user_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(sensor_, url_prefix='/')
    app.register_blueprint(actuator_, url_prefix='/')
    app.register_blueprint(read, url_prefix='/')
    app.register_blueprint(write, url_prefix='/')
    


    
    @app.route('/login')
    def login():
        return render_template("login.html")
    
    
    app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = ''  
    app.config['MQTT_PASSWORD'] = ''  
    app.config['MQTT_KEEPALIVE'] = 5000  
    app.config['MQTT_TLS_ENABLED'] = False 

    mqtt_client= Mqtt()
    mqtt_client.init_app(app)

    topic_subscribe = "aquario/#"



    @app.route('/tempo_real')
    @login_required
    def tempo_real():
        if current_user.is_operador():
            return redirect(url_for('user_bp.home'))
        global salinidade, ph
        values = {"salinidade":salinidade, "ph":ph, "ph_angulo": ph_angulo, "sal_angulo": sal_angulo}
        return render_template("tr.html", values=values)
    

    @app.route('/publish')
    @login_required
    def publish():
        if current_user.is_estatistico():
            return redirect(url_for('user_bp.home'))
        return render_template('publish.html')


    @app.route('/publish_message', methods=['POST'])
    @login_required
    def publish_message():
        if current_user.is_estatistico():
            return redirect(url_for('user_bp.home'))
        try:
            topic = request.form.get('topic')
            message = request.form.get('message')

            if not topic or not message:
                flash("Tópico e mensagem são obrigatórios.", "danger")
                return redirect(url_for('publish'))

            if topic == "aquario/modo":
                if message not in ['manual', 'auto']:
                    flash("Modo escolhido inválido", "danger")
                    return redirect(url_for('publish'))

                mqtt_client.publish(topic, message)
                flash("Modo atualizado com sucesso", "success")
                return redirect(url_for('publish'))

            elif topic in ["aquario/sal/servosal", "aquario/ph/servoph"]:
                try:
                    valor = float(message)
                    mqtt_client.publish(topic, int(valor))
                    Write.save_write(topic, valor)
                    flash("Valor do ângulo do servo alterado com sucesso", "success")
                    return redirect(url_for('publish'))
                except ValueError:
                    flash("Valor inválido para servo", "danger")
                    return redirect(url_for('publish'))

            flash("Tópico não reconhecido", "danger")
            return redirect(url_for('publish'))

        except Exception as e:
            flash(f"Erro interno: {str(e)}", "danger")
            return redirect(url_for('publish'))



    @mqtt_client.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Conexao ao broker foi um sucesso')
            mqtt_client.subscribe(topic_subscribe)
        else:
            print('Nao foi possivel conectar ao broker. codigo: ', rc)

    @mqtt_client.on_disconnect()
    def handle_disconnect(client, userdata, rc):
        print("Disconnected from broker")


    @mqtt_client.on_message()
    def handle_mqtt_message(client, userdata, message):
        global salinidade, ph, ph_angulo, sal_angulo
        print(f"[MQTT] Mensagem recebida em {message.topic}: {message.payload}")

        try:

            valor = message.payload.decode()

            with app.app_context():
                if message.topic == "aquario/sal":
                    salinidade = float(valor)
                    Read.save_read(message.topic, float(valor))
                elif message.topic == "aquario/ph":
                    ph = float(valor)
                    Read.save_read(message.topic, float(valor))
                elif message.topic == "aquario/ph/servo":
                    ph_angulo = float(valor)
                    Write.save_write(message.topic, float(valor))
                elif message.topic == "aquario/sal/servo":
                    sal_angulo = float(valor)
                    Write.save_write(message.topic, float(valor))



        except Exception as e:
            print("Erro ao processar mensagem MQTT:", e)

    
    return app
