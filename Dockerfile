# Використовуємо офіційний Python
FROM python:3.11-slim

# Встановлюємо залежності для роботи з MySQL та wget
RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential wget pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Робоча директорія
WORKDIR /app

# Копіюємо requirements.txt
COPY requirements.txt .

# Встановлюємо залежності Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копіюємо весь проєкт
COPY . .

# Завантажуємо wait-for-it
RUN wget -O wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x wait-for-it.sh

# Змінні оточення
ENV PYTHONUNBUFFERED=1

# Запуск Django після перевірки MySQL
CMD ["./wait-for-it.sh", "db:3306", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]