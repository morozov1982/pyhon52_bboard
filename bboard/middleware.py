from django.db.models import Count

from bboard.models import Rubric


def my_middleware(next):
    # Инициализация
    def core_middleware(request):
        # Обработка клиентского запроса
        print('Обработка запроса')
        response = next(request)
        # Обработка ответа
        print('Обработка ответа')
        return response
    return core_middleware

class MyMiddleware:
    def __init__(self, next):
        self.next = next
        # Инициализация

    def __call__(self, request):
        # Обработка клиентского запроса
        print('Обработка запроса')
        response = self.next(request)
        # Обработка ответа
        print('Обработка ответа')
        return response


class RubricMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_template_response(self, request, response):
        response.context_data['rubrics'] = Rubric.objects.annotate(
                                               cnt=Count('bb')).filter(cnt__gt=0)
        return response


def rubrics(request):
    return {'rubrics': Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)}
