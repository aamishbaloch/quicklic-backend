from django.db import models


class QueryManager(models.Manager):
    def get_first(self, **kwargs):
        queryset = self.model.objects.filter(**kwargs)
        if queryset.exists():
            return queryset.first()
