from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title





class Product(models.Model):
    name        = models.CharField("Название", max_length=200)
    price       = models.DecimalField("Цена", max_digits=8, decimal_places=2)
    description = models.TextField("Описание", blank=True)
    image       = models.ImageField(
                    "Фото товара",
                    upload_to="products/",      # папка media/products/
                    blank=True,
                    null=True
                  )

    def __str__(self):
        return self.name

class QuizQuestion(models.Model):
    text           = models.CharField("Вопрос", max_length=255)
    option1        = models.CharField("Вариант 1", max_length=255)
    option2        = models.CharField("Вариант 2", max_length=255)
    option3        = models.CharField("Вариант 3", max_length=255)
    option4        = models.CharField("Вариант 4", max_length=255)
    correct_option = models.CharField(
        "Правильный вариант",
        max_length=1,
        choices=[('1','1'), ('2','2'), ('3','3'), ('4','4')]
    )

    def __str__(self):
        return self.text