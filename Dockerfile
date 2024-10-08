FROM pytorch/pytorch:latest as builder

RUN pip install poetry

COPY . .

RUN poetry install

ENTRYPOINT ["poetry", "run", "python", "-m", "main"]