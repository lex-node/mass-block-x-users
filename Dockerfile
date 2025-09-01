FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install Flask
ENV FLASK_APP=web_app.py
CMD ["flask", "run", "--host=0.0.0.0"]
