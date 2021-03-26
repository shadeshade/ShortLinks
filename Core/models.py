from django.contrib.sessions.models import Session
from django.db import models


class Link(models.Model):
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, blank=True, null=True)
    main_part = models.URLField(blank=False, null=False)
    subpart = models.CharField(max_length=100, unique=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.main_part} {self.subpart}'
