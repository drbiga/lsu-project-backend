FROM python:3.10

WORKDIR /app

RUN pip install requests

COPY ./initialize_repositories.py .

CMD [ "python", "initialize_repositories.py" ]
