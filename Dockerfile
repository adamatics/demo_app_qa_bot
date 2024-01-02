FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

EXPOSE 5000

COPY . /app

# Define the environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV FLASK_RUN_DEBUG=false
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]