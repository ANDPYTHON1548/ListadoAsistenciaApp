import base64
from datetime import datetime
import hashlib
import os
from uuid import uuid4 as uuid

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'db', 'listado_asistencias.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
db = SQLAlchemy(app)

# Mail configuration
app.config["MAIL_SERVER"] = "app.debugmail.io"
app.config["MAIL_PORT"] = 25
app.config["MAIL_USERNAME"] = "95f620c6-3334-453a-9997-cf1a1398f8a2"
app.config["MAIL_PASSWORD"] = "1e7cfb16-7d1d-4a49-964c-84c30128ca4b"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False

# Initialize Flask-Mail
mail = Mail(app)


class Usuario(db.Model):
    Email = db.Column(db.String, primary_key=True)
    Clave = db.Column(db.String, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Usuario {self.Email}>'

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()


@app.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.get_json()
    email = data.get('Email')
    clave = Usuario.hash_password(data.get('Clave'))
    new_usuario = Usuario(Email=email, Clave=clave)
    db.session.add(new_usuario)
    db.session.commit()
    return jsonify({'message': 'Usuario creado exitosamente'}), 201


@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{'Email': usuario.Email, 'fecha_creacion': usuario.fecha_creacion} for usuario in usuarios]), 200


@app.route('/usuarios/<email>', methods=['GET'])
def get_usuario(email):
    usuario = Usuario.query.get_or_404(email)
    return jsonify({'Email': usuario.Email, 'fecha_creacion': usuario.fecha_creacion}), 200


@app.route('/usuarios/<email>', methods=['PUT'])
def update_usuario(email):
    usuario = Usuario.query.get_or_404(email)
    data = request.get_json()
    usuario.Clave = Usuario.hash_password(data.get('Clave'))
    usuario.fecha_modificacion = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Usuario actualizado exitosamente'}), 200


@app.route('/usuarios/<email>', methods=['DELETE'])
def delete_usuario(email):
    usuario = Usuario.query.get_or_404(email)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'message': 'Usuario eliminado exitosamente'}), 200


