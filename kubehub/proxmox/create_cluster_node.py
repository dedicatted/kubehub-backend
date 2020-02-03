from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from proxmoxer import ProxmoxAPI
import json
import time


@csrf_exempt
def create_cluster_node(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            proxmox = ProxmoxAPI(host=data["proxmox_ip"], user='root@pam', password=data["password"], verify_ssl=False)
            template = proxmox.nodes(data["node"]).qemu(data["vmid"])
            clone = template.clone.create(newid=data["newid"], full=data["full"], name=data["name"])
            if clone:
                start_vm = proxmox.nodes(data["node"]).qemu(data["newid"]).status().start().post()
                if start_vm:
                    vm_status = proxmox.nodes(data["node"]).qemu(data["newid"]).status('current').get()
                    status = vm_status.get("status")
                    while status == "stopped":
                        vm_status = proxmox.nodes(data["node"]).qemu(data["newid"]).status('current').get()
                        status = vm_status.get("status")
                        if status == "running":
                            time.sleep(50)
                            agent = proxmox.nodes(data["node"]).qemu(data["newid"]).agent('network-get-interfaces').get()
                            ip = agent.get("result")[1].get("ip-addresses")[0].get("ip-address")
                            return JsonResponse(ip, safe=False)
        except Exception as e:
            return JsonResponse(e.args, safe=False)
