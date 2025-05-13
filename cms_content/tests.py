from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Content
from django.core.files.uploadedfile import SimpleUploadedFile

class ContentViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.content = Content.objects.create(
            title='Test Content',
            description='Test Description',
            content='Test Content Body',
            author=self.user,
            status='published'
        )
        
    def test_content_list_view(self):
        response = self.client.get(reverse('content_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cms_content/content_list.html')
        self.assertContains(response, 'Test Content')
        
    def test_content_detail_view(self):
        response = self.client.get(reverse('content_detail', args=[self.content.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cms_content/content_detail.html')
        self.assertContains(response, 'Test Content')
        
    def test_content_create_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('content_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cms_content/content_form.html')
        
        # Тест создания контента
        image = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        
        post_data = {
            'title': 'New Content',
            'description': 'New Description',
            'content': 'New Content Body',
            'status': 'draft',
            'image': image
        }
        
        response = self.client.post(reverse('content_create'), post_data)
        self.assertEqual(response.status_code, 302)  # Редирект после успешного создания
        self.assertTrue(Content.objects.filter(title='New Content').exists())
        
    def test_content_update_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('content_update', args=[self.content.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cms_content/content_form.html')
        
        # Тест обновления контента
        post_data = {
            'title': 'Updated Content',
            'description': 'Updated Description',
            'content': 'Updated Content Body',
            'status': 'published'
        }
        
        response = self.client.post(reverse('content_update', args=[self.content.id]), post_data)
        self.assertEqual(response.status_code, 302)  # Редирект после успешного обновления
        self.content.refresh_from_db()
        self.assertEqual(self.content.title, 'Updated Content')
        
    def test_content_delete_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('content_delete', args=[self.content.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cms_content/content_confirm_delete.html')
        
        # Тест удаления контента
        response = self.client.post(reverse('content_delete', args=[self.content.id]))
        self.assertEqual(response.status_code, 302)  # Редирект после успешного удаления
        self.assertFalse(Content.objects.filter(id=self.content.id).exists())
        
    def test_search_functionality(self):
        # Создаем дополнительный контент для тестирования поиска
        Content.objects.create(
            title='Another Content',
            description='Different Description',
            content='Different Content Body',
            author=self.user,
            status='published'
        )
        
        # Тест поиска по заголовку
        response = self.client.get(reverse('content_list') + '?search=Test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['content_list']), 1)
        
        # Тест поиска по описанию
        response = self.client.get(reverse('content_list') + '?search=Different')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['content_list']), 1)
        
    def test_pagination(self):
        # Создаем дополнительный контент для тестирования пагинации
        for i in range(15):  # Создаем 15 дополнительных записей
            Content.objects.create(
                title=f'Content {i}',
                description=f'Description {i}',
                content=f'Content Body {i}',
                author=self.user,
                status='published'
            )
            
        response = self.client.get(reverse('content_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['content_list']), 10)  # 10 записей на странице
        
    def test_status_filter(self):
        # Создаем контент с разными статусами
        Content.objects.create(
            title='Draft Content',
            description='Draft Description',
            content='Draft Content Body',
            author=self.user,
            status='draft'
        )
        
        # Тест фильтра по статусу published
        response = self.client.get(reverse('content_list') + '?status=published')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['content_list']), 1)
        
        # Тест фильтра по статусу draft
        response = self.client.get(reverse('content_list') + '?status=draft')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['content_list']), 1)
