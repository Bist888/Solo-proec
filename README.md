# Solo-proec — Система управления контентом

Веб-приложение для управления контентом сайта, разработанное на Python/Django.

---

## Описание

**Solo-proec** — это современная CMS (система управления контентом), позволяющая создавать, редактировать и публиковать статьи, управлять пользователями, комментариями и уведомлениями. Проект реализован на Django и поддерживает расширение через REST API.

---

## Основные возможности

- CRUD для статей и комментариев
- Управление пользователями и ролями
- Поиск и фильтрация статей
- Уведомления для пользователей
- Современный адаптивный интерфейс
- Админ-панель Django
- REST API для интеграции с внешними сервисами
- Автоматическое тестирование

---

## Требования

- Python 3.8+
- Django 3.2+ (или твоя версия)
- Windows 7/10/11, Linux или macOS
- Минимум 2GB RAM
- 500MB свободного места на диске

---

## Установка и запуск

1. **Клонируйте репозиторий:**
   ```sh
   git clone https://github.com/Bist888/Solo-proec.git
   cd Solo-proec
   ```

2. **Установите зависимости:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Примените миграции:**
   ```sh
   python manage.py migrate
   ```

4. **Создайте суперпользователя (админа):**
   ```sh
   python manage.py createsuperuser
   ```

5. **Запустите сервер:**
   ```sh
   python manage.py runserver
   ```

6. **Откройте в браузере:**
   - Пользовательский интерфейс: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Админ-панель: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Документация

- [User Guide](https://github.com/Bist888/Solo-proec/wiki/User-Guide)
- [Архитектура](https://github.com/Bist888/Solo-proec/wiki/Архитектура)
- [API](https://github.com/Bist888/Solo-proec/wiki/API)
- [Тестирование](https://github.com/Bist888/Solo-proec/wiki/Тестирование)
- [Brand Book](https://github.com/Bist888/Solo-proec/wiki/Brand-Book)


*или используйте [Wiki](https://github.com/Bist888/Solo-proec/wiki) для подробной документации.*

---

## Тестирование

Для запуска всех тестов выполните:
```sh
python manage.py test
```

---

## Примеры API

- Получить список статей:  
  `GET /api/articles/`
- Создать статью:  
  `POST /api/articles/`
- Получить комментарии:  
  `GET /api/comments/`

Подробнее — в [API-документации](docs/api.md) или Wiki.

---

## Лицензия

MIT License

---

## Контакты и поддержка

- Email: serezha.serezha.05@bk.ru
- Telegram: @khkksjshskkz

---

**Буду рад вашим вопросам и предложениям!** 
