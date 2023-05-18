FROM python:3.11.2-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "app.py"]
