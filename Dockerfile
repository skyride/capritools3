FROM python:3.8

WORKDIR /app

RUN pip install --no-cache-dir uWSGI==2.0.18

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy files
COPY . /app

# Collectstatic, fake these values because they're required even though
# we don't use them.
ARG SECRET_KEY=collectstatic
ARG DB_HOST=
ARG DB_NAME=
ARG DB_USER=
ARG DB_PASSWORD=
ARG REDIS_URL=
RUN ./manage.py collectstatic

# Ops Parameters
ENV WORKERS=2
ENV PORT=8000

CMD uwsgi --http :${PORT} --processes ${WORKERS} --static-map /static=/static --module capritools.wsgi:application
