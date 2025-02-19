FROM ubuntu:latest
RUN apt-get update && apt-get install -y \
    curl \
    sudo \
    supervisor \
    && apt-get clean



RUN curl https://clickhouse.com/ | sh
RUN ./clickhouse install

COPY ./docker_config/config.xml /etc/clickhouse-server/config.xml
COPY ./docker_config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./docker_config/users.xml /etc/clickhouse-server/users.xml


EXPOSE 8123 9000 9009

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]