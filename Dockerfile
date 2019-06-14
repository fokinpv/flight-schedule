FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1
RUN apt-get clean && apt-get update && apt-get install -y locales --no-install-recommends \
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/;s/# fa_IR UTF-8/fa_IR UTF-8/' /etc/locale.gen \
    && locale-gen \
    && rm -rf /var/lib/apt/lists/*
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
COPY ./requirements.txt ./deployments/entrypoint.sh /
COPY . /app
RUN pip install -r /requirements.txt \
    && groupadd -r django \
    && useradd -r -g django django \
    && chown -R django /app \
    && sed -i 's/\r//' /entrypoint.sh \
    && chmod +x /entrypoint.sh

WORKDIR /app
RUN mkdir /app/media \
    && mkdir /app/static \
    && chown -R django.django /app/static \
    && chown -R django.django /app/media

ENTRYPOINT ["/entrypoint.sh"]
