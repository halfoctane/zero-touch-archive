FROM python:3.11-alpine
WORKDIR /app
RUN pip install flask pytz --no-cache-dir
COPY app.py .
COPY templates/ templates/
EXPOSE 5000
CMD ["python", "app.py"]