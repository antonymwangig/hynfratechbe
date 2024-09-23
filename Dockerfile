FROM python:3.12-bookworm

WORKDIR /opt/hyn

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH .

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && apt-get install -y libvirt-dev \
    && apt-get clean 

COPY ./requirements.txt /opt/hyn/
RUN pip install --no-cache-dir -r requirements.txt

COPY .  /opt/hyn/

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 8000"]
