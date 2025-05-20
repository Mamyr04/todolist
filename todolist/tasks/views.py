from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Task
from .forms import TaskForm
import json
from django.shortcuts import render, redirect
from .models import Product, QuizQuestion


class CustomLoginView(LoginView):
    template_name = 'tasks/login.html'
    authentication_form = AuthenticationForm

    def get_success_url(self):
        if self.request.user.is_superuser:
            return '/admin/'
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['theme'] = self.request.session.get('theme', 'light')
        return context


class CustomLogoutView(LogoutView):
    next_page = 'welcome'


def home(request):
    theme = request.session.get('theme', 'light')
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/')
        return redirect('task_list')
    return redirect('welcome')


def welcome(request):
    theme = request.session.get('theme', 'light')
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'tasks/welcome.html', {'theme': theme})


def register(request):
    theme = request.session.get('theme', 'light')
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form, 'theme': theme})


@login_required
def task_list(request):
    theme = request.session.get('theme', 'light')
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'theme': theme
    })


@login_required
def task_create(request):
    theme = request.session.get('theme', 'light')
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'theme': theme
    })


@login_required
def task_update(request, pk):
    theme = request.session.get('theme', 'light')
    task = Task.objects.get(id=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'theme': theme
    })


@login_required
def task_delete(request, pk):
    theme = request.session.get('theme', 'light')
    task = Task.objects.get(id=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {
        'task': task,
        'theme': theme
    })


@require_POST
def set_theme(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            theme = data.get('theme', 'light')
            request.session['theme'] = theme
            return JsonResponse({'status': 'ok', 'theme': theme})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error'}, status=400)
    return JsonResponse({'status': 'error'}, status=400)



def home(request):
    return render(request, 'tasks/home.html')

def about(request):
    return render(request, 'tasks/about.html')

def products_list(request):
    products = Product.objects.all()
    return render(request, 'tasks/products.html', {'products': products})

@login_required()
def quiz_test(request):
    questions = QuizQuestion.objects.all()
    if request.method == 'POST':
        score = 0
        for q in questions:
            ans = request.POST.get(f'question_{q.id}')
            if ans == q.correct_option:
                score += 1
        return render(request, 'tasks/quiz_result.html', {
            'score': score,
            'total': questions.count()
        })
    return render(request, 'tasks/quiz.html', {'questions': questions})