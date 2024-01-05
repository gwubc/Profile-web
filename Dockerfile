FROM python:slim

WORKDIR /usr/src/goaltracker

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY requirements-test.txt .

RUN pip install --no-cache-dir -r requirements-test.txt

COPY . .

EXPOSE 5000

CMD ["python", "Profile-web/server.py"]
# CMD ["gunicorn", "-w", "2", "main:app", "-b", "0.0.0.0:5000"]