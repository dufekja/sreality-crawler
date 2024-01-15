FROM postgres:latest

ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=admin
ENV POSTGRES_DB=srealitydb

COPY src/database/create.sql /docker-entrypoint-initdb.d

EXPOSE 5432

CMD ["postgres"]
