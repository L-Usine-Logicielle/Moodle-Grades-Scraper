FROM python:3.9-alpine

WORKDIR /app
COPY . /app

RUN addgroup --gid 1001 moodle \
    && adduser --uid 1001 --disabled-password --no-create-home --ingroup moodle moodle \
    && apk update \
    && pip install -e .

USER moodle

CMD ["python", "application/main.py"]