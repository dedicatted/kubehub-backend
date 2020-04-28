from json import loads
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


from kubehub.models.proxmox_cloud_provider import ProxmoxCloudProvider
from kubehub.serializers.proxmox_cloud_provider_serializer import ProxmoxCloudProviderSerializer


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def proxmox_cloud_provider_list(request):
    if request.method == 'GET':
        try:
            return JsonResponse({'cloud_provider_list': list(ProxmoxCloudProvider.objects.values())})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def proxmox_cloud_provider_add(request):
    if request.method == 'POST':
        data = loads(request.body)
        cps = ProxmoxCloudProviderSerializer(data=data)
        if cps.is_valid():
            cp = cps.create(cps.validated_data)
            return JsonResponse(model_to_dict(cp))
        else:
            return JsonResponse({'errors': cps.errors})
    return JsonResponse({'operation': 'add'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def proxmox_cloud_provider_remove(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            pk = data.pop('id')
            instance = ProxmoxCloudProvider.objects.get(pk=pk)
            instance.delete()
            return JsonResponse({'deleted': model_to_dict(instance)})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
    return JsonResponse({'operation': 'remove'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def proxmox_cloud_provider_edit(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            pk = data.pop('id')
            instance = ProxmoxCloudProvider.objects.get(pk=pk)
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
        cps = ProxmoxCloudProviderSerializer(data=data, partial=True)
        if cps.is_valid():
            cp = cps.update(instance, cps.validated_data)
            return JsonResponse(model_to_dict(cp))
        else:
            return JsonResponse({'errors': cps.errors})
    return JsonResponse({'operation': 'edit'})
