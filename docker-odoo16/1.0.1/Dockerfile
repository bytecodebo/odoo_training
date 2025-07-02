FROM odoo:16.0

USER root

COPY ./resources/requirements-advance.txt .


# Set default user when running the container
USER odoo

ENTRYPOINT ["/entrypoint.sh"]

CMD ["odoo"]
