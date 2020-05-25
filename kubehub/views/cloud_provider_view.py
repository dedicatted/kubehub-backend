from json import loads
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt

from kubehub.models.proxmox_cloud_provider import ProxmoxCloudProvider
from kubehub.vbox_api.models.vbox_cloud_provider import VirtualBoxCloudProvider


@csrf_exempt
def all_cloud_provider_list(request):
    if request.method == 'GET':
        try:
            cp_list = list(VirtualBoxCloudProvider.objects.values()) + list(ProxmoxCloudProvider.objects.values())
            return JsonResponse({'cloud_provider_list': cp_list})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@csrf_exempt
def cloud_provider_remove(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            pk = data.get('cloud_provider_id')
            if data.get('cp_type') == 'VirtualBox':
                instance = VirtualBoxCloudProvider.objects.get(pk=pk)
                instance.delete()
                return JsonResponse({'deleted': model_to_dict(instance)})
            if data.get('cp_type') == 'Proxmox':
                instance = ProxmoxCloudProvider.objects.get(pk=pk)
                instance.delete()
                return JsonResponse({'deleted': model_to_dict(instance)})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
