from django.urls import path
from . import views

urlpatterns = [
    # Основные маршруты
    path('', views.home, name='home'),
    path('welcome/', views.welcome, name='welcome'),

    # Аутентификация
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    # Управление темами
    path('set-theme/', views.set_theme, name='set_theme'),

    # Маршруты для задач
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/add/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/update/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),


    path('about/', views.about, name='about'),
    path('products/', views.products_list, name='products'),
    path('quiz/', views.quiz_test, name='quiz'),
]

