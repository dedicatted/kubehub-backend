from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from proxmoxer import ProxmoxAPI
import json


@csrf_exempt
def vm_clone(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            proxmox = ProxmoxAPI(host=data["proxmox_ip"], user='root@pam', password=data["password"], verify_ssl=False)
            template = proxmox.nodes(data["node"]).qemu(data["vmid"])
            clone = template.clone.create(newid=data["newid"], full=data["full"], name=data["name"])
        except Exception as e:
            return JsonResponse(e.args, safe=False)
        else:
            return JsonResponse(clone, safe=False)
