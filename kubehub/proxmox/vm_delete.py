from django.http import JsonResponse

import time

from ..models.cloud_provider import CloudProvider
from ..proxmox.proxmox_auth import proxmox_auth
from ..proxmox.vm_status import vm_status
from ..proxmox.vm_stop import vm_stop


def vm_delete(data):
    cloud_provider_instance = CloudProvider.objects.get(pk=data['cloud_provider_id'])
    proxmox = proxmox_auth(
        host=cloud_provider_instance.api_endpoint,
        password=cloud_provider_instance.password
    )
    status = vm_status(
        host=cloud_provider_instance.api_endpoint,
        node=data["node"],
        password=cloud_provider_instance.password,
        vmid=data["vmid"]
    )
    while status != "stopped":
        time.sleep(35)
        vm_stop(
            host=cloud_provider_instance.api_endpoint,
            password=cloud_provider_instance.password,
            node=data["node"],
            vmid=data["vmid"]
        )
        proxmox.nodes(data["node"]).qemu(data["vmid"]).status().stop().post()
        status = vm_status(
            host=cloud_provider_instance.api_endpoint,
            node=data["node"],
            password=cloud_provider_instance.password,
            vmid=data["vmid"]
        )
    vm_list = proxmox.cluster.resources.get(type='vm')
    vmid_list = [vm["vmid"] for vm in vm_list]
    while data["vmid"] in vmid_list:
        time.sleep(20)
        delete = proxmox.nodes(data["node"]).qemu().delete(data["vmid"])
        return JsonResponse(delete, safe=False)
