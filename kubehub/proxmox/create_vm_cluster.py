from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import multiprocessing
from multiprocessing import Pool
from proxmoxer import ProxmoxAPI
import time
import json
import random


def create_cluster_node(data):
    proxmox = ProxmoxAPI(host=data["proxmox_ip"], user='root@pam', password=data["password"], verify_ssl=False)
    template = proxmox.nodes('pve-01').qemu('1222')
    newid = random.randint(245, 3333)
    clone = template.clone.create(newid=newid, full='1', name=data["name"])
    start = proxmox.nodes(data["node"]).qemu(newid).status().start().post()
    vm_status = proxmox.nodes(data["node"]).qemu(newid).status('current').get()
    status = vm_status.get("status")
    while status != "running":
        time.sleep(25)
        start = proxmox.nodes(data["node"]).qemu(newid).status().start().post()
        vm_status = proxmox.nodes(data["node"]).qemu(newid).status('current').get()
        status = vm_status.get("status")
        if status == "running":
            time.sleep(25)
            agent = proxmox.nodes(data["node"]).qemu(newid).agent('network-get-interfaces').get()
            ip = agent.get("result")[1].get("ip-addresses")[0].get("ip-address")
            return ip


@csrf_exempt
def create_vm_cluster(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            number_of_cores = multiprocessing.cpu_count()
            pool = Pool(number_of_cores)
            data = [data]*int(data["number_of_nodes"])
            return JsonResponse(str(pool.map(create_cluster_node, data)), safe=False)
        except Exception as e:
            return JsonResponse(e.args, safe=False)

