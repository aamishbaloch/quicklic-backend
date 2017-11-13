from django.contrib import admin

from entities.review.models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'doctor', 'clinic', 'rating')

admin.site.register(Review, ReviewAdmin)
