# fluentd/Dockerfile
FROM fluent/fluentd:v1.12.0-debian-1.0

USER root  # Use root user to install software

USER fluent

COPY conf/fluent.conf /fluentd/etc/
CMD ["fluentd", "-c", "/fluentd/etc/fluent.conf"]