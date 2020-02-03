from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from proxmoxer import ProxmoxAPI
import json


@csrf_exempt
def vm_manager_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            proxmox = ProxmoxAPI(host=data["proxmox_ip"], user='root@pam', password=data["password"], verify_ssl=False)
            agent = proxmox.nodes(data["node"]).qemu(data["vmid"]).agent('info').get()
            status = agent.get("result")[1].get("enabled")[0].get("enabled")
        except Exception as e:
            return JsonResponse(e.args, safe=False)
        else:
            return JsonResponse(status, safe=False)
