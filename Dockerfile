FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src ./src
RUN mkdir data

EXPOSE 8000

CMD [ "python", "src/main.py" ]
