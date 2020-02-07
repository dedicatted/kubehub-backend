from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from proxmoxer import ProxmoxAPI

import json

from ..models.cloud_provider import CloudProvider


@csrf_exempt
def template_list(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            instance = CloudProvider.objects.get(pk=data['cloud_provider_id'])
            proxmox = ProxmoxAPI(host=instance.api_endpoint, user='root@pam', password=instance.password, verify_ssl=False)
            vm = proxmox.cluster.resources.get(type='vm')
            template = list(filter(lambda x: "template" in x["name"], vm))
            name_id = [{"name": temp["name"], "vmid": temp["vmid"]} for temp in template]
        except Exception as e:
            return JsonResponse(e.args, safe=False)
        else:
            return JsonResponse(name_id, safe=False)
