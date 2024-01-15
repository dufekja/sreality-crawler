FROM python:3.10

WORKDIR /

RUN apt update && apt install --yes postgresql

# copy deps
COPY requirements.txt requirements.txt
COPY pyproject.toml pyproject.toml
COPY conf/ conf/
COPY src/server/ src/server/
COPY src/database/ src/database/

# install requirements
RUN python -m pip install --upgrade -r requirements.txt --no-cache-dir

EXPOSE 8080

CMD ["uvicorn", "src.server.server:app", "--host", "0.0.0.0", "--port", "8080"]
