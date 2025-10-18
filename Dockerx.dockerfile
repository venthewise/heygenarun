FROM ubuntu:22.04

# Install FFmpeg and wget
RUN apt-get update && \
    apt-get install -y ffmpeg wget python3 python3-pip && \
    apt-get clean

# Install Flask for a simple API
RUN pip3 install flask

WORKDIR /app

# Copy the API script
COPY app.py /app/app.py

EXPOSE 8080

CMD ["python3", "app.py"]
