<h1 align="center">sefer_foundation_back_end</h1>

<details align="center">
  <summary align="center"><h3>Эндпоинты</h3></summary>
  <ul>
    <li>Документация: <code>http://127.0.0.1:8000/api/redoc/</code></li>
    <li>Админ панель: <code>http://127.0.0.1:8000/admin/</code></li>
  </ul>
</details>
<hr>
<h3 align="center">Установка и запуск проекта</h3>
<details>
  <summary align="center"><h4>1. Для работы необходимо <ins>(НА ДАННЫЙ МОМЕНТ ПУНКТ НЕ АКТУАЛЕН)</ins></h4></summary>
  <ul>
    <li>Создать сервисный аккаунт в консоли управления.</li>
    <li>Создать бакет в Yandex Object Storage, доступ для бакета нужно сделать публичным.</li>
    <li>Установить YC CLI, для получения IAM-token для работы с API Yandex Speechkit(обновляется ежедневно).</li>
    <li>Так же ,для корректной работы библиотеки boto3, необходимо установить  AWS CLI и настроить соответствующие файлы конфигурации.</li>
  </ul>

  <div align="center">
  <h4>Подробные инструкции доступны по ссылкам:</h4>
      https://cloud.yandex.ru/docs/storage/tools/boto<br>
      https://cloud.yandex.ru/docs/speechkit/stt/api/transcribation-api<br>
      https://cloud.yandex.ru/docs/iam/operations/iam-token/create-for-sa<br>
      https://cloud.yandex.ru/docs/iam/operations/sa/create<br>
      https://cloud.yandex.ru/docs/iam/operations/sa/create-access-key<br>
  </div>
</details>


<h4 align="center">2. Создайте файл <code>.env</code> с переменными окружения в папке 
  <a href="https://github.com/Studio-Yandex-Practicum/sefer_foundation_back_end/tree/feature/infrastructure_refactoring/infra"><code>infra</code></a> 
  по шаблону <a href="https://github.com/Studio-Yandex-Practicum/sefer_foundation_back_end/blob/feature/infrastructure_refactoring/infra/.env.example"><code>.env.example</code></a>
</h4>


<h4 align="center">3. Запустите проект</h4>
<details>
  <p align="center"><summary align="center"><ins>через Docker</ins></summary></p>
  <ul>
    <li align="center">
      <p>1. Создать виртуальную оболочку <code>python -m venv venv</code>.</p>
    </li>
    <li align="center">
      <p>2. Активировать виртуальную оболочку <code>. venv/scripts/acitvate</code>.</p>
    </li>
    <li align="center">
      <p>3. Установить зависимости <code>pip install -r requirements.txt</code>.</p>
    </li>
    <li>
      <div align="center">
        <p>4. Если имеется утилита <code>Make</code>, в корне проекта выполнить команду <code>make project-init-dev</code>,</p>
        <p><code>Docker</code> соберёт контейнер с <code>postgreSQL</code>, выполнятся миграции, создастся <i>superuser</i>.</p>
        <p>иначе</p>
        <p>выполнить команды:</p>
      </div>

  ```bash
    docker compose -f infra/docker-compose-dev.yml --env-file ./infra/.env up -d
    python transcribe_app/manage.py migrate
    python transcribe_app/manage.py createsuperuser --noinput
    python transcribe_app/manage.py runserver
  ```
  </li>
    <li>
      <p align="center">5. После сервер будет доступен по адрессу: <code>http://127.0.0.1:8000/</code>.</p>
    </li>
    <p align="center"><b>Примечание</b></p>
    <li align="center">
      <p>Последующие запуски проекта осуществляются через команду <code>make project-start-dev</code></p>
    </li>
  </ul>
</details>

<details>
  <p align="center"><summary align="center"><ins>через консоль</ins></summary></p>
  <ul>
    <li align="center">
      <p>1. Создать БД в <code>postgreSQL</code>.</p>
    </li>
    <li align="center">
      <p>2. Создать виртуальную оболочку <code>python -m venv venv</code>.</p>
    </li>
    <li align="center">
      <p>3. Активировать виртуальную оболочку <code>. venv/scripts/acitvate</code>.</p>
    </li>
    <li align="center">
      <p>4. Установить зависимости <code>pip install -r requirements.txt</code>.</p>
    </li>
    <li align="center">
      <p>5. Выполнить миграцию БД <code>python transcribe_app/manage.py migrate</code>.</p>
    </li>
        <li align="center">
      <p>6. Создать superuser-a <code>python transcribe_app/manage.py createsuperuser --noinput</code>.</p>
    </li>
    </li>
    <li align="center">
      <p>7. Запустить сервер <code>python transcribe_app/manage.py runserver</code>.</p>
    </li>
    <li align="center">
      <p>8. Сервер будет доступен по адрессу: <code>http://127.0.0.1:8000/</code>.</p>
    </li>
  </ul>
</details>
<hr>
<h3 align="center">Стек</h3>
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9-red?style=flat&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Django-4.2.1-red?style=flat&logo=django&logoColor=white">
  <img src="https://img.shields.io/badge/DjangoRestFramework-3.14.0-red?style=flat">
  <img src="https://img.shields.io/badge/Boto3-1.26.144-red?style=flat&logo=boto3&logoColor=white">
  <img src="https://img.shields.io/badge/PostgreSQL-Latest-red?style=flat&logo=postgresql&logoColor=white">
  <img src="https://img.shields.io/badge/Docker-Latest-red?style=flat&logo=docker&logoColor=white">
  <img src="https://img.shields.io/badge/Swagger-Latest-red?style=flat&logo=swagger&logoColor=white">
</p>
<hr>
