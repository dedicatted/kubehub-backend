from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from json import loads
from time import sleep

from ..models.proxmox_cloud_provider import ProxmoxCloudProvider
from ..proxmox.proxmox_auth import proxmox_auth
from ..proxmox.get_vm_node import get_vm_node


@csrf_exempt
def proxmox_hard_drive_cleaning(request):
    if request.method == 'POST':
        data = loads(request.body)
        cloud_provider_instance = ProxmoxCloudProvider.objects.get(pk=data['cloud_provider_id'])
        vmid_list = list(range(int(data['from']), int(data['to'])))
        proxmox = proxmox_auth(
            host=cloud_provider_instance.api_endpoint,
            password=cloud_provider_instance.password
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
