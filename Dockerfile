FROM python:3.8.5-slim-buster

RUN mkdir /api_service
RUN useradd -m service

COPY --chown=service:service main.py /api_service
COPY --chown=service:service ./project/ /api_service/project

RUN pip install --upgrade pip
RUN pip install -r api_service/project/requirements.txt

WORKDIR /api_service
USER service
EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
