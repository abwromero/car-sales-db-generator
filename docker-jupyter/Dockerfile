FROM jupyter/minimal-notebook:python-3.11

WORKDIR /projects

USER root

RUN pip install faker psycopg2-binary

USER $NB_UID