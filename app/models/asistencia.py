from ..extensions import db

class Asistencia(db.Model):
    __tablename__ = "asistencia"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hora = db.Column(db.Time, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    materia_horario_curso_paralelo_id = db.Column(db.Integer, db.ForeignKey("materia_horario_curso_paralelo.id"), nullable=False)