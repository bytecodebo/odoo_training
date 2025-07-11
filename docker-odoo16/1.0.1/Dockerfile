FROM odoo:16.0
SHELL ["/bin/bash", "-xo", "pipefail", "-c"]
USER root

COPY ./resources/requirements-advance.txt /tmp/.

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements-advance.txt
# RUN pip install --no-cache-dir -r /opt/odoo/extra_requirements.txt
# Set default user when running the container
USER odoo

ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]

# docker build --platform=linux/amd64 -t {user|account}/{image-name}:{tag} .
# docker build --platform=linux/amd64 -t robertsvx38/odoo-training:16.1.0.1
