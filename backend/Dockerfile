# Imagen base oficial de Python
FROM python:3.13-slim

# Crear directorio de trabajo dentro del contenedor
WORKDIR /backend

# El compose tiene un volumen que mapea el directorio actual al contenedor por lo que run.py deberia de sobreescribirse al modificarlo
# Aún así, requerimos copiar el requirements.txt y run.py al contenedor porque la imagen se construye antes de que el contenedor se ejecute

# Copiar requirements.txt y run.py al contenedor
COPY requirements.txt .
COPY run.py .

# Instalar dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto para ejecutar el script principal
CMD ["python", "run.py"]