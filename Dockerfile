FROM python:3.11

# Создаем директорию /lb и устанавливаем её как рабочую
WORKDIR /lb

# Копируем файлы проекта в рабочую директорию контейнера
COPY . .

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Запускаем бота
CMD ["python", "bot.py"]
