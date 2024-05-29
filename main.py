# В файле views.py:

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import random
import string

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Создаем пользователя
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        # Отправляем письмо с подтверждением регистрации
        send_registration_confirmation_email(user)

        return JsonResponse({'message': 'Пользователь успешно зарегистрирован!'})

@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Генерируем новый пароль
        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()

            # Отправляем письмо с новым паролем
            send_password_reset_email(user, new_password)

            return JsonResponse({'message': 'Новый пароль отправлен на вашу почту.'})
        except User.DoesNotExist:
            return JsonResponse({'message': 'Пользователь с такой почтой не найден.'})

def send_registration_confirmation_email(user):
    subject='Подтверждение регистрации'
    message='Добро пожаловать, {}! Ваша регистрация успешно подтверждена.'.format(user.username)
    from_email='email@example.com'
    to_list=[user.email]
    send_mail(subject,message,from_email,to_list,fail_silently=False)

def send_password_reset_email(user, new_password):
    subject='Сброс пароля'
    message='Ваш новый пароль: {}'.format(new_password)
    from_email='email@example.com'
    to_list=[user.email]
    send_mail(subject,message,from_email,to_list,fail_silently=False)
