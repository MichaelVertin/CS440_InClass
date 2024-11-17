FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip3 install --break-system-packages requests
COPY . .
EXPOSE 8000
CMD ["python", "api_gateway.py"]
