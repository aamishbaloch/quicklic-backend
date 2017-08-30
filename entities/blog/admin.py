from django.contrib import admin
from entities.blog.models import Blog, Author


class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'is_active', 'created_at')

admin.site.register(Blog, BlogAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'title', 'is_active', 'created_at')

admin.site.register(Author, AuthorAdmin)
