from django.contrib import admin
from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured')
    search_fields = ('title', 'category_name')

admin.site.register(Project, ProjectAdmin)
