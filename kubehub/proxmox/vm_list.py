from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from proxmoxer import ProxmoxAPI
from ..models.cloud_provider import CloudProvider
import json


@csrf_exempt
def vm_list(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            instance = CloudProvider.objects.get(pk=data['cloud_provider_id'])
            proxmox = ProxmoxAPI(host=instance.api_endpoint, user='root@pam', password=instance.password, verify_ssl=False)
            vm = proxmox.cluster.resources.get(type='vm')
        except Exception as e:
            return JsonResponse(e.args, safe=False)
        else:
            return JsonResponse(vm, safe=False)
