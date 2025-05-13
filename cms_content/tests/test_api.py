from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import Content
from django.core.files.uploadedfile import SimpleUploadedFile

class ContentAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = get_user_model().objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.content = Content.objects.create(
            title='Test Content',
            description='Test Description',
            content='Test Content Body',
            author=self.user,
            status='published'
        )
        
    def test_content_list(self):
        """Тест получения списка контента"""
        response = self.client.get(reverse('api:content-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
    def test_content_detail(self):
        """Тест получения деталей контента"""
        response = self.client.get(
            reverse('api:content-detail', args=[self.content.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Content')
        
    def test_create_content_unauthorized(self):
        """Тест создания контента без авторизации"""
        data = {
            'title': 'New Content',
            'description': 'New Description',
            'content': 'New Content Body',
            'status': 'draft'
        }
        response = self.client.post(reverse('api:content-list'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_create_content_authorized(self):
        """Тест создания контента с авторизацией"""
        self.client.force_authenticate(user=self.user)
        image = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        data = {
            'title': 'New Content',
            'description': 'New Description',
            'content': 'New Content Body',
            'status': 'draft',
            'image': image
        }
        response = self.client.post(reverse('api:content-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Content.objects.count(), 2)
        
    def test_update_content_unauthorized(self):
        """Тест обновления контента без авторизации"""
        data = {'title': 'Updated Title'}
        response = self.client.patch(
            reverse('api:content-detail', args=[self.content.id]),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_update_content_not_author(self):
        """Тест обновления контента не автором"""
        self.client.force_authenticate(user=self.other_user)
        data = {'title': 'Updated Title'}
        response = self.client.patch(
            reverse('api:content-detail', args=[self.content.id]),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_update_content_author(self):
        """Тест обновления контента автором"""
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated Title'}
        response = self.client.patch(
            reverse('api:content-detail', args=[self.content.id]),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.content.refresh_from_db()
        self.assertEqual(self.content.title, 'Updated Title')
        
    def test_delete_content_unauthorized(self):
        """Тест удаления контента без авторизации"""
        response = self.client.delete(
            reverse('api:content-detail', args=[self.content.id])
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_delete_content_not_author(self):
        """Тест удаления контента не автором"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(
            reverse('api:content-detail', args=[self.content.id])
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_delete_content_author(self):
        """Тест удаления контента автором"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse('api:content-detail', args=[self.content.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Content.objects.count(), 0)
        
    def test_search_content(self):
        """Тест поиска контента"""
        Content.objects.create(
            title='Another Content',
            description='Different Description',
            content='Different Content Body',
            author=self.user,
            status='published'
        )
        
        response = self.client.get(
            reverse('api:content-list'),
            {'search': 'Test'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Content')
        
    def test_filter_by_status(self):
        """Тест фильтрации по статусу"""
        Content.objects.create(
            title='Draft Content',
            description='Draft Description',
            content='Draft Content Body',
            author=self.user,
            status='draft'
        )
        
        response = self.client.get(
            reverse('api:content-list'),
            {'status': 'published'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['status'], 'published') 