# Python image-dan foydalanamiz
FROM python:3.11

# FFMPEG va kerakli kutubxonalarni o'rnatamiz
RUN apt-get update && apt-get install -y ffmpeg

# Loyihani ichiga nusxalash va kutubxonalarni o'rnatish
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Botni ishga tushirish
CMD ["python", "main.py"]
