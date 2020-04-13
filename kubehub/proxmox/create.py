from json import loads
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..proxmox.vm_config import vm_config
from ..proxmox.move_disk import move_disk
from ..models.cloud_provider import CloudProvider
from ..proxmox.vm_status import vm_status
from ..proxmox.vm_start import vm_start
from ..proxmox.get_vm_ip import get_vm_ip
from ..proxmox.vm_create_set_up import vm_create_set_up
from ..proxmox.resize_disk import resize_disk
from ..proxmox.get_less_busy_node import get_less_busy_node
from ..proxmox.get_vm_node import get_vm_node
from ..proxmox.vm_migrate import vm_migrate
from ..proxmox.get_task_status import get_task_status


@csrf_exempt
def create_vm(request):
    if request.method == 'POST':
        data = loads(request.body)
        cloud_provider_instance = CloudProvider.objects.get(pk=data['cloud_provider_id'])
        vmid = 177
        node = get_vm_node(
            host=cloud_provider_instance.api_endpoint,
            password=cloud_provider_instance.password,
            vmid=9999
        )
        vm_create_set_up(
            host=cloud_provider_instance.api_endpoint,
            password=cloud_provider_instance.password,
            node=node,
            vmid=vmid
        )
        vm_config(
            host=cloud_provider_instance.api_endpoint,
            password=cloud_provider_instance.password,
            node=node,
            vmid=vmid
        )
        copy_img = move_disk(
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
        copy_img_task_status = get_task_status(
            host=cloud_provider_instance.api_endpoint,
            password=cloud_provider_instance.password,
            task=copy_img,
            node=get_vm_node(
                host=cloud_provider_instance.api_endpoint,
                password=cloud_provider_instance.password,
                vmid=vmid
            )
        )
        copy_img_successful = True
        while copy_img_task_status.get('status') == 'running':
            if copy_img_task_status.get('exitstatus') is None:
                copy_img_task_status = get_task_status(
                    host=cloud_provider_instance.api_endpoint,
                    password=cloud_provider_instance.password,
                    task=copy_img,
                    node=get_vm_node(
                        host=cloud_provider_instance.api_endpoint,
                        password=cloud_provider_instance.password,
                        vmid=vmid
                    )
                )
            else:
                copy_img_successful = False
                break
        if copy_img_successful:
            source_node = get_vm_node(
                host=cloud_provider_instance.api_endpoint,
                password=cloud_provider_instance.password,
                vmid=vmid
            )
            target_node = get_less_busy_node(
                host=cloud_provider_instance.api_endpoint,
                password=cloud_provider_instance.password
            )
            if source_node != target_node:
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
                    start_task_status = get_task_status(
                        host=cloud_provider_instance.api_endpoint,
                        password=cloud_provider_instance.password,
                        task=start,
                        node=get_vm_node(
                            host=cloud_provider_instance.api_endpoint,
                            password=cloud_provider_instance.password,
                            vmid=vmid
                        )
                    )
                    start_successful = True
                    while start_task_status.get('status') == 'running':
                        if start_task_status.get('exitstatus') is None:
                            start_task_status = get_task_status(
                                host=cloud_provider_instance.api_endpoint,
                                password=cloud_provider_instance.password,
                                task=start,
                                node=get_vm_node(
                                    host=cloud_provider_instance.api_endpoint,
                                    password=cloud_provider_instance.password,
                                    vmid=vmid
                                )
                            )
                        else:
                            start_successful = False
                            break
                    if start_successful:
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
