from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView
from .models import Post, Category
from django.utils import timezone
from django.http import Http404



class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        now = timezone.now()
        context = super().get_context_data(**kwargs)
        post_list = Post.objects.filter(is_published=True, category__is_published=True, pub_date__lte=now)[0:5]
        context = {'post_list': post_list}
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get(self, request, id: int) -> HttpResponse:
        try:
            post = Post.objects.get(id=id)
        except ObjectDoesNotExist:
            raise Http404('Заданный пост не существует')

        now = timezone.now()
        # get_object_or_404(post, post.category.is_published=False, post.pub_date__lte=now, post.is_published=False)

        if post.is_published == False or post.category.is_published == False or post.pub_date > now:
            raise Http404('Болт')

        context = {'post': post}
        return render(request, self.template_name, context)


class CategoryPostView(DetailView):
    model = Category
    template_name = 'blog/category.html'

    def get(self, request, category_slug: str) -> HttpResponse:
        now = timezone.now()
        category = Category.objects.get(slug=category_slug)
        if category.is_published == False:
            raise Http404
        post_list = Post.objects.select_related('category').filter(category=category, is_published=True, category__is_published=True, pub_date__lte=now)
        context = {'category': category, 'post_list': post_list}
        return render(request, self.template_name, context)

