from json import loads
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from kubehub.models.proxmox_cloud_provider import ProxmoxCloudProvider
from kubehub.vbox_api.models.vbox_cloud_provider import VirtualBoxCloudProvider
from kubehub.serializers.proxmox_cloud_provider_serializer import ProxmoxCloudProviderSerializer
from kubehub.vbox_api.serializers.vbox_cloud_provider_serializer import VirtualBoxCloudProviderSerializer


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_cloud_provider_list(request):
    if request.method == 'GET':
        try:
            cp_list = list(VirtualBoxCloudProvider.objects.values()) + list(ProxmoxCloudProvider.objects.values())
            return JsonResponse({'cloud_provider_list': cp_list})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cloud_provider_remove(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            pk = data.get('cloud_provider_id')
            provider = data.get('cp_type')
            if provider == 'VirtualBox':
                instance = VirtualBoxCloudProvider.objects.get(pk=pk)
                instance.delete()
                return JsonResponse({'deleted': model_to_dict(instance)})
            elif provider == 'Proxmox':
                instance = ProxmoxCloudProvider.objects.get(pk=pk)
                instance.delete()
                return JsonResponse({'deleted': model_to_dict(instance)})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cloud_provider_edit(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            pk = data.get('cloud_provider_id')
            provider = data.get('cp_type')
            if provider == 'VirtualBox':
                instance = VirtualBoxCloudProvider.objects.get(pk=pk)
                cps = VirtualBoxCloudProviderSerializer(data=data, partial=True)
                if cps.is_valid():
                    cp = cps.update(instance, cps.validated_data)
                    return JsonResponse(model_to_dict(cp))
                else:
                    return JsonResponse({'errors': cps.errors})
            elif provider == 'Proxmox':
                instance = ProxmoxCloudProvider.objects.get(pk=pk)
                cps = ProxmoxCloudProviderSerializer(data=data, partial=True)
                if cps.is_valid():
                    cp = cps.update(instance, cps.validated_data)
                    return JsonResponse(model_to_dict(cp))
                else:
                    return JsonResponse({'errors': cps.errors})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
