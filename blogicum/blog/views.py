from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from blog.models import Post, Category
from blog.services import get_post, get_list_posts, get_category


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts_list'

    def get_context_data(self) -> dict:
        post_list = get_list_posts()
        context = {'post_list': post_list}
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get(self, request, id: int) -> HttpResponse:
        post = get_post(id)
        context = {'post': post}
        return render(request, self.template_name, context)


class CategoryPostView(DetailView):
    model = Category
    template_name = 'blog/category.html'

    def get(self, request, category_slug: str) -> HttpResponse:
        category, post_list = get_category(category_slug)
        context = {'category': category,
                   'post_list': post_list}
        return render(request, self.template_name, context)
