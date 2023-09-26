from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    name = models.CharField(max_length=50, unique=True)
    user_access = models.ManyToManyField(User, related_name='products_access')

class Lesson(models.Model):
    name = models.CharField(max_length=100, unique=True)
    link_video = models.URLField(unique=True)
    duration_sec = models.IntegerField()
    products = models.ManyToManyField(Product, related_name="lessons")

class LessonStatus(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    view_time_sec = models.IntegerField(default=0)
    view_or_notview = models.BooleanField(default=False)

