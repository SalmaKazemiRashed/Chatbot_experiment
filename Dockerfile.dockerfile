FROM python:3.11-slim

# Install necessary system dependencies
RUN apt-get update && apt-get install -y git gcc g++ && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download Hugging Face model (optional but recommended for local speed)
# Replace 'google/flan-t5-large' with your actual model if different
RUN python -c "from transformers import AutoTokenizer, AutoModelForSeq2SeqLM; AutoTokenizer.from_pretrained('google/flan-t5-large'); AutoModelForSeq2SeqLM.from_pretrained('google/flan-t5-large')"

EXPOSE 5000

# Run the Flask app using gunicorn for production-like behavior
#CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]


CMD ["flask", "--app", "main", "run", "--host=0.0.0.0", "--port=8080"]  

#CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]





