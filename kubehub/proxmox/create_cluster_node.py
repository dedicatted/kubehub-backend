import time
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
