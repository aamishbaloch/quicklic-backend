from django.contrib import admin
from entities.blog.models import Blog, Author


class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'is_active', 'created_at')
    search_fields = ('title',)
    list_filter = ('author__name', 'is_active')

admin.site.register(Blog, BlogAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'title', 'is_active', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_active',)

admin.site.register(Author, AuthorAdmin)
