from django.contrib import admin
from .models import Project, Category


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_categories', 'is_featured')
    search_fields = ('title', 'category_name')

    def display_categories(self, obj):
        return ', '.join([category.name for category in obj.category.all()])

    display_categories.short_description = 'Categories'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Category, CategoryAdmin)
