from json import loads
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..proxmox.vm_start import vm_start
from ..proxmox.vm_config import vm_config
from ..proxmox.get_vm_ip import get_vm_ip
from ..proxmox.vm_status import vm_status
from ..proxmox.vm_migrate import vm_migrate
from ..proxmox.get_vm_node import get_vm_node
from ..proxmox.vm_move_disk import vm_move_disk
from ..proxmox.vm_disk_resize import resize_disk
from ..models.cloud_provider import CloudProvider
from ..proxmox.vm_create_set_up import vm_create_set_up


@csrf_exempt
def create_vm(request):
    if request.method == 'POST':
        data = loads(request.body)
        cloud_provider_instance = CloudProvider.objects.get(pk=data['cloud_provider_id'])
        vmid = 185
        node = get_vm_node(
            host=cloud_provider_instance.api_endpoint,
            password=cloud_provider_instance.password,
            vmid=9999
        )
        set_up_vm = vm_create_set_up(
            host=cloud_provider_instance.api_endpoint,
            password=cloud_provider_instance.password,
            cores=1,
            sockets=1,
            memory=2048,
            name="VM",
            node=node,
            vmid=vmid,
            storage='kube'
        )
        if set_up_vm:
            config = vm_config(
                host=cloud_provider_instance.api_endpoint,
                password=cloud_provider_instance.password,
                node=node,
                vmid=vmid
            )
            if config:
                move_disk = vm_move_disk(
                    host=cloud_provider_instance.api_endpoint,
                    password=cloud_provider_instance.password,
                    node=get_vm_node(
                        host=cloud_provider_instance.api_endpoint,
                        password=cloud_provider_instance.password,
                        vmid=vmid
                    ),
                    vmid=vmid,
                    storage='kube'
                )
                if move_disk:
                    migrate = vm_migrate(
                        host=cloud_provider_instance.api_endpoint,
                        password=cloud_provider_instance.password,
                        vmid=vmid,
                    )
                    if migrate:
                        resize_disk(
                            host=cloud_provider_instance.api_endpoint,
                            password=cloud_provider_instance.password,
                            node=get_vm_node(
                                host=cloud_provider_instance.api_endpoint,
                                password=cloud_provider_instance.password,
                                vmid=vmid
                            ),
                            vmid=vmid,
                            size=16
                        )
                        start = vm_start(
                            host=cloud_provider_instance.api_endpoint,
                            password=cloud_provider_instance.password,
                            node=get_vm_node(
                                host=cloud_provider_instance.api_endpoint,
                                password=cloud_provider_instance.password,
                                vmid=vmid),
                            vmid=vmid
                        )
                        if start:
                            status = vm_status(
                                host=cloud_provider_instance.api_endpoint,
                                password=cloud_provider_instance.password,
                                node=get_vm_node(
                                    host=cloud_provider_instance.api_endpoint,
                                    password=cloud_provider_instance.password,
                                    vmid=vmid),
                                vmid=vmid
                            )
                            if status == "running":
                                ip = get_vm_ip(
                                    proxmox_ip=cloud_provider_instance.api_endpoint,
                                    password=cloud_provider_instance.password,
                                    node=get_vm_node(
                                        host=cloud_provider_instance.api_endpoint,
                                        password=cloud_provider_instance.password,
                                        vmid=vmid),
                                    vmid=vmid
                                )
                                return JsonResponse(str(ip), safe=False)




