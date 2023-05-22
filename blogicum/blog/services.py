from django.http import Http404
from blog.posts import posts


def get_list_posts() -> dict:
    return {'post_list': posts}


def get_post(id: int) -> dict:
    try:
        post = posts[id]
    except IndexError:
        raise Http404('Заданный пост не существует')
    return post
