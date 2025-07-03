FROM odoo:16.0

USER root

RUN apt-get update && apt-get install -y zip

COPY ./resources/requirements-advance.txt /tmp/.
COPY ./resources/requirements.txt /tmp/.

RUN pip install --upgrade pip \
    && pip install -r /tmp/requirements.txt

RUN mkdir -p /opt/odoo/backups \
    && chown -R odoo /opt/odoo/backups

VOLUME ["/opt/odoo/backups"]
# Set default user when running the container

USER odoo

#ENTRYPOINT ["/entrypoint.sh"]

#CMD ["odoo"]

# docker buildx --platform=linux/amd64 --force-rm -t robertsvx38/odoo-training:16.0.1 .
# docker build --force-rm -t robertsvx38/odoo-training:16.0.1 .
