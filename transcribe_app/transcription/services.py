import time

import boto3
import requests
from django.conf import settings

from .models import Transcription


def get_audio_file(obj_id: int) -> str:
    trancription = Transcription.objects.get(pk=obj_id)
    path_to_audio = str(trancription.audio)
    return path_to_audio


def upload_file_to_bucket(obj_id: int) -> None:
    """Функция для загрузки файла в бакет."""
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net'
    )
    file_name = get_audio_file(obj_id).split('/')[-1]
    s3.upload_file(f'{settings.MEDIA_ROOT}/{get_audio_file(obj_id)}',
                   settings.YC_BUCKET_NAME, file_name)


def create_bucket_url(obj_id: int) -> str:
    """Функция для генерации ссылки файла из бакета."""
    file_name = get_audio_file(obj_id).split('/')[-1]
    return f'https://storage.yandexcloud.net/{settings.YC_BUCKET_NAME}/{file_name}'


def create_transcription(obj_id: int) -> str:
    """Функция для создания транскрипции текста."""
    upload_file_to_bucket(obj_id)
    file_url = create_bucket_url(obj_id)
    post_url = "https://transcribe.api.cloud.yandex.net/speech/stt/v2/longRunningRecognize"
    body = {
        "config": {
            "specification": {
                "languageCode": "ru-RU",
                "audioEncoding": "MP3",
            }
        },
        "audio": {
            "uri": file_url
        }
    }
    header = {'Authorization': 'Bearer {}'.format(settings.YC_IAM_TOKEN)}
    req = requests.post(post_url, headers=header, json=body)
    data = req.json()
    id = data['id']

    while True:
        time.sleep(1)
        GET = "https://operation.api.cloud.yandex.net/operations/{id}"
        req = requests.get(GET.format(id=id), headers=header)
        req = req.json()
        if req['done']:
            break
        # print('Not ready')
    # print("Response:")
    # print(json.dumps(req, ensure_ascii=False, indent=2))
    result_text = []
    for chunk in req['response']['chunks']:
        result_text.append(chunk['alternatives'][0]['text'])
    return '. '.join(result_text)
