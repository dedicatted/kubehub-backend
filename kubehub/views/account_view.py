from json import loads
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes

from kubehub.models.account import Account
from kubehub.serializers.account_serializer import RegistrationSerializer


@api_view(['GET'])
@permission_classes([IsAdminUser])
@csrf_exempt
def account_list(request):
    if request.method == 'GET':
        try:
            return JsonResponse({'user_list': list(Account.objects.values())})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@api_view(['POST'])
@permission_classes([IsAdminUser])
@csrf_exempt
def account_add(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            serializer = RegistrationSerializer(data=data)
            if serializer.is_valid():
                account = serializer.save()
                return JsonResponse(model_to_dict(account))
            else:
                return JsonResponse({'errors': serializer.errors})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@api_view(['POST'])
@permission_classes([IsAdminUser])
@csrf_exempt
def account_remove(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            user_id = data.pop('id')
            instance = Account.objects.get(pk=user_id)
            instance.delete()
            return JsonResponse({'deleted': model_to_dict(instance)})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@api_view(['POST'])
@permission_classes([IsAdminUser])
@csrf_exempt
def account_edit(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            user_id = data.pop('id')
            instance = Account.objects.get(pk=user_id)
            users = RegistrationSerializer(data=data, partial=True)
            if users.is_valid():
                user = users.update(instance, users.validated_data)
                return JsonResponse(model_to_dict(user))
            else:
                return JsonResponse({'errors': users.errors})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@api_view(['POST'])
@permission_classes([IsAdminUser])
@csrf_exempt
def get_account_data(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            user_id = data.pop('id')
            user_data = Account.objects.get(pk=user_id)
            return JsonResponse(model_to_dict(user_data))
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
