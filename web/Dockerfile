FROM python:3.12-slim

# Crear carpeta de trabajo
WORKDIR /myapi

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . .

# Exponer puerto Flask
EXPOSE 8000

# Comando para correr la app
CMD ["python", "run.py"]
