FROM python:3.10

WORKDIR /

# install python and postgres
RUN apt update && apt install --yes postgresql

# copy deps
COPY requirements.txt requirements.txt
COPY pyproject.toml pyproject.toml
COPY conf/ conf/
COPY src/crawler/ src/crawler/

# install requirements
RUN python -m pip install --upgrade -r requirements.txt --no-cache-dir
RUN playwright install-deps
RUN playwright install chromium

ENTRYPOINT ["python", "src/crawler/crawler.py"]