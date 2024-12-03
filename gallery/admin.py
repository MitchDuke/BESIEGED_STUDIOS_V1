from django.contrib import admin
from .models import Project, Category


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured')
    search_fields = ('title', 'category_name')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('name',)

admin.site.register(Project, ProjectAdmin)
admin.site.register(Category, CategoryAdmin)
