from app.seeders.user_seeder import seed_users
from app.seeders.rol_seeder import seed_roles
from app.seeders.hora_seeder import seed_horarios
from app.seeders.dia_seeder import seed_dias
from app.seeders.dia_horario_seeder import seed_dia_horarios
from app.seeders.materia_seeder import seed_materias
from app.seeders.curso_seeder import seed_cursos
from app.seeders.paralelo_seeder import seed_paralelos
from app.seeders.gestion_seeder import seed_gestion
from app.seeders.curso_paralelo import seed_curso_paralelo
from app.seeders.gestion_curso_paralelo import seed_gestion_curso_paralelo
from app.seeders.subgestion_seeder import seed_subgestiones
from app.seeders.profesor_seeder import seed_profesores
from app.seeders.apoderado_seeder import seed_apoderados
from app.seeders.estudiante_seeder import seed_estudiantes
from app.seeders.parentesco_seeder import seed_parentescos
from app.seeders.matricula_seeder import seed_matriculas


def run_all_seeders():
    seed_roles()
    seed_users()
    seed_horarios()
    seed_dias()
    seed_dia_horarios()
    seed_materias()
    seed_cursos()
    seed_paralelos()
    seed_gestion()
    seed_curso_paralelo()
    seed_gestion_curso_paralelo()
    seed_subgestiones()
    seed_profesores()
    seed_apoderados()
    seed_estudiantes()
    seed_parentescos()
    seed_matriculas()