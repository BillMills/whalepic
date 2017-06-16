FROM python:2.7

RUN pip install Flask
COPY . /app

ENV FLASK_APP=whalepic.py
WORKDIR /app
CMD ["python", "whalepic.py"]
