FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Mở port uvicorn
EXPOSE 8000

# Lệnh khởi chạy uvicorn
CMD ["uvicorn", "mymoney.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--reload"]
