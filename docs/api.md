# API Documentation

## Общая информация

Все эндпоинты API возвращают данные в формате JSON. Для авторизованных запросов необходимо передавать токен в заголовке:

```
Authorization: Token <your_token>
```

## Эндпоинты

### Список контента

```
GET /api/content/
```

Параметры запроса:
- `page`: номер страницы (по умолчанию 1)
- `search`: поисковый запрос
- `status`: фильтр по статусу (published/draft)

Пример ответа:
```json
{
    "count": 100,
    "next": "http://example.com/api/content/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Заголовок",
            "description": "Описание",
            "content": "Полный текст",
            "author": {
                "id": 1,
                "username": "author"
            },
            "created_at": "2024-03-20T12:00:00Z",
            "updated_at": "2024-03-20T12:00:00Z",
            "status": "published"
        }
    ]
}
```

### Получение контента

```
GET /api/content/{id}/
```

Пример ответа:
```json
{
    "id": 1,
    "title": "Заголовок",
    "description": "Описание",
    "content": "Полный текст",
    "author": {
        "id": 1,
        "username": "author"
    },
    "created_at": "2024-03-20T12:00:00Z",
    "updated_at": "2024-03-20T12:00:00Z",
    "status": "published",
    "image": "http://example.com/media/images/content_1.jpg"
}
```

### Создание контента

```
POST /api/content/
```

Требуется авторизация.

Тело запроса:
```json
{
    "title": "Новый заголовок",
    "description": "Новое описание",
    "content": "Новый контент",
    "status": "draft",
    "image": <file>
}
```

### Обновление контента

```
PUT /api/content/{id}/
```

Требуется авторизация. Доступно только автору контента.

Тело запроса:
```json
{
    "title": "Обновленный заголовок",
    "description": "Обновленное описание",
    "content": "Обновленный контент",
    "status": "published"
}
```

### Удаление контента

```
DELETE /api/content/{id}/
```

Требуется авторизация. Доступно только автору контента.

## Коды ответов

- 200: Успешный запрос
- 201: Успешное создание
- 204: Успешное удаление
- 400: Некорректный запрос
- 401: Не авторизован
- 403: Доступ запрещен
- 404: Не найдено

## Примеры использования

### Python (requests)

```python
import requests

# Получение списка контента
response = requests.get('http://example.com/api/content/')
content_list = response.json()

# Создание контента
headers = {'Authorization': 'Token your_token'}
data = {
    'title': 'Новый контент',
    'description': 'Описание',
    'content': 'Текст контента',
    'status': 'draft'
}
files = {'image': open('image.jpg', 'rb')}
response = requests.post('http://example.com/api/content/', 
                        headers=headers,
                        data=data,
                        files=files)

# Обновление контента
data = {'title': 'Обновленный заголовок'}
response = requests.patch('http://example.com/api/content/1/',
                         headers=headers,
                         json=data)
```

### JavaScript (fetch)

```javascript
// Получение списка контента
fetch('http://example.com/api/content/')
    .then(response => response.json())
    .then(data => console.log(data));

// Создание контента
const formData = new FormData();
formData.append('title', 'Новый контент');
formData.append('description', 'Описание');
formData.append('content', 'Текст контента');
formData.append('status', 'draft');
formData.append('image', imageFile);

fetch('http://example.com/api/content/', {
    method: 'POST',
    headers: {
        'Authorization': 'Token your_token'
    },
    body: formData
})
    .then(response => response.json())
    .then(data => console.log(data));
```

## Ограничения

- Максимальный размер загружаемого изображения: 5MB
- Поддерживаемые форматы изображений: JPG, PNG, GIF
- Количество запросов: 1000 в час для авторизованных пользователей, 100 в час для анонимных 