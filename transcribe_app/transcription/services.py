import boto3
from .models import Trancription


FILE_PATH = '/home/buvaev/Dev/sefer_foundation_back_end/transcribe_app/media/'
BACKET_NAME = 'buvaev-backet'


def upload_file_to_bucket(obj_id: int) -> None:
    """Функция для загрузки файла в бакет."""
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net'
    )
    trancription = Trancription.objects.get(pk=obj_id)
    path_to_audio = str(trancription.audio)
    file_name = path_to_audio.split('/')[-1]
    s3.upload_file(f'{FILE_PATH}/{path_to_audio}', BACKET_NAME, file_name)


if __name__ == '__main__':
    upload_file_to_bucket(2)
