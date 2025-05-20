from django.contrib import admin
from .models import Product, QuizQuestion

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','price')

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('id','text')