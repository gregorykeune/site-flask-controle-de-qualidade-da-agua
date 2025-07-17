from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.iot.sensors import Sensor

sensor_ = Blueprint('sensor', __name__, template_folder='views')


@sensor_.route('/register_sensor')
@login_required
def register_sensor():
    if not current_user.is_admin():
        return redirect(url_for('user_bp.home'))
    return render_template('register_sensor.html')


@sensor_.route('/add_sensor', methods=['POST'])
@login_required
def add_sensor():
    if not current_user.is_admin():
        return redirect(url_for('user_bp.home'))
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    unit = request.form.get("unit")
    topic = request.form.get("topic")
    is_active = True if request.form.get("is_active") == "on" else False

    Sensor.save_sensor(name, brand, model, unit, topic, is_active)
    sensors = Sensor.get_all_sensors()
    return render_template("sensors.html", sensors=sensors)


@sensor_.route('/sensors')
@login_required
def sensors():
    if current_user.is_operador():
        return redirect(url_for('user_bp.home'))
    sensors = Sensor.get_all_sensors()
    return render_template('sensors.html', sensors=sensors)


@sensor_.route('/edit_sensor')
@login_required
def edit_sensor():
    if not current_user.is_admin():
        return redirect(url_for('user_bp.home'))
    id = request.args.get('id', None)
    sensor = Sensor.get_single_sensor(id)
    return render_template("update_sensor.html", sensor=sensor)


@sensor_.route('/update_sensor', methods=['POST'])
@login_required
def update_sensor():
    if not current_user.is_admin():
        return redirect(url_for('user_bp.home'))
    id = request.form.get("id")
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = True if request.form.get("is_active") == "on" else False

    Sensor.update_sensor(id, name, brand, model, topic, unit, is_active)
    sensors = Sensor.get_all_sensors()
    return render_template("sensors.html", sensors=sensors)


@sensor_.route('/del_sensor')
@login_required
def delete_sensor():
    if not current_user.is_admin():
        return redirect(url_for('user_bp.home'))
    id = request.args.get('id', None)
    Sensor.delete_sensor(id)
    sensors = Sensor.get_all_sensors()
    return render_template("sensors.html", sensors=sensors)
