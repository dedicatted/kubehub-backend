from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from proxmoxer import ProxmoxAPI
import json


@csrf_exempt
def vm_ip(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            proxmox = ProxmoxAPI(host=data["proxmox_ip"], user='root@pam', password=data["password"], verify_ssl=False)
            agent = proxmox.nodes(data["node"]).qemu(data["vmid"]).agent('network-get-interfaces').get()
            ip = agent.get("result")[1].get("ip-addresses")[0].get("ip-address")
        except Exception as e:
            return JsonResponse(e.args, safe=False)
        else:
            return JsonResponse(ip, safe=False)
