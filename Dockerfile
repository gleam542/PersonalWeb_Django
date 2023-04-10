FROM python:3.10

WORKDIR /app

# 複製依賴文件
COPY requirements.txt .

# 安裝依賴
RUN pip install -r requirements.txt

# 複製代碼到映像中
COPY . .

# 運行Django服務
CMD python manage.py runserver 0.0.0.0:8000

