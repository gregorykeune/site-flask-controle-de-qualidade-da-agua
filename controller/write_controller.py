from flask import Blueprint, request
from models.iot.write import Write
from models.iot.sensors import Sensor
from models.iot.actuators import Actuator
from flask import render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash


write = Blueprint("write", __name__, template_folder="views")  

@write.route("/history_write")
@login_required
def history_write():
    if current_user.is_estatistico():
        return redirect(url_for('user_bp.home'))
    actuators = Actuator.get_all_actuators()
    write_data = {}
    return render_template("history_write.html", actuators=actuators, write=write_data)

@write.route("/get_write", methods=['POST'])
@login_required
def get_write():
    if request.method == 'POST':
        id = request.form['id']
        start = request.form['start']
        end = request.form['end']
        write_data = Write.get_write(id, start, end)
        actuators = Actuator.get_all_actuators()
        return render_template("history_write.html", actuators=actuators, write=write_data)
