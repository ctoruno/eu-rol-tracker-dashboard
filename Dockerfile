FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install gdal==3.10.1

RUN git clone https://github.com/ctoruno/eu-rol-tracker-dashboard.git .

RUN pip3 install -r requirements.txt

CMD ["sh", "-c", "streamlit run app.py --server.port=8501 --server.address=0.0.0.0"]
