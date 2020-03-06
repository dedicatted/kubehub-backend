from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from json import loads
from time import sleep

from ..models.cloud_provider import CloudProvider
from ..proxmox.proxmox_auth import proxmox_auth
from ..proxmox.get_vm_node import get_vm_node
from ..proxmox.vm_stop import vm_stop


@csrf_exempt
def proxmox_hard_drive_cleaning(request):
    if request.method == 'POST':
        data = loads(request.body)
        cloud_provider_instance = CloudProvider.objects.get(pk=data['cloud_provider_id'])
        vmid_list = list(range(int(data['from']), int(data['to'])))
        proxmox = proxmox_auth(
            host=cloud_provider_instance.api_endpoint,
            password=cloud_provider_instance.password
        )
        for vmid in vmid_list:
            node = get_vm_node(
                host=cloud_provider_instance.api_endpoint,
                password=cloud_provider_instance.password,
                vmid=vmid
            )
            vm_stop(
                host=cloud_provider_instance.api_endpoint,
                password=cloud_provider_instance.password,
                node=node,
                vmid=vmid
            )
        deleted_vms_list = []
        for vmid in vmid_list:
            node = get_vm_node(
                host=cloud_provider_instance.api_endpoint,
                password=cloud_provider_instance.password,
                vmid=vmid
            )
            delete = proxmox.nodes(node).qemu().delete(vmid)
            sleep(60)
            if delete:
                deleted_vms_list.append(vmid)
        return JsonResponse(str(deleted_vms_list), safe=False)
