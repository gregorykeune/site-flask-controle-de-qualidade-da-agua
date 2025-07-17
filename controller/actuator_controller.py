from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.iot.actuators import Actuator

actuator_ = Blueprint('actuator', __name__, template_folder='views')


@actuator_.route('/register_actuator')
@login_required
def register_actuator():
    if not current_user.is_admin():
        return redirect(url_for('user_bp.home'))
    return render_template('register_actuator.html')


@actuator_.route('/add_actuator', methods=['POST'])
@login_required
def add_actuator():
    if not current_user.is_admin():
        return redirect(url_for('user_bp.home'))
   
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    unit = request.form.get("unit")
    topic = request.form.get("topic")
    is_active = True if request.form.get("is_active") == "on" else False

    Actuator.save_actuator(name, brand, model, unit, topic, is_active)
    actuators = Actuator.get_all_actuators()
    return render_template("actuators.html", actuators=actuators)


@actuator_.route('/actuators')
@login_required
def actuators():
    if not current_user.is_admin():
        return redirect(url_for('user_bp.home'))
    actuators = Actuator.get_all_actuators()
    return render_template('actuators.html', actuators=actuators)


@actuator_.route('/edit_actuator')
@login_required
def edit_actuator():
    if not current_user.is_admin():
        return redirect(url_for('user_bp.home'))
    id = request.args.get('id', None)
    actuator = Actuator.get_single_actuator(id)
    return render_template("update_actuator.html", actuator=actuator)


@actuator_.route('/update_actuator', methods=['POST'])
@login_required
def update_actuator():
    if not current_user.is_admin():
        return redirect(url_for('user_bp.home'))
    id = request.form.get("id")
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = True if request.form.get("is_active") == "on" else False

    Actuator.update_actuator(id, name, brand, model, topic, unit, is_active)
    actuators = Actuator.get_all_actuators()
    return render_template("actuators.html", actuators=actuators)


@actuator_.route('/del_actuator')
@login_required
def delete_actuator():
    if not current_user.is_admin():
        return redirect(url_for('user_bp.home'))

    id = request.args.get('id', None)
    Actuator.delete_actuator(id)
    actuators = Actuator.get_all_actuators()
    return render_template("actuators.html", actuators=actuators)
