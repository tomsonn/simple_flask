FROM python:3.8-alpine

COPY . .

RUN pip3 install --upgrade pip && \
	pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "run.py"]
