# Użyj oficjalnego obrazu Python jako obrazu bazowego
FROM python:3.9-slim

# Ustaw zmienne środowiskowe, aby zapobiec tworzeniu plików .pyc i buforowaniu outputu
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Ustaw katalog roboczy w kontenerze
WORKDIR /code

# Zainstaluj zależności systemowe potrzebne dla mysqlclient ORAZ pkg-config
RUN apt-get update && apt-get install -y default-libmysqlclient-dev gcc pkg-config

# Skopiuj plik z zależnościami i zainstaluj je
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj resztę kodu aplikacji do katalogu roboczego
COPY . /code/