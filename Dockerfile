FROM python:3.11-slim

# install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libegl1 \
    libglib2.0-0 \
    libxkbcommon-x11-0 \
    libxcb-cursor0 \
    libdbus-1-3 \
    libx11-xcb1 \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

# set wd
WORKDIR /app

COPY . /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV QT_QPA_PLATFORM=xcb

CMD ["python", "main.py"]
