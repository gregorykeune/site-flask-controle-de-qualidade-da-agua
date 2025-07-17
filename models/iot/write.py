from models.db import db
from models.iot.actuators import Actuator
from models.iot.devices import Device
from datetime import datetime

class Write(db.Model):
    __tablename__ = 'write'
    id = db.Column('id', db.Integer, nullable=False, primary_key=True)
    write_datetime = db.Column(db.DateTime(), nullable=False)
    actuator_id = db.Column(db.Integer, db.ForeignKey(Actuator.id), nullable=False)
    degree = db.Column(db.String(255), nullable=False)
    
    def get_write(device_id, start, end):
        actuator = Actuator.query.filter(Actuator.devices_id == device_id).first()
        write = Write.query.filter(Write.actuator_id == actuator.id,
		Write.write_datetime > start,
		Write.write_datetime < end).all()
        return write

    def save_write(topic, degree):
        actuator = Actuator.query.filter(Actuator.topic == topic).first()
        if actuator is not None:
            device = Device.query.filter(Device.id == actuator.devices_id).first()
            if device is not None and device.is_active:
                write = Write(write_datetime=datetime.now(), actuator_id=actuator.id, degree=degree)
                db.session.add(write)
                db.session.commit()
