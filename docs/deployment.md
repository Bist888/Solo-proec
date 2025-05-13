# Инструкция по развертыванию

## Системные требования

- Python 3.8 или выше
- PostgreSQL 12 или выше (опционально, можно использовать SQLite)
- 1GB RAM минимум
- 2GB свободного места на диске

## Установка из исходного кода

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/cms-project.git
cd cms-project
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл .env в корневой директории проекта:
```bash
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=example.com,www.example.com
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

5. Примените миграции:
```bash
python manage.py migrate
```

6. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

7. Соберите статические файлы:
```bash
python manage.py collectstatic
```

## Установка из exe (только для Windows)

1. Скачайте последнюю версию установщика с [страницы релизов](https://github.com/your-username/cms-project/releases)
2. Запустите установщик и следуйте инструкциям
3. После установки запустите приложение через ярлык на рабочем столе

## Настройка для production

### Nginx

```nginx
server {
    listen 80;
    server_name example.com www.example.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/your/project;
    }

    location /media/ {
        root /path/to/your/project;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

### Gunicorn

Создайте файл `/etc/systemd/system/gunicorn.service`:

```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/your/project/venv/bin/gunicorn \
    --access-logfile - \
    --workers 3 \
    --bind unix:/run/gunicorn.sock \
    myproject.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Supervisor

Создайте файл `/etc/supervisor/conf.d/cms.conf`:

```ini
[program:cms]
command=/path/to/your/project/venv/bin/gunicorn --workers 3 --bind unix:/run/gunicorn.sock myproject.wsgi:application
directory=/path/to/your/project
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/cms.err.log
stdout_logfile=/var/log/cms.out.log
```

## Обновление

1. Остановите сервер:
```bash
sudo systemctl stop gunicorn
```

2. Получите последние изменения:
```bash
git pull origin main
```

3. Обновите зависимости:
```bash
pip install -r requirements.txt
```

4. Примените миграции:
```bash
python manage.py migrate
```

5. Соберите статические файлы:
```bash
python manage.py collectstatic --noinput
```

6. Запустите сервер:
```bash
sudo systemctl start gunicorn
```

## Резервное копирование

### База данных

```bash
# PostgreSQL
pg_dump dbname > backup.sql

# SQLite
sqlite3 db.sqlite3 .dump > backup.sql
```

### Медиафайлы

```bash
tar -czf media_backup.tar.gz media/
```

## Мониторинг

Рекомендуется настроить следующие инструменты мониторинга:

- Sentry для отслеживания ошибок
- Prometheus + Grafana для мониторинга производительности
- ELK Stack для анализа логов

## Безопасность

1. Всегда используйте HTTPS в production
2. Регулярно обновляйте зависимости
3. Настройте брандмауэр
4. Используйте strong password policy
5. Настройте rate limiting
6. Включите CSRF и XSS защиту

## Оптимизация

1. Настройте кэширование:
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

2. Включите сжатие:
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
```

3. Настройте CDN для статических файлов

## Troubleshooting

### Проблемы с правами доступа

```bash
sudo chown -R www-data:www-data /path/to/your/project
sudo chmod -R 755 /path/to/your/project
```

### Проблемы с медиафайлами

```bash
sudo chown -R www-data:www-data media/
sudo chmod -R 755 media/
```

### Очистка кэша

```bash
python manage.py clearcache
python manage.py clear_cache
redis-cli flushall
``` 