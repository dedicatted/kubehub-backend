from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from multiprocessing import Pool

import multiprocessing
import time
import json
import random

from ..models.cloud_provider import CloudProvider
from ..proxmox.vm_clone import vm_clone
from ..proxmox.vm_start import vm_start
from ..proxmox.vm_status import vm_status
from ..proxmox.get_vm_ip import get_vm_ip


def create_cluster_node(data):
    instance = CloudProvider.objects.get(pk=data['id'])
    newid = random.randint(245, 3333)
    vm_clone(proxmox_ip=instance.api_endpoint, password=instance.password, node=data["node"], vmid='1222', newid=newid, name=data["name"])
    vm_start(proxmox_ip=instance.api_endpoint, password=instance.password, node=data["node"], vmid=newid)
    status = vm_status(proxmox_ip=instance.api_endpoint, password=instance.password, node=data["node"], vmid=newid)
    while status != "running":
        time.sleep(25)
        vm_start(proxmox_ip=instance.api_endpoint, password=instance.password, node=data["node"], vmid=newid)
        status = vm_status(proxmox_ip=instance.api_endpoint, password=instance.password, node=data["node"], vmid=newid)
        if status == "running":
            time.sleep(40)
            ip = get_vm_ip(proxmox_ip=instance.api_endpoint, password=instance.password, node=data["node"], vmid=newid)
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