class Rol(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre = db.Column(db.String, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Rol {self.Nombre}>'


@app.route('/roles', methods=['POST'])
def create_rol():
    data = request.get_json()
    nombre = data.get('Nombre')
    new_rol = Rol(Nombre=nombre)
    db.session.add(new_rol)
    db.session.commit()
    return jsonify({'message': 'Rol creado exitosamente'}), 201


@app.route('/roles', methods=['GET'])
def get_roles():
    roles = Rol.query.all()
    return jsonify([{'ID': rol.ID, 'Nombre': rol.Nombre} for rol in roles]), 200


@app.route('/roles/<int:id_rol>', methods=['GET'])
def get_rol(id_rol):
    rol = Rol.query.get_or_404(id_rol)
    return jsonify({'ID': rol.ID, 'Nombre': rol.Nombre}), 200


@app.route('/roles/<int:id_rol>', methods=['PUT'])
def update_rol(id_rol):
    rol = Rol.query.get_or_404(id_rol)
    data = request.get_json()
    rol.Nombre = data.get('Nombre')
    rol.fecha_modificacion = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Rol actualizado exitosamente'}), 200


@app.route('/roles/<int:id_rol>', methods=['DELETE'])
def delete_rol(id_rol):
    rol = Rol.query.get_or_404(id_rol)
    db.session.delete(rol)
    db.session.commit()
    return jsonify({'message': 'Rol eliminado exitosamente'}), 200


class Cargo(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Cargo {self.Nombre}>'


@app.route('/cargos', methods=['POST'])
def create_cargo():
    data = request.get_json()
    nombre = data.get('Nombre')
    new_cargo = Cargo(Nombre=nombre)
    db.session.add(new_cargo)
    db.session.commit()
    return jsonify({'message': 'Cargo creado exitosamente'}), 201


@app.route('/cargos', methods=['GET'])
def get_cargos():
    cargos = Cargo.query.all()
    return jsonify([{'ID': cargo.ID, 'Nombre': cargo.Nombre} for cargo in cargos]), 200


@app.route('/cargos/<int:id_cargo>', methods=['GET'])
def get_cargo(id_cargo):
    cargo = Cargo.query.get_or_404(id_cargo)
    return jsonify({'ID': cargo.ID, 'Nombre': cargo.Nombre}), 200


@app.route('/cargos/<int:id_cargo>', methods=['PUT'])
def update_cargo(id_cargo):
    cargo = Cargo.query.get_or_404(id_cargo)
    data = request.get_json()
    cargo.Nombre = data.get('Nombre')
    cargo.fecha_modificacion = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Cargo actualizado exitosamente'}), 200


@app.route('/cargos/<int:id_cargo>', methods=['DELETE'])
def delete_cargo(id_cargo):
    cargo = Cargo.query.get_or_404(id_cargo)
    db.session.delete(cargo)
    db.session.commit()
    return jsonify({'message': 'Cargo eliminado exitosamente'}), 200


class Persona(db.Model):
    Identificacion = db.Column(db.String, primary_key=True)
    Nombre = db.Column(db.String, nullable=False)
    Cargo = db.Column(db.Integer, db.ForeignKey('cargo.ID'))
    Rol = db.Column(db.Integer, db.ForeignKey('rol.ID'))
    Email = db.Column(db.String, db.ForeignKey('usuario.Email'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Persona {self.Nombre}>'


@app.route('/personas', methods=['POST'])
def create_persona():
    data = request.get_json()
    persona = Persona(
        Identificacion=data.get('Identificacion'),
        Nombre=data.get('Nombre'),
        Cargo=data.get('Cargo'),
        Rol=data.get('Rol'),
        Email=data.get('Email')
    )
    db.session.add(persona)
    db.session.commit()
    return jsonify({'message': 'Persona creada exitosamente'}), 201


@app.route('/personas', methods=['GET'])
def get_personas():
    personas = Persona.query.all()
    return jsonify([
        {
            'Identificacion': persona.Identificacion,
            'Nombre': persona.Nombre,
            'Cargo': Cargo.query.get(persona.Cargo).Nombre,
            'Rol': Rol.query.get(persona.Rol).Nombre,
            'Email': persona.Email
        } for persona in personas
    ]), 200


@app.route('/personas/<identificacion>', methods=['GET'])
def get_persona(identificacion):
    persona = Persona.query.get_or_404(identificacion)
    return jsonify({
        'Identificacion': persona.Identificacion,
        'Nombre': persona.Nombre,
        'Cargo': persona.Cargo,
        'Rol': persona.Rol,
        'Email': persona.Email
    }), 200


@app.route('/personas/correo/<correo>', methods=['GET'])
def get_persona_por_correo(correo):
    persona = Persona.query.filter_by(Email=correo).first()
    return jsonify({
        'Identificacion': persona.Identificacion,
        'Nombre': persona.Nombre,
        'Cargo': persona.Cargo,
        'Rol': persona.Rol,
        'Email': persona.Email
    }), 200


@app.route('/personas/<identificacion>', methods=['PUT'])
def update_persona(identificacion):
    persona = Persona.query.get_or_404(identificacion)
    data = request.get_json()
    persona.Nombre = data.get('Nombre', persona.Nombre)
    persona.Cargo = data.get('Cargo', persona.Cargo)
    persona.Rol = data.get('Rol', persona.Rol)
    persona.Email = data.get('Email', persona.Email)
    persona.fecha_modificacion = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Persona actualizada exitosamente'}), 200


@app.route('/personas/<identificacion>', methods=['DELETE'])
def delete_persona(identificacion):
    persona = Persona.query.get_or_404(identificacion)

    evento_personas = EventoPersona.query.filter_by(PersonaIdentificacion=identificacion).all()
    for relacion in evento_personas:
        db.session.delete(relacion)

    instructor = Instructor.query.filter_by(Identificacion=identificacion).first()
    if instructor:
        eventos = Evento.query.filter_by(Instructor=identificacion).all()
        for evento in eventos:
            evento.Instructor = None

        db.session.delete(instructor)

    usuario = Usuario.query.filter_by(Email=persona.Email).first()

    if usuario:
        db.session.delete(usuario)

    db.session.delete(persona)
    db.session.commit()
    return jsonify({'message': 'Persona eliminada exitosamente'}), 200


def serializar_persona(persona):
    """
    Función para serializar una instancia de Persona.

    Args:
        persona (Persona): Instancia de Persona a serializar.

    Returns:
        dict: Diccionario con los datos de la persona serializados.
    """
    return {
        'Identificacion': persona.Identificacion,
        'Nombre': persona.Nombre,
        'Cargo': persona.Cargo,
        'Rol': persona.Rol,
        'Email': persona.Email
    }


class Instructor(db.Model):
    Identificacion = db.Column(db.String, db.ForeignKey('persona.Identificacion'), primary_key=True)
    Rol = db.Column(db.Integer, db.ForeignKey('rol.ID'))
    Estado = db.Column(db.Integer, nullable=False)
    Observacion = db.Column(db.Text)
    Email = db.Column(db.String, db.ForeignKey('usuario.Email'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/instructores', methods=['POST'])
def create_instructor():
    data = request.get_json()
    instructor = Instructor(
        Identificacion=data.get('Identificacion'),
        Rol=data.get('Rol'),
        Estado=data.get('Estado'),
        Observacion=data.get('Observacion'),
        Email=data.get('Email')
    )
    db.session.add(instructor)
    db.session.commit()
    return jsonify({'message': 'Instructor creado exitosamente'}), 201


@app.route('/instructores', methods=['GET'])
def get_instructores():
    instructores = Instructor.query.all()

    for instructor in instructores:
        persona = Persona.query.get(instructor.Identificacion)
        instructor.Nombre = persona.Nombre

    return jsonify([{
        'Identificacion': instructor.Identificacion,
        'Nombre': instructor.Nombre,
        'Rol': instructor.Rol,
        'Estado': instructor.Estado,
        'Observacion': instructor.Observacion,
        'Email': instructor.Email
    } for instructor in instructores]), 200


@app.route('/instructores/<identificacion>', methods=['GET'])
def get_instructor(identificacion):
    instructor = Instructor.query.get_or_404(identificacion)
    return jsonify({
        'Identificacion': instructor.Identificacion,
        'Rol': instructor.Rol,
        'Estado': instructor.Estado,
        'Observacion': instructor.Observacion,
        'Email': instructor.Email
    }), 200


@app.route('/instructores/<identificacion>', methods=['PUT'])
def update_instructor(identificacion):
    instructor = Instructor.query.get_or_404(identificacion)
    data = request.get_json()
    instructor.Rol = data.get('Rol', instructor.Rol)
    instructor.Estado = data.get('Estado', instructor.Estado)
    instructor.Observacion = data.get('Observacion', instructor.Observacion)
    instructor.Email = data.get('Email', instructor.Email)
    instructor.fecha_modificacion = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Instructor actualizado exitosamente'}), 200


@app.route('/instructores/<identificacion>', methods=['DELETE'])
def delete_instructor(identificacion):
    instructor = Instructor.query.get_or_404(identificacion)
    db.session.delete(instructor)
    db.session.commit()
    return jsonify({'message': 'Instructor eliminado exitosamente'}), 200


class Dependencia(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Dependencia {self.Nombre}>'


@app.route('/dependencias', methods=['POST'])
def create_dependencia():
    data = request.get_json()
    nombre = data.get('Nombre')
    new_dependencia = Dependencia(Nombre=nombre)
    db.session.add(new_dependencia)
    db.session.commit()
    return jsonify({'message': 'Dependencia creada exitosamente'}), 201


@app.route('/dependencias', methods=['GET'])
def get_dependencias():
    dependencias = Dependencia.query.all()
    return jsonify([{
        'ID': dependencia.ID,
        'Nombre': dependencia.Nombre
    } for dependencia in dependencias]), 200


@app.route('/dependencias/<int:id_dependencia>', methods=['GET'])
def get_dependencia(id_dependencia):
    dependencia = Dependencia.query.get_or_404(id_dependencia)
    return jsonify({
        'ID': dependencia.ID,
        'Nombre': dependencia.Nombre
    }), 200


@app.route('/dependencias/<int:id_dependencia>', methods=['PUT'])
def update_dependencia(id_dependencia):
    dependencia = Dependencia.query.get_or_404(id_dependencia)
    data = request.get_json()
    dependencia.Nombre = data.get('Nombre', dependencia.Nombre)
    dependencia.fecha_modificacion = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Dependencia actualizada exitosamente'}), 200


@app.route('/dependencias/<int:id_dependencia>', methods=['DELETE'])
def delete_dependencia(id_dependencia):
    dependencia = Dependencia.query.get_or_404(id_dependencia)
    db.session.delete(dependencia)
    db.session.commit()
    return jsonify({'message': 'Dependencia eliminada exitosamente'}), 200


class TipoInduccion(db.Model):
    __tablename__ = 'TipoInduccion'
    ID = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<TipoInduccion {self.Nombre}>'


@app.route('/tipos_induccion', methods=['POST'])
def create_tipo_induccion():
    data = request.get_json()
    nombre = data.get('Nombre')
    new_tipo_induccion = TipoInduccion(Nombre=nombre)
    db.session.add(new_tipo_induccion)
    db.session.commit()
    return jsonify({'message': 'Tipo de inducción creado exitosamente'}), 201


@app.route('/tipos-induccion', methods=['GET'])
def get_tipos_induccion():
    tipos_induccion = TipoInduccion.query.all()
    return jsonify([{
        'ID': tipo_induccion.ID,
        'Nombre': tipo_induccion.Nombre
    } for tipo_induccion in tipos_induccion]), 200


@app.route('/tipos_induccion/<int:id_tipo_induccion>', methods=['GET'])
def get_tipo_induccion(id_tipo_induccion):
    tipo_induccion = TipoInduccion.query.get_or_404(id_tipo_induccion)
    return jsonify({
        'ID': tipo_induccion.ID,
        'Nombre': tipo_induccion.Nombre
    }), 200


@app.route('/tipos_induccion/<int:id_tipo_induccion>', methods=['PUT'])
def update_tipo_induccion(id_tipo_induccion):
    tipo_induccion = TipoInduccion.query.get_or_404(id_tipo_induccion)
    data = request.get_json()
    tipo_induccion.Nombre = data.get('Nombre', tipo_induccion.Nombre)
    tipo_induccion.fecha_modificacion = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Tipo de inducción actualizado exitosamente'}), 200


@app.route('/tipos_induccion/<int:id_tipo_induccion>', methods=['DELETE'])
def delete_tipo_induccion(id_tipo_induccion):
    tipo_induccion = TipoInduccion.query.get_or_404(id_tipo_induccion)
    db.session.delete(tipo_induccion)
    db.session.commit()
    return jsonify({'message': 'Tipo de inducción eliminado exitosamente'}), 200


class Evento(db.Model):
    ID = db.Column(db.String, primary_key=True)
    Nombre = db.Column(db.String, nullable=False)
    TipoInduccionID = db.Column(db.Integer, db.ForeignKey('TipoInduccion.ID'))
    Duracion = db.Column(db.Numeric, nullable=False)
    MedidaDuracion = db.Column(db.String)
    Autoregistro = db.Column(db.Integer)
    FechaHoraInicio = db.Column(db.String)
    FechaHoraTerminacion = db.Column(db.String)
    Tematica = db.Column(db.String)
    Instructor = db.Column(db.String, db.ForeignKey('instructor.Identificacion'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/eventos', methods=['POST'])
def create_evento():
    data = request.get_json()
    evento = Evento(
        ID=str(uuid()),
        Nombre=data.get('Nombre'),
        TipoInduccionID=data.get('TipoInduccionID'),
        Duracion=data.get('Duracion'),
        MedidaDuracion=data.get('MedidaDuracion'),
        Autoregistro=data.get('Autoregistro'),
        FechaHoraInicio=datetime.fromisoformat(data.get('FechaHoraInicio')).strftime('%Y-%m-%d %H:%M:%S'),
        FechaHoraTerminacion=datetime.fromisoformat(data.get('FechaHoraTerminacion')).strftime('%Y-%m-%d %H:%M:%S'),
        Tematica=data.get('Tematica'),
        Instructor=None
    )
    db.session.add(evento)
    db.session.commit()
    return jsonify({'message': 'Evento creado exitosamente'}), 201


@app.route('/eventos', methods=['GET'])
def get_eventos():
    eventos = Evento.query.all()
    return jsonify([{
        'ID': evento.ID,
        'Nombre': evento.Nombre,
        'TipoInduccion': TipoInduccion.query.get(evento.TipoInduccionID).Nombre,
        'Duracion': evento.Duracion,
        'MedidaDuracion': evento.MedidaDuracion,
        'Autoregistro': evento.Autoregistro,
        'FechaHoraInicio': evento.FechaHoraInicio,
        'FechaHoraTerminacion': evento.FechaHoraTerminacion,
        'Tematica': evento.Tematica,
        'Instructor': evento.Instructor,
        'NombreInstructor': Persona.query.get(evento.Instructor).Nombre if evento.Instructor else 'No asignado'
    } for evento in eventos]), 200


@app.route('/eventos/<id>', methods=['GET'])
def get_evento(id):
    evento = Evento.query.get_or_404(id)
    return jsonify({
        'ID': evento.ID,
        'Nombre': evento.Nombre,
        # Incluye otros campos según necesites
    }), 200


@app.route('/eventos/persona/<identificacion>', methods=['GET'])
def get_eventos_persona(identificacion):
    eventos = EventoPersona.query.filter_by(PersonaIdentificacion=identificacion).all()

    eventos_asociados = [Evento.query.get(evento.EventoID) for evento in eventos]

    return jsonify([{
        'ID': evento.ID,
        'Nombre': evento.Nombre,
        'TipoInduccion': TipoInduccion.query.get(evento.TipoInduccionID).Nombre,
        'Duracion': evento.Duracion,
        'MedidaDuracion': evento.MedidaDuracion,
        'FechaHoraInicio': evento.FechaHoraInicio,
        'FechaHoraTerminacion': evento.FechaHoraTerminacion,
        'Tematica': evento.Tematica,
        'NombreInstructor': Persona.query.get(evento.Instructor).Nombre if evento.Instructor else 'No asignado'
    } for evento in eventos_asociados]), 200


@app.route('/eventos/<id>', methods=['PUT'])
def update_evento(id):
    evento = Evento.query.get_or_404(id)
    data = request.get_json()
    evento.Nombre = data.get('Nombre', evento.Nombre)
    # Actualiza otros campos según necesites
    evento.fecha_modificacion = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Evento actualizado exitosamente'}), 200


@app.route('/eventos/<id>', methods=['DELETE'])
def delete_evento(id):
    evento_dependencias = EventoDependencia.query.filter_by(EventoID=id).all()
    for relacion in evento_dependencias:
        db.session.delete(relacion)

    evento_personas = EventoPersona.query.filter_by(EventoID=id).all()
    for relacion in evento_personas:
        db.session.delete(relacion)
    
    evento = Evento.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()
    return jsonify({'message': 'Evento eliminado exitosamente'}), 200


class EventoDependencia(db.Model):
    __tablename__ = 'evento_dependencia'
    EventoID = db.Column(db.String, db.ForeignKey('evento.ID'), primary_key=True)
    DependenciaID = db.Column(db.Integer, db.ForeignKey('dependencia.ID'), primary_key=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow)

    evento = db.relationship('Evento', backref=db.backref('dependencias_asociadas', lazy='dynamic'))
    dependencia = db.relationship('Dependencia', backref=db.backref('eventos_asociados', lazy='dynamic'))


@app.route('/evento_dependencia', methods=['POST'])
def create_evento_dependencia():
    data = request.get_json()
    new_evento_dependencia = EventoDependencia(
        EventoID=data['EventoID'],
        DependenciaID=data['DependenciaID']
    )
    db.session.add(new_evento_dependencia)
    db.session.commit()
    return jsonify({'message': 'Relación evento-dependencia creada exitosamente'}), 201


@app.route('/evento_dependencia', methods=['GET'])
def get_evento_dependencias():
    relaciones = EventoDependencia.query.all()
    return jsonify([{
        'EventoID': relacion.EventoID,
        'DependenciaID': relacion.DependenciaID
    } for relacion in relaciones]), 200


class EventoPersona(db.Model):
    __tablename__ = 'evento_persona'
    EventoID = db.Column(db.String, db.ForeignKey('evento.ID'), primary_key=True)
    PersonaIdentificacion = db.Column(db.String, db.ForeignKey('persona.Identificacion'), primary_key=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow)

    evento = db.relationship('Evento', backref=db.backref('personas_asociadas', lazy='dynamic'))
    persona = db.relationship('Persona', backref=db.backref('eventos_asociados', lazy='dynamic'))


@app.route('/evento_persona', methods=['POST'])
def create_evento_persona():
    data = request.get_json()
    new_evento_persona = EventoPersona(
        EventoID=data['EventoID'],
        PersonaIdentificacion=data['PersonaIdentificacion']
    )
    db.session.add(new_evento_persona)
    db.session.commit()
    return jsonify({'message': 'Relación evento-persona creada exitosamente'}), 201


@app.route('/evento_personas', methods=['POST'])
def create_evento_personas():
    data = request.get_json()
    evento_id = data.get('EventoID')    
    personas = data.get('Personas')

    for persona in personas:
        new_evento_persona = EventoPersona(
            EventoID=evento_id,
            PersonaIdentificacion=persona
        )

        persona = Persona.query.filter_by(Identificacion=persona).first()
        email = persona.Email
        evento = Evento.query.get(evento_id)
        evento_nombre = evento.Nombre
        enviar_email(email, evento_nombre)

        db.session.add(new_evento_persona)
        db.session.commit()
    
    return jsonify({'message': 'Relaciones evento-persona creada exitosamente'}), 201


@app.route('/evento_persona', methods=['GET'])
def get_evento_personas():
    relaciones = EventoPersona.query.all()
    return jsonify([{
        'EventoID': relacion.EventoID,
        'PersonaIdentificacion': relacion.PersonaIdentificacion
    } for relacion in relaciones]), 200


@app.route('/evento_persona/<id_evento>', methods=['GET'])
def get_evento_personas_asociadas(id_evento):
    evento = Evento.query.get_or_404(id_evento)
    personas_asociadas = [serializar_persona(Persona.query.get_or_404(persona.PersonaIdentificacion)) for persona in evento.personas_asociadas]
    personas_no_asociadas = [serializar_persona(persona) for persona in Persona.query.all() if persona.Identificacion not in personas_asociadas]

    for persona in personas_asociadas:
        cargo = Cargo.query.get(persona['Cargo'])
        rol = Rol.query.get(persona['Rol'])
        persona['Cargo'] = cargo.Nombre
        persona['Rol'] = rol.Nombre
    
    for persona in personas_no_asociadas:
        cargo = Cargo.query.get(persona['Cargo'])
        rol = Rol.query.get(persona['Rol'])
        persona['Cargo'] = cargo.Nombre
        persona['Rol'] = rol.Nombre

    return jsonify({
        'asociadas': personas_asociadas,
        'noAsociadas': personas_no_asociadas
    }), 200


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('Email')
    clave = Usuario.hash_password(data.get('Clave'))
    usuario = Usuario.query.filter_by(Email=email).first()

    if usuario:
        instructor = Instructor.query.filter_by(Email=email).first()

        tipo_usuario = {}

        if instructor:
            tipo_usuario['Tipo'] = 'Instructor'
            tipo_usuario['Identificacion'] = instructor.Identificacion
            tipo_usuario['Rol'] = instructor.Rol
            tipo_usuario['Estado'] = instructor.Estado
        else:
            persona = Persona.query.filter_by(Email=email).first()
            tipo_usuario['Tipo'] = 'Usuario'
            tipo_usuario['Identificacion'] = persona.Identificacion
            tipo_usuario['Rol'] = persona.Rol
            tipo_usuario['Cargo'] = persona.Cargo
        
        if usuario and usuario.Clave == clave:
            return jsonify(tipo_usuario), 200
    else:
        return jsonify({'message': 'Credenciales inválidas'}), 401


@app.route('/firma/<id>')
def imagen(id):
    """
    Función para obtener una imagen desde el directorio 'imagenes'.

    Args:
        id (str): Nombre del archivo de imagen.
    
    Returns:
        tuple: Tupla con la imagen, el código de estado y el tipo de contenido.
    """
    try:
        imagen = open(os.path.join('static', 'images', f'{id}.png'), 'rb').read()
    except FileNotFoundError:
        imagen = open(os.path.join('static', 'images', 'sin_firma.png'), 'rb').read()
    
    return imagen, 200, {'Content-Type': 'image/png'}


@app.route('/firmar', methods=['POST'])
def guardar_firma():
    data = request.json
    evento_id = data.get('EventoID')
    identificacion = data.get('Identificacion')
    firma = data.get('Firma')

    with open(os.path.join('static', 'images', f'{evento_id};{identificacion}.png'), 'wb') as file:
        file.write(base64.b64decode(firma.split(',')[1]))

    return jsonify({'message': 'Firma registrada correctamente'}), 200


@app.route('/registrar_instructor', methods=['POST'])
def registrar_instructor():
    data = request.get_json()
    evento_id = data.get('EventoID')
    instructor_identificacion = data.get('InstructorIdentificacion')

    evento = Evento.query.get_or_404(evento_id)
    evento.Instructor = instructor_identificacion
    db.session.commit()

    return jsonify({'message': 'Instructor registrado exitosamente'}), 200


def enviar_email(email, evento):
    """
    Función para enviar un correo electrónico.

    Args:
        email (str): Dirección de correo electrónico.
        evento (Evento): Instancia de Evento.
    
    Returns:
        str: Mensaje de éxito o error al enviar el correo.
    """
    msg = Message(f'¡Registro en evento {evento}!',
                  sender="your-email@debugmail.io",
                  recipients=[email],
                  body=f'¡Hola! Te informamos que has sido registrado en el evento {evento}. ¡Te esperamos!. Vaya a la página de inicio de sesión para firmar su asistencia: http://localhost:5000/')
    try:
        mail.send(msg)
        return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email: {e}"


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
