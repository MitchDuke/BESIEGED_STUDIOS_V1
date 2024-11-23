from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery/images/')
