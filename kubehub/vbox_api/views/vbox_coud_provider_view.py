from json import loads
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from kubehub.vbox_api.models.vbox_cloud_provider import VirtualBoxCloudProvider
from kubehub.vbox_api.serializers.vbox_cloud_provider_serializer import VirtualBoxCloudProviderSerializer


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def virtualbox_provider_list(request):
    if request.method == 'GET':
        try:
            return JsonResponse({'virtualbox_provider_list': list(VirtualBoxCloudProvider.objects.values())})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def virtualbox_provider_add(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            cps = VirtualBoxCloudProviderSerializer(data=data)
            if cps.is_valid():
                cp = cps.create(cps.validated_data)
                return JsonResponse(model_to_dict(cp))
            else:
                return JsonResponse({'errors': cps.errors})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})

