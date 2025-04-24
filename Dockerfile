FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/ctoruno/eu-rol-tracker-dashboard.git .

RUN pip install -r requirements.txt

CMD ["sh", "-c", "streamlit run 0_Home.py --server.port=8501 --server.address=0.0.0.0"]
