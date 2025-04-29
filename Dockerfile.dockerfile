FROM python:3.10
WORKDIR /app
COPY app /app
COPY index.pkl /app/index.pkl
RUN pip install -r requirements.txt
CMD ["flask", "--app", "main", "run", "--host=0.0.0.0", "--port=8080"]