FROM python:3.7

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV ENV=dev
ENV WORKERS=2
ENV PORT=80

CMD gunicorn -w ${WORKERS} -b 0.0.0.0:${PORT} capritools.wsgi:application