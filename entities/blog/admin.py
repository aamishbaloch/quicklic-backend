from django.contrib import admin
from entities.blog.models import Blog


class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'is_active', 'created_at')

admin.site.register(Blog, BlogAdmin)
