from json import loads
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt

from kubehub.models.user import User
from kubehub.serializers.user_serializer import UserSerializer


@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        try:
            return JsonResponse({'user_list': list(User.objects.values())})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@csrf_exempt
def user_add(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            users = UserSerializer(data=data)
            if users.is_valid():
                user = users.create(users.validated_data)
                return JsonResponse(model_to_dict(user))
            else:
                return JsonResponse({'errors': users.errors})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@csrf_exempt
def user_remove(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            user_id = data.pop('id')
            instance = User.objects.get(pk=user_id)
            instance.delete()
            return JsonResponse({'deleted': model_to_dict(instance)})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@csrf_exempt
def user_edit(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            user_id = data.pop('id')
            instance = User.objects.get(pk=user_id)
            users = UserSerializer(data=data, partial=True)
            if users.is_valid():
                user = users.update(instance, users.validated_data)
                return JsonResponse(model_to_dict(user))
            else:
                return JsonResponse({'errors': users.errors})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})

