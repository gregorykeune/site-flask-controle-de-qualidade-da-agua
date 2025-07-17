from flask import Blueprint, request
from models.iot.read import Read
from models.iot.sensors import Sensor
from models.iot.actuators import Actuator
from flask import render_template
from flask import flash, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

read = Blueprint("read", __name__, template_folder="views")  

@read.route("/history_read")
@login_required
def history_read():
    if current_user.is_operador():
        return redirect(url_for('user_bp.home'))
    sensors = Sensor.get_all_sensors()
    read = {}
    return render_template("history_read.html", sensors=sensors, read=read)

@read.route("/get_read", methods=['POST'])
@login_required
def get_read():
    if current_user.is_operador():
        return redirect(url_for('user_bp.home'))
    if request.method == 'POST':
        id = request.form['id']
        start = request.form['start']
        end = request.form['end']
        read = Read.get_read(id, start, end)
        sensors = Sensor.get_all_sensors()
        return render_template("history_read.html", sensors=sensors, read=read)
