# Usa la variante slim de Python 3.11
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalamos librerías del sistema necesarias para psycopg2 y mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    libpq-dev \
    pkg-config \
    build-essential \
  && rm -rf /var/lib/apt/lists/*

# Copiamos el archivo de dependencias y lo instalamos
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de tu código
COPY . .

# Variables de entorno para Flask
ENV FLASK_APP=manage.py
ENV FLASK_ENV=production

# Railway (y otras plataformas) inyectan el puerto en $PORT
# Si no existe, cae al 5000 por defecto
ENV PORT=${PORT:-5000}

# Exponemos el puerto configurado
EXPOSE ${PORT}

# Arrancamos el servidor de Flask en el puerto dinámico
# Usamos shell form para que $PORT se expanda correctamente
ENTRYPOINT flask run --host=0.0.0.0 --port=$PORT
