FROM odoo:16.0

USER root

RUN apt-get update && apt-get install -y \
    nano \
    zip

COPY ./resources/requirements-advance.txt /opt/odoo/.

RUN pip install --upgrade pip \
    && pip install -r /odoo/requirements-advance.txt

RUN mkdir -p /opt/odoo/backups \
    && chown -R odoo /opt/odoo/backups

VOLUME ["/opt/odoo/backups"]
# Set default user when running the container

USER odoo

#ENTRYPOINT ["/entrypoint.sh"]

#CMD ["odoo"]

# docker build --force-rm -t robertsvx38/odoo-training:16.0.1 .

