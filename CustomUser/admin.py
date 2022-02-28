from django.contrib import admin
from . import models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'student_name',
        'email',
        'date_joined',
    )

    list_display_links = (
        'student_name',
        'email',
    )