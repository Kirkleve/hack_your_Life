import os
import requests
import imagehash
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from logger import log_info, log_warning, log_error

try:
    log_info(f"✅ OpenCV установлен, версия: {cv2.__version__}")
except Exception as e:
    log_warning(f"❌ Ошибка с OpenCV: {e}")


def get_image_hash(image_url):
    """🔍 Получаем хеш изображения для сравнения"""
    try:
        response = requests.get(image_url, timeout=10)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            log_info(f"🔄 Проверяем изображение: {image_url}")
            return str(imagehash.average_hash(image))
    except Exception as e:
        log_warning(f"Ошибка при обработке изображения: {e}")
    return None


def contains_faces(image_url):
    """🤖 Проверяем, есть ли лица на изображении (исключаем фото людей)"""
    try:
        response = requests.get(image_url, timeout=10)
        if response.status_code == 200:
            image_array = np.asarray(bytearray(response.content), dtype=np.uint8)  # ✅ Декодируем изображение
            image_cv = cv2.imdecode(image_array, cv2.IMREAD_GRAYSCALE)  # ✅ Добавляем флаг

            cv2_base_dir = os.path.dirname(cv2.__file__)  # Находим путь к OpenCV
            haarcascade_path = os.path.join(cv2_base_dir, "data", "haarcascade_frontalface_default.xml")

            face_cascade = cv2.CascadeClassifier(haarcascade_path)
            faces = face_cascade.detectMultiScale(image_cv, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            return len(faces) > 0

    except Exception as e:
        log_error(f"Ошибка при анализе изображения: {e}")

    return False
