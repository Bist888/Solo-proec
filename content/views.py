from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms import ArticleForm

def article_list(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'content/article_list.html', {'articles': articles})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'content/article_detail.html', {'article': article})

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
    return render(request, 'content/article_form.html', {'form': form})

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
    return render(request, 'content/article_form.html', {'form': form})

@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect('article_list') 