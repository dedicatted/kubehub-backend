from json import loads
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from kubehub.models.os_image import OsImage
from kubehub.serializers.os_image_serializer import OsImageSerializer


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def os_image_list(request):
    if request.method == 'GET':
        try:
            return JsonResponse({'os_image_list': list(OsImage.objects.values())})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def os_image_add(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            os_imgs = OsImageSerializer(data=data)
            if os_imgs.is_valid():
                os_img = os_imgs.create(os_imgs.validated_data)
                return JsonResponse(model_to_dict(os_img))
            else:
                return JsonResponse({'errors': os_imgs.errors})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def os_image_remove(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            pk = data.pop('id')
            instance = OsImage.objects.get(pk=pk)
            instance.delete()
            return JsonResponse({'deleted': model_to_dict(instance)})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
    return JsonResponse({'operation': 'remove'})

