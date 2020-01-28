from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from proxmoxer import ProxmoxAPI
import json


def login(proxmox_ip, password):
    return ProxmoxAPI(proxmox_ip, user='root@pam', password=password, verify_ssl=False)


@csrf_exempt
def node_list(requst):
    if requst.method == 'POST':
        try:
            data = json.loads(requst.body)
            proxmox = login(proxmox_ip=data["proxmox_ip"], password=data["password"])
            nodes = proxmox.nodes.get()
        except Exception as e:
            return JsonResponse(e.args, safe=False)
        else:
            return JsonResponse(nodes, safe=False)
