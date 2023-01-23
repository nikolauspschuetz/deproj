FROM bitnami/python:3.11.1 as main

RUN apt-get update && \
    apt-get install -y autoconf automake libtool jq

ARG PYTHON_BASE_IMAGE="bitnami/python:3.11-slim"

ENV PYTHON_BASE_IMAGE=${PYTHON_BASE_IMAGE} \
    DEBIAN_FRONTEND='noninteractive LANGUAGE=C.UTF-8 LANG=C.UTF-8 LC_ALL=C.UTF-8 LC_CTYPE=C.UTF-8 LC_MESSAGES=C.UTF-8'

COPY ./docker /app/deproj/docker

RUN python -m pip install -r "/app/deproj/docker/requirements.txt"

COPY requirements_dev.txt /app/deproj/requirements_dev.txt
COPY src /app/deproj/src
COPY setup.py /app/deproj/setup.py

ENV PYTHONPATH=/app/deproj/src

RUN python -m pip install -e /app/deproj

ENTRYPOINT ["/app/deproj/docker/entrypoint.sh"]

CMD ["deproj"]

FROM main as test
COPY tests /app/deproj/tests
COPY Makefile /app/deproj
RUN python -m pip install -e '/app/deproj[test]'

WORKDIR /app/deproj
CMD ["make", "test"]
