# Usa la imagen oficial de Python en su variante slim
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Instalamos dependencias del sistema necesarias para psycopg2, mysqlclient, etc.
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    libpq-dev \
    pkg-config \
    build-essential \
  && rm -rf /var/lib/apt/lists/*

# Copiamos el requirements e instalamos las dependencias de Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# Definimos variables de entorno para producción
ENV FLASK_APP=manage.py
ENV FLASK_ENV=production
# Railway inyecta el puerto en $PORT; usamos 5000 por defecto si no existe
ENV PORT=${PORT:-5000}

# Exponemos el puerto de la aplicación
EXPOSE ${PORT}

# Arrancamos con Gunicorn vinculando al puerto dinámico
CMD ["gunicorn", "manage:app", "--bind", "0.0.0.0:${PORT}", "--workers", "3"]
