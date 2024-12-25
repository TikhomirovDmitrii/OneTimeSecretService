OneTimeSecretService

OneTimeSecretService — это HTTP-сервис для создания одноразовых секретов с использованием Python, Django и MySQL. Проект реализован в формате JSON API, без пользовательского интерфейса.

Функционал
1. **Создание секрета**: 
   - Эндпоинт `/api/secrets/generate/`
   - Принимает секрет и кодовую фразу, возвращает уникальный `secret_key`.
2. **Получение секрета**:
   - Эндпоинт `/api/secrets/{secret_key}/`
   - Принимает кодовую фразу, возвращает секрет. Секрет удаляется после первого доступа.

Технологии
- **Язык программирования**: Python 3.7
- **Фреймворк**: Django
- **База данных**: MySQL
- **Контейнеризация**: Docker

Установка и запуск
Шаг 1: Клонируйте репозиторий
```bash
git clone https://github.com/your-username/OneTimeSecretService.git
cd OneTimeSecretService

Шаг 2: Настройка Docker
Для запуска контейнеров выполните:
docker-compose up --build

Шаг 3: Примените миграции
docker exec -it onetimesecretservice_app python manage.py migrate

Шаг 4: Тестирование
Запустите тесты для проверки функциональности:
docker exec -it onetimesecretservice_app python manage.py test


Примеры использования API
1. Создание секрета
Запрос:

POST /api/secrets/generate/
Content-Type: application/json
{
    "secret": "MySecretMessage",
    "passphrase": "MyPassphrase123"
}

Ответ:
{
    "secret_key": "abc123xyz"
}


2. Получение секрета
Запрос:
GET /api/secrets/abc123xyz/
Content-Type: application/json
{
    "passphrase": "MyPassphrase123"
}

Ответ:
{
    "secret": "MySecretMessage"
}
