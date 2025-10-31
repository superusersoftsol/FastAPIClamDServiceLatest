FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    clamav-daemon \
    python3 python3-pip supervisor \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY app/ /app/app/
COPY requirements.txt .
COPY clamd.conf /etc/clamav/clamd.conf
COPY supervisord.conf /etc/supervisord.conf

RUN pip3 install --no-cache-dir -r requirements.txt

RUN mkdir -p /clamav /defs /var/lib/clamav && chown -R root:root /clamav /defs

EXPOSE 8000 3310

ENV CLAMAV_DB_DIR=/defs \    CLAMAV_SCAN_PATH=/clamav \    MAX_BYTES=4000000000 \    LOG_LEVEL=INFO

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
