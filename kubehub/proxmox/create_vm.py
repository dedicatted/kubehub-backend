import time
import random

from ..models.cloud_provider import CloudProvider
from ..proxmox.vm_clone import vm_clone
from ..proxmox.vm_start import vm_start
from ..proxmox.vm_status import vm_status
from ..proxmox.get_vm_ip import get_vm_ip
from ..proxmox.node_list import node_list


def create_vm(data):
    instance = CloudProvider.objects.get(pk=data['cloud_provider_id'])
    newid = random.randint(100, 200)
    vm_clone(proxmox_ip=instance.api_endpoint, password=instance.password, node=data["node"], vmid=data["template_id"], newid=newid, name=data["name"], target=node_list)
    vm_start(proxmox_ip=instance.api_endpoint, password=instance.password, node=data["node"], vmid=newid)
    status = vm_status(proxmox_ip=instance.api_endpoint, password=instance.password, node=data["node"], vmid=newid)
    while status != "running":
        time.sleep(35)
        vm_start(proxmox_ip=instance.api_endpoint, password=instance.password, node=data["node"], vmid=newid)
        status = vm_status(proxmox_ip=instance.api_endpoint, password=instance.password, node=data["node"], vmid=newid)
        if status == "running":
            time.sleep(15*int(data["number_of_nodes"]))
            ip = get_vm_ip(proxmox_ip=instance.api_endpoint, password=instance.password, node=data["node"], vmid=newid)
            return ip
