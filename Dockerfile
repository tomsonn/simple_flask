FROM python:3.8-alpine

WORKDIR /simpleflask
COPY . /simpleflask

RUN pip3 install --upgrade pip && \
	pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["./run.py"]
