FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR uchet/
COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r req.txt
RUN python manage.py collectstatic

CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]