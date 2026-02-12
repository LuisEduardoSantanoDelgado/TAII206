FROM python:3.12-slim

#crear una carpeta de trabajo
WORKDIR /app

#Copiar requerimientos
COPY requerimients.txt .

#instalados
RUN pip install --no-cache-dir -r requerimients.txt

#copiar el codigo del proyecto
COPY ./app ./app

#Exponer el puerto
EXPOSE 5000

#Comandos para ejecutar FASTAPI
CMD [ "uvicorn","app.main:app","--host","0.0.0.0","--port","5000", "--reload" ]

