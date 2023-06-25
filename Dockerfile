FROM jupyter/minimal-notebook:python-3.11

WORKDIR /projects

USER root

RUN pip install selenium beautifulsoup4 faker pandas matplotlib scikit-learn psycopg2-binary

USER $NB_UID