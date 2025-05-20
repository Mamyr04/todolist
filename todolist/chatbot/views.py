from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json
from .models import ChatMessage


@login_required
@require_POST
def chat(request):
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip().lower()

        # Простые ответы бота
        responses = {
            'привет': 'Привет! Как я могу вам помочь?',
            'как дела': 'У меня всё отлично! А у вас?',
            'помощь': 'Я могу ответить на простые вопросы. Попробуйте спросить "как добавить задачу?"',
            'как добавить задачу': 'Нажмите кнопку "Добавить задачу" на странице списка задач',
            'спасибо': 'Пожалуйста! Обращайтесь ещё!',
        }

        response = responses.get(message, 'Извините, я не понимаю ваш вопрос. Попробуйте спросить "помощь"')

        # Сохраняем сообщение в базу
        ChatMessage.objects.create(
            user=request.user,
            message=message,
            response=response
        )

        return JsonResponse({'response': response})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)