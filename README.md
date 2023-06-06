# sefer_foundation_back_end

Установка и запуск проекта.
===
Для работы необходимо:
- Создать сервисный аккаунт в консоли управления.
- Создать бакет в Yandex Object Storage, доступ для бакета нужно сделать публичным.
- Установить YC CLI, для получения IAM-token для работы с API Yandex Speechkit.(Обновляется ежедневно.)
- Так же ,для корректной работы библиотеки boto3, необходимо установить  AWS CLI и настроить соответствующие файлы конфигурации.

Подробные инструкции доступны по ссылкам:
- https://cloud.yandex.ru/docs/storage/tools/boto
- https://cloud.yandex.ru/docs/speechkit/stt/api/transcribation-api
- https://cloud.yandex.ru/docs/iam/operations/iam-token/create-for-sa
- https://cloud.yandex.ru/docs/iam/operations/sa/create
- https://cloud.yandex.ru/docs/iam/operations/sa/create-access-key

Создайте файл .env  с переменными окружения в корневой директории проекта:
```
YC_IAM_TOKEN = 'you iam token'
YC_BUCKET_NAME = 'you backet name'
```
---

Создайте виртуальное окружение и установите файл с зависимостями:
```bash
python -m venv venv
pip install -r requirements.txt
``` 

В директории с файлом manage.py установите миграции и создайте супер юзера:
```bash
cd transcribe_app/
python manage.py migrate
python manage.py createsuperuser
```
---

Запустить проект на локальном сервере:
```bash
python manage.py runserver
```
---

Документация API доступна по адресу:
```bash
localhot:8000/docs
```