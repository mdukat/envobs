FROM python@sha256:d1fd807555208707ec95b284afd10048d0737e84b5f2d6fdcbed2922b9284b56

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./envobserverserver.py ./

EXPOSE 8080

CMD ["python", "envobserverserver.py"]
