# 1) Base image
FROM python:3.11-slim

# 2) Directorio de trabajo
WORKDIR /app

# 3) Dependencias del sistema (psycopg2, mysqlclient…)
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    libpq-dev \
    pkg-config \
    build-essential \
  && rm -rf /var/lib/apt/lists/*

# 4) Copiamos requirements e instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5) Copiamos TODO el código de tu proyecto
COPY . .

# 6) Variables de entorno para que Flask encuentre tu app
#    - manage:app  => módulo manage.py y variable app dentro
ENV FLASK_APP=manage:app
ENV FLASK_ENV=production

# 7) Puerto dinámico (Railway lo inyecta en $PORT)
ENV PORT=${PORT:-5000}
EXPOSE ${PORT}

# 8) Arrancamos Flask en producción, host y puerto dinámico
#    Usamos shell form para que expanda $PORT
ENTRYPOINT flask run --host=0.0.0.0 --port=$PORT
