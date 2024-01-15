FROM postgres:latest

ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=admin
ENV POSTGRES_DB=srealitydb

COPY create_db.sql /docker-entrypoint-initdb.d

EXPOSE 5432

CMD ["postgres"]
