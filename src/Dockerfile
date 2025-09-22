# Usa una imagen base de Python oficial.
# Esta es una imagen ligera de Python ideal para aplicaciones web.
FROM python:3.12-slim-bookworm

# Establece el directorio de trabajo dentro del contenedor.
WORKDIR /src

# Copia los archivos de requerimientos e instala las dependencias.
# Esto es más eficiente, ya que Docker cachea este paso.
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación.
COPY . .

# Expone el puerto 9000 del contenedor.
EXPOSE 9000

# Define el comando que se ejecutará al iniciar el contenedor.
# Usa Gunicorn para un servidor de producción simple y robusto.
# El --bind 0.0.0.0:9000 es crucial para que el servidor escuche en todas las interfaces, no solo en localhost.
CMD ["gunicorn", "--bind", "0.0.0.0:9000", "api:app"]