FROM python:3.6

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN fabmanager create-admin --username admin --firstname admin --lastname flask --email admin@flask.org --password password
RUN python testdata.py

EXPOSE 5000

CMD ["python", "run.py"]
