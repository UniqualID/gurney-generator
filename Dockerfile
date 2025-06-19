FROM python:3.10-slim

RUN apt update && apt install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir flask flask-cors gtts pydub

ENV PORT=8080
EXPOSE 8080

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
