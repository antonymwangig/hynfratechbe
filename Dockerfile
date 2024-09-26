FROM python:3.12-bookworm

WORKDIR /opt/hyn

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH .

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && apt-get install -y libvirt-dev \
    && apt-get install -y libvirt-clients libvirt-daemon-system qemu-kvm \
    && apt-get install -y qemu-utils \
    && apt-get clean 
RUN apt-get install -y build-essential
COPY ./requirements.txt /opt/hyn/
RUN pip install --no-cache-dir -r requirements.txt

COPY .  /opt/hyn/

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py setup_roles && python manage.py populate_service_plans && python manage.py runserver 0.0.0.0:8000"]
