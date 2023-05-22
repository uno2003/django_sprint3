from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Post, Category
from datetime import datetime as dt
from django.http import Http404

DATETIME_NOW = dt.now()


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Post.objects.filter(is_published=True, category__is_published=True, pub_date__lte=DATETIME_NOW)[0:5]
        context['post_list'] = queryset
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get(self, request, id: int) -> HttpResponse:
        post = Post.objects.get(id=id)
        if post.is_published == False or post.category.is_published == False:
            raise Http404
        context = {'post': post}
        return render(request, self.template_name, context)


class CategoryPostView(DetailView):
    model = Category
    template_name = 'blog/category.html'

    def get(self, request, category_slug: str) -> HttpResponse:
        category = Category.objects.get(slug=category_slug)
        if category.is_published == False:
            raise Http404
        post_list = Post.objects.select_related('category').filter(category=category, is_published=True, category__is_published=True, pub_date__lte=DATETIME_NOW)
        context = {'category': category, 'post_list': post_list}
        return render(request, self.template_name, context)

