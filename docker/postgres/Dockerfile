FROM postgres:latest

EXPOSE 5432

ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword
ENV POSTGRES_DB=mydb

COPY init.sql /docker-entrypoint-initdb.d/