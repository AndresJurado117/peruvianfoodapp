FROM python:latest
WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY foodapp/ /app/

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]