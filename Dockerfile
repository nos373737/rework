FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY . /app
WORKDIR /app
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt --proxy=10.49.0.50:8080


EXPOSE 5000

CMD ["python", "run.py"]
