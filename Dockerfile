# Python 3.9 asosiy image
FROM python:3.9-slim

# ffmpeg ni o'rnatish
RUN apt-get update && apt-get install -y ffmpeg

# Dastur kodini nusxalash
COPY . /app
WORKDIR /app

# Kerakli kutubxonalarni o'rnatish
RUN pip install -r requirements.txt

# Dasturni ishga tushirish
CMD ["python", "main.py"]
