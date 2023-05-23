from django.contrib import admin
from blog.models import Post, Category, Location


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'category',
        'location',
        'pub_date',
        'is_published',
    )
    list_editable = ('is_published',)
    list_filter = ('category', 'location', 'author',)
    search_fields = ('title', 'author', 'category',)
    list_display_links = ('title',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published',)
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_display_links = ('title',)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published',)
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_display_links = ('name',)


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
