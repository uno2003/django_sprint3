from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class PublishedModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        null=False,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
        verbose_name='Добавлено',
    )

    class Meta:
        abstract = True


class Category(PublishedModel):
    title = models.CharField(
        max_length=256,
        blank=False,
        null=False,
        verbose_name='Заголовок',
    )
    description = models.TextField(verbose_name='Описание',)
    slug = models.SlugField(
        unique=True,
        null=False,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; разрешены'
                  ' символы латиницы, цифры, дефис и подчёркивание.',
    )

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse('category', kwargs={'category_slug': self.slug})

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Location(PublishedModel):
    name = models.CharField(
        max_length=256,
        null=False,
        verbose_name='Название места',
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name


class Post(PublishedModel):
    title = models.CharField(
        max_length=256,
        blank=False,
        null=False,
        verbose_name='Заголовок',
    )
    text = models.TextField(verbose_name='Текст',)
    pub_date = models.DateTimeField(
        null=False,
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в'
                  ' будущем — можно делать отложенные публикации.',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self) -> str:
        return self.title
