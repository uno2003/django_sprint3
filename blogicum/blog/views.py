from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Post, Category
from datetime import datetime as dt

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        time_now = dt.now()
        print(time_now)

        queryset = Post.objects.select_related('category').filter(is_published=True, category__is_published=True, pub_date__lt=time_now)[0:5]
        print(queryset)
        context['post_list'] = queryset
        return context




class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get(self, request, id: int) -> HttpResponse:
        post = Post.objects.get(id=id)
        context = {'post': post}
        return render(request, self.template_name, context)


class CategoryPostView(DetailView):
    model = Category
    template_name = 'blog/category.html'

    def get(self, request, category_slug: str) -> HttpResponse:
        category = Category.objects.get(slug=category_slug)
        post_list = Post.objects.filter(category=category)
        context = {'category': category, 'post_list': post_list }
        return render(request, self.template_name, context)
