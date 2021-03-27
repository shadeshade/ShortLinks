from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from Core.models import Link, Session


@admin.register(Link)
class LinkModelAdmin(ModelAdmin):
    readonly_fields = [
                'session', 'main_part', 'subpart', 'created_at'
            ]


@admin.register(Session)
class SessionModelAdmin(ModelAdmin):
    readonly_fields = [
                'session_key', 'session_data', 'expire_date'
            ]
