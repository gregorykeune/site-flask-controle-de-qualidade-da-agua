from models.db import db
from models.iot.devices import Device

class Actuator(db.Model):
    __tablename__ = 'actuators'
    id= db.Column('id', db.Integer, primary_key=True)
    devices_id = db.Column( db.Integer, db.ForeignKey(Device.id))
    unit = db.Column(db.String(50))
    topic = db.Column(db.String(50))
    
    def save_actuator(name, brand, model, unit, topic, is_active):
        device = Device(name=name, brand=brand, model=model, is_active=is_active)
        
        actuator = Actuator(devices_id=device.id, unit=unit, topic=topic)
        
        device.actuators.append(actuator)
        db.session.add(device)
        db.session.commit()

    def get_single_actuator(id):
        actuator = Actuator.query.filter(Actuator.devices_id == id).first()
        if actuator is not None:
            actuator = Actuator.query.filter(Actuator.devices_id == id)\
            .join(Device).add_columns(Device.id, Device.name, Device.brand,
            Device.model, Device.is_active, Actuator.topic, Actuator.unit).first()
            return [actuator]
        
    def get_all_actuators():
        actuators = Actuator.query.all()
        if actuators is not None:
            actuators = Actuator.query.join(Device).add_columns(Device.id, Device.name, Device.brand,
            Device.model, Device.is_active, Actuator.topic, Actuator.unit).all()
            return actuators
        
    def update_actuator(id, name, brand, model, topic, unit, is_active):
        device = Device.query.filter(Device.id == id).first()
        actuator = Actuator.query.filter(Actuator.devices_id == id).first()
        if device is not None and actuator is not None:
            device.name = name
            device.brand = brand
            device.model = model
            actuator.topic = topic
            actuator.unit = unit
            device.is_active = is_active
            db.session.commit()
        return Actuator.get_all_actuators()
    
    def delete_actuator(id):
        actuator = Actuator.query.filter(Actuator.devices_id == id).first()
        device = Device.query.filter(Device.id == id).first()
        if actuator is not None:
            db.session.delete(actuator)
            db.session.delete(device)
            db.session.commit()
        return Actuator.get_all_actuators()
    