from django.http import JsonResponse
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
