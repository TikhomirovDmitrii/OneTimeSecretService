from django.shortcuts import render, get_object_or_404
from .models import Secret
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, Http404
import json


@csrf_exempt #Генерируем секрет
def generate_secret(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        secret = data.get('secret')
        passphrase = data.get('passphrase')

        if not secret or not passphrase:
            return JsonResponse({'error': 'Secret and passphrase are required.'}, status=400)

        secret_key = get_random_string(64)
        new_secret = Secret.objects.create(secret_key=secret_key, secret=secret, passphrase=passphrase)
        return JsonResponse({'secret_key': secret_key})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

def get_secret(request, secret_key):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

    passphrase = request.GET.get('passphrase')

    try:
        secret_obj = get_object_or_404(Secret, secret_key=secret_key)

        if secret_obj.is_expired():
            return JsonResponse({'error': 'This secret has expired.'}, status=410)

        if not passphrase or secret_obj.passphrase != passphrase:
            return JsonResponse({'error': 'Incorrect passphrase.'}, status=403)

        secret_value = secret_obj.secret
        secret_obj.delete() #Удаляем секркт из базы данных после вызова

        return JsonResponse({'secret': secret_value})

    except Http404:
        return JsonResponse({'error': 'Secret not found.'}, status=404)
    except Exception as e:
        print(f'Unexpected error: {e}')
        return JsonResponse({'error': 'Initial server error'}, status=500)
