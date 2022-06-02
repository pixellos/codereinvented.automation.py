FROM python:3.10.0-slim


WORKDIR /usr/src/app

COPY linux-packages.txt linux-packages.txt
RUN apt-get update && \
  apt-get install -yq --no-install-recommends \
  $(grep -vE '^#' linux-packages.txt) && \
  rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-input && rm requirements.txt

COPY . .

CMD [ "python", "./main.py" ]