FROM python:3.11-slim


WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["flask", "--app", "main", "run", "--host=0.0.0.0", "--port=5000"]  

#CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]

#







