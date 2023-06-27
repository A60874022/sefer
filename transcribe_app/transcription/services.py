import time

import boto3
import requests
from django.conf import settings
from http import HTTPStatus
from .models import Transcription


def check_obj_id_type(obj_id: int) -> int:
    """
    Функция проверяет тип переданного obj_id.
    Тип obj_id должен быть целочисленным значением.
    """
    if not isinstance(obj_id, int):
        raise ValueError("Invalid data, obj_id must be a integer.")
    return obj_id


def create_text_blocks(text: list) -> list:
    """
    Функция разбивает результат, полученный от
    API Yandex Speechkit, на списки по промежуткам
    времени. В качестве вводных данных принимает список
    из кортежей со значениями (время, слово).
    """
    text_blocks = [[]]
    start = text[0][0]
    for curr_time, word in text:
        if curr_time - start <= 60:  # 60 - значение интервала(в сек.)
            text_blocks[-1].append(word)
        else:
            text_blocks.append([word])
            start = curr_time
    return text_blocks


def get_audio_file(obj_id: int) -> str:
    """
    Функция возвращает путь к файлу в проекте.
    Принимает в качестве аргумента pk модели транскрипции.
    """
    check_obj_id_type(obj_id)
    transcription = Transcription.objects.get(pk=obj_id)
    path_to_audio = str(transcription.audio)
    return path_to_audio


def upload_file_to_bucket(obj_id: int) -> None:
    """Функция для загрузки файла в бакет."""
    check_obj_id_type(obj_id)
    session = boto3.session.Session()
    s3 = session.client(
        service_name="s3", endpoint_url="https://storage.yandexcloud.net"
    )
    file_name = get_audio_file(obj_id).split("/")[-1]
    s3.upload_file(
        f"{settings.MEDIA_ROOT}/{get_audio_file(obj_id)}",
        settings.YC_BUCKET_NAME,
        file_name,
    )


def create_bucket_url(obj_id: int) -> str:
    """Функция для генерации ссылки файла из бакета."""
    check_obj_id_type(obj_id)
    file_name = get_audio_file(obj_id).split("/")[-1]
    return f"https://storage.yandexcloud.net/{settings.YC_BUCKET_NAME}/{file_name}"


def create_transcription(obj_id: int) -> list:
    """
    Функция для создания транскрипции текста.
    Отправляет POST запрос к API Yandex Speechkit
    Принимает ссылку аудио из модели транскрипции.
    На выходе получаем список из слов разбитым по временным интервалам:
    [[word1, word2, word3], [word4, word5, word6], ...].
    """
    upload_file_to_bucket(obj_id)  # загрузка файла в бакет
    file_url = create_bucket_url(obj_id)
    post_url = settings.TRANSCRIBE_API_URL
    body = {
        "config": {
            "specification": {
                "languageCode": "ru-RU",
                "audioEncoding": "MP3",
            }
        },
        "audio": {"uri": file_url},
    }
    header = {"Authorization": "Bearer {}".format(settings.YC_IAM_TOKEN)}
    req = requests.post(post_url, headers=header, json=body)
    if req.status_code != HTTPStatus.OK:
        raise requests.HTTPError("Произошла ошибка при отправке HTTP запроса.")
    data = req.json()

    while True:
        time.sleep(1)
        get_url = "https://operation.api.cloud.yandex.net/operations/{id}"
        req = requests.get(get_url.format(id=data["id"]), headers=header)
        req = req.json()
        if req["done"]:
            break
    result_text = []
    for chunk in req["response"]["chunks"]:
        for word in chunk["alternatives"][0]["words"]:
            result_text.append((float(word["startTime"][:-1]), word["word"]))
    return create_text_blocks(result_text)
