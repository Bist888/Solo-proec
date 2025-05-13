from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms import ArticleForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from .models import Content
from .forms import ContentForm

def article_list(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'cms_content/article_list.html', {'articles': articles})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'cms_content/article_detail.html', {'article': article})

@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'cms_content/article_form.html', {'form': form})

@login_required
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'cms_content/article_form.html', {'form': form})

@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect('article_list')

class ContentListView(ListView):
    model = Content
    template_name = 'cms_content/content_list.html'
    context_object_name = 'content_list'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Content.objects.all()
        
        # Поиск
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        
        # Фильтрация по статусу
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset.order_by('-created_at')

class ContentDetailView(DetailView):
    model = Content
    template_name = 'cms_content/content_detail.html'
    context_object_name = 'content'

class ContentCreateView(LoginRequiredMixin, CreateView):
    model = Content
    form_class = ContentForm
    template_name = 'cms_content/content_form.html'
    success_url = reverse_lazy('content_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Контент успешно создан')
        return super().form_valid(form)

class ContentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Content
    form_class = ContentForm
    template_name = 'cms_content/content_form.html'
    success_url = reverse_lazy('content_list')
    
    def test_func(self):
        content = self.get_object()
        return self.request.user == content.author
    
    def form_valid(self, form):
        messages.success(self.request, 'Контент успешно обновлен')
        return super().form_valid(form)

class ContentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Content
    template_name = 'cms_content/content_confirm_delete.html'
    success_url = reverse_lazy('content_list')
    
    def test_func(self):
        content = self.get_object()
        return self.request.user == content.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Контент успешно удален')
        return super().delete(request, *args, **kwargs)
