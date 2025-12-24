FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

WORKDIR /app
RUN apt-get update && apt-get install -y python3.10 python3-pip
RUN ln -s /usr/bin/python3 /usr/bin/python

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
COPY rc_xi_large_dataset.jsonl .

CMD ["python", "app.py"]
