from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from ..forms import ContentForm

class ContentFormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_content_form_valid_data(self):
        """Тест формы с валидными данными"""
        image = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        form_data = {
            'title': 'Test Content',
            'description': 'Test Description that is long enough',
            'content': 'Test Content Body',
            'status': 'draft'
        }
        form = ContentForm(data=form_data, files={'image': image})
        self.assertTrue(form.is_valid())
        
    def test_content_form_no_data(self):
        """Тест формы без данных"""
        form = ContentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)  # title, description, content
        
    def test_content_form_title_too_short(self):
        """Тест формы с коротким заголовком"""
        form_data = {
            'title': 'Te',  # Менее 3 символов
            'description': 'Test Description that is long enough',
            'content': 'Test Content Body',
            'status': 'draft'
        }
        form = ContentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        
    def test_content_form_description_too_short(self):
        """Тест формы с коротким описанием"""
        form_data = {
            'title': 'Test Content',
            'description': 'Too short',  # Менее 10 символов
            'content': 'Test Content Body',
            'status': 'draft'
        }
        form = ContentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)
        
    def test_content_form_invalid_image(self):
        """Тест формы с неверным форматом изображения"""
        image = SimpleUploadedFile(
            "test_doc.txt",
            b"file_content",
            content_type="text/plain"
        )
        form_data = {
            'title': 'Test Content',
            'description': 'Test Description that is long enough',
            'content': 'Test Content Body',
            'status': 'draft'
        }
        form = ContentForm(data=form_data, files={'image': image})
        self.assertFalse(form.is_valid())
        self.assertIn('image', form.errors)
        
    def test_content_form_large_image(self):
        """Тест формы с большим изображением"""
        # Создаем файл размером более 5MB
        large_image = SimpleUploadedFile(
            "large_image.jpg",
            b"x" * (5 * 1024 * 1024 + 1),
            content_type="image/jpeg"
        )
        form_data = {
            'title': 'Test Content',
            'description': 'Test Description that is long enough',
            'content': 'Test Content Body',
            'status': 'draft'
        }
        form = ContentForm(data=form_data, files={'image': large_image})
        self.assertFalse(form.is_valid())
        self.assertIn('image', form.errors)
        
    def test_content_form_html_injection(self):
        """Тест формы на защиту от HTML-инъекций"""
        form_data = {
            'title': '<script>alert("XSS")</script>',
            'description': 'Test Description that is long enough',
            'content': '<iframe src="malicious-site"></iframe>',
            'status': 'draft'
        }
        form = ContentForm(data=form_data)
        self.assertTrue(form.is_valid())  # Форма валидна, но данные будут очищены
        content = form.save(commit=False)
        self.assertNotIn('<script>', content.title)
        self.assertNotIn('<iframe>', content.content)
        
    def test_content_form_status_choices(self):
        """Тест выбора статуса контента"""
        form_data = {
            'title': 'Test Content',
            'description': 'Test Description that is long enough',
            'content': 'Test Content Body',
            'status': 'invalid_status'  # Неверный статус
        }
        form = ContentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('status', form.errors) 