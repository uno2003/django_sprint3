from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from blog.models import Post, Category
from django.utils import timezone


def get_list_posts() -> dict:
    now = timezone.now()
    post_list = Post.objects \
                    .select_related('category') \
                    .filter(
                            is_published=True,
                            category__is_published=True,
                            pub_date__lte=now)[0:5]
    return post_list


def get_post(id: int) -> dict:
    now = timezone.now()
    try:
        post = Post.objects.get(id=id)
        if not post.is_published \
                or not post.category.is_published \
                or post.pub_date > now:
            raise Http404('Заданный пост не доступен')
    except ObjectDoesNotExist:
        raise Http404('Заданный пост не существует')
    return post


def get_category(category_slug: str) -> list:
    now = timezone.now()
    category = Category.objects.get(slug=category_slug)
    if not category.is_published:
        raise Http404('Заданная категория не доступна')
    post_list = (
        Post.objects
        .select_related('category')
        .filter(
            category=category,
            is_published=True,
            category__is_published=True,
            pub_date__lte=now
        )
        )
    return [category, post_list]
