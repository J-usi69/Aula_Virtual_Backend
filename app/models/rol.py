from ..extensions import db

class Rol(db.Model):
    __tablename__ = "rol"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)