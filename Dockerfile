FROM python:3.10
COPY ./Arquivos/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . ./app
WORKDIR /app
CMD ["bash", "/scripts/execute.sh"]
