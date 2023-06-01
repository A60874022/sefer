import boto3


FILE_PATH = '/home/buvaev/Dev/sefer_foundation_back_end/transcribe_app/media/transcription/audio'
BACKET_NAME = 'buvaev-backet'


def upload_file_to_bucket(file_name: str) -> None:
    """Функция для загрузки файла в бакет."""
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net'
    )
    s3.upload_file(f'{FILE_PATH}/{file_name}', BACKET_NAME, file_name)


if __name__ == '__main__':
    upload_file_to_bucket('speech.ogg')
