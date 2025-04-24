FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN apk upgrade --update
RUN apk add --no-cache build-base gcc gdal gdal-dev zlib
RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
RUN export C_INCLUDE_PATH=/usr/include/gdal
RUN export LDFLAGS="-L/usr/local/opt/zlib/lib"
RUN export CPPFLAGS="-I/usr/local/opt/zlib/include"
RUN pip install --no-cache-dir

RUN git clone https://github.com/ctoruno/eu-rol-tracker-dashboard.git .

RUN pip install -r requirements.txt

CMD ["sh", "-c", "streamlit run app.py --server.port=8501 --server.address=0.0.0.0"]
