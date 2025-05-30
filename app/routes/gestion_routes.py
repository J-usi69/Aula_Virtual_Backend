from flask import Blueprint, jsonify
from sqlalchemy.orm import joinedload
from ..extensions import db
from ..models.gestion import Gestion
from ..models.gestion_curso_paralelo import GestionCursoParalelo
from ..models.curso_paralelo import CursoParalelo
from ..models.curso import Curso
from ..models.paralelo import Paralelo
from ..models.materia_horario_curso_paralelo import MateriaHorarioCursoParalelo
from ..models.materia_profesor_dia_horario import MateriaProfesorDiaHorario
from ..models.materia_profesor import MateriaProfesor
from ..models.profesor import Profesor
from ..models.user import User
from ..models.materia import Materia
from ..models.dia_horario import DiaHorario
from ..models.dia import Dia
from ..models.horario import Horario

gestion_bp = Blueprint('gestion_bp', __name__)

@gestion_bp.route('/listar-estructura', methods=['GET'])
def listar_estructura_gestion():
    gestiones = Gestion.query.options(
        joinedload(Gestion.gestion_curso_paralelos)
        .joinedload(GestionCursoParalelo.curso_paralelo)
        .joinedload(CursoParalelo.curso),

        joinedload(Gestion.gestion_curso_paralelos)
        .joinedload(GestionCursoParalelo.curso_paralelo)
        .joinedload(CursoParalelo.paralelo),

        joinedload(Gestion.gestion_curso_paralelos)
        .joinedload(GestionCursoParalelo.materia_horario_curso_paralelo_rel)
        .joinedload(MateriaHorarioCursoParalelo.materia_profesor_dia_horario)
        .joinedload(MateriaProfesorDiaHorario.materia_profesor)
        .joinedload(MateriaProfesor.profesor_rel)
        .joinedload(Profesor.user_profesor),

        joinedload(Gestion.gestion_curso_paralelos)
        .joinedload(GestionCursoParalelo.materia_horario_curso_paralelo_rel)
        .joinedload(MateriaHorarioCursoParalelo.materia_profesor_dia_horario)
        .joinedload(MateriaProfesorDiaHorario.materia_profesor)
        .joinedload(MateriaProfesor.materia),

        joinedload(Gestion.gestion_curso_paralelos)
        .joinedload(GestionCursoParalelo.materia_horario_curso_paralelo_rel)
        .joinedload(MateriaHorarioCursoParalelo.materia_profesor_dia_horario)
        .joinedload(MateriaProfesorDiaHorario.dia_horario)
        .joinedload(DiaHorario.dia),

        joinedload(Gestion.gestion_curso_paralelos)
        .joinedload(GestionCursoParalelo.materia_horario_curso_paralelo_rel)
        .joinedload(MateriaHorarioCursoParalelo.materia_profesor_dia_horario)
        .joinedload(MateriaProfesorDiaHorario.dia_horario)
        .joinedload(DiaHorario.horario)
    ).all()

    resultado = []
    for g in gestiones:
        gestion_dict = {
            "gestion_id": g.id,
            "nombre": g.nombre,
            "cursos_paralelos": []
        }

        for gcp in g.gestion_curso_paralelos:
            cp = gcp.curso_paralelo
            curso_paralelo_dict = {
                "curso_paralelo_id": cp.id,
                "curso": cp.curso.nombre,
                "paralelo": cp.paralelo.nombre,
                "materias_asignadas": []
            }

            for mhcp in gcp.materia_horario_curso_paralelo_rel:
                mpdh = mhcp.materia_profesor_dia_horario
                mp = mpdh.materia_profesor
                materia = mp.materia
                profesor = mp.profesor_rel
                user = profesor.user_profesor
                dia = mpdh.dia_horario.dia
                horario = mpdh.dia_horario.horario

                curso_paralelo_dict["materias_asignadas"].append({
                    "materia_id": materia.id,
                    "materia_nombre": materia.nombre,
                    "profesor": {
                        "id": profesor.id,
                        "ci": profesor.ci,
                        "nombre": profesor.nombre,
                        "apellido": profesor.apellido,
                        "telefono": profesor.telefono,
                        "direccion": profesor.direccion,
                        "user": {
                            "id": user.id,
                            "name": user.name,
                            "email": user.email,
                            "photo_url": user.photo_url,
                            "status": user.status
                        }
                    },
                    "dia": dia.nombre,
                    "hora_inicio": horario.hora_inicio.strftime("%H:%M"),
                    "hora_final": horario.hora_final.strftime("%H:%M")
                })

            gestion_dict["cursos_paralelos"].append(curso_paralelo_dict)

        resultado.append(gestion_dict)

    return jsonify(resultado)

# Listar todos los registros
@gestion_bp.route('/listar', methods=['GET'])
def listar():
    gestiones = Gestion.query.all()
    result = [
        {
            "id": g.id,
            "nombre": g.nombre
        } for g in gestiones
    ]
    return jsonify(result), 200

# Buscar un registro por ID
@gestion_bp.route('/buscar/<int:id>', methods=['GET'])
def buscar(id):
    gestion = Gestion.query.get_or_404(id)
    result = {
        "id": gestion.id,
        "nombre": gestion.nombre
    }
    return jsonify(result), 200

# Crear un nuevo registro
@gestion_bp.route('/guardar', methods=['POST'])
def guardar():
    data = request.get_json()
    nueva_gestion = Gestion(
        nombre=data['nombre']
    )
    db.session.add(nueva_gestion)
    db.session.commit()
    return jsonify({"message": "Registro creado exitosamente"}), 201

# Actualizar un registro existente
@gestion_bp.route('/actualizar/<int:id>', methods=['PUT'])
def actualizar(id):
    data = request.get_json()
    gestion = Gestion.query.get_or_404(id)
    gestion.nombre = data.get('nombre', gestion.nombre)
    db.session.commit()
    return jsonify({"message": "Registro actualizado exitosamente"}), 200

# Eliminar un registro
@gestion_bp.route('/eliminar/<int:id>', methods=['DELETE'])
def eliminar(id):
    gestion = Gestion.query.get_or_404(id)
    db.session.delete(gestion)
    db.session.commit()
    return jsonify({"message": "Registro eliminado exitosamente"}), 200