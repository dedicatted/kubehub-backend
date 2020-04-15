from ..proxmox.vm_start import vm_start
from ..proxmox.vm_config import vm_config
from ..proxmox.get_vm_ip import get_vm_ip
from ..proxmox.vm_status import vm_status
from ..proxmox.vm_update import vm_update
from ..proxmox.vm_upgrade import vm_upgrade
from ..proxmox.vm_migrate import vm_migrate
from ..proxmox.get_vm_node import get_vm_node
from ..proxmox.vm_move_disk import vm_move_disk
from ..proxmox.vm_disk_resize import resize_disk
from ..models.cloud_provider import CloudProvider
from ..proxmox.vm_create_set_up import vm_create_set_up


def create_vm_from_img(data):
    cloud_provider_instance = CloudProvider.objects.get(pk=data['cloud_provider_id'])
    vmid = data["vmid"]
    node = get_vm_node(
        host=cloud_provider_instance.api_endpoint,
        password=cloud_provider_instance.password,
        vmid=9999
    )
    set_up_vm = vm_create_set_up(
        host=cloud_provider_instance.api_endpoint,
        password=cloud_provider_instance.password,
        cores=data['cores'],
        sockets=data['sockets'],
        memory=data['memory'],
        name=data['name'],
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
                        size=data['boot_disk']
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
                        if status == 'running':
                            ip = get_vm_ip(
                                proxmox_ip=cloud_provider_instance.api_endpoint,
                                password=cloud_provider_instance.password,
                                node=get_vm_node(
                                    host=cloud_provider_instance.api_endpoint,
                                    password=cloud_provider_instance.password,
                                    vmid=vmid),
                                vmid=vmid
                            )
                            vm_update(
                                host=cloud_provider_instance.api_endpoint,
                                password=cloud_provider_instance.password,
                                node=get_vm_node(
                                    host=cloud_provider_instance.api_endpoint,
                                    password=cloud_provider_instance.password,
                                    vmid=vmid),
                                vmid=vmid
                            )
                            vm_upgrade(
                                host=cloud_provider_instance.api_endpoint,
                                password=cloud_provider_instance.password,
                                node=get_vm_node(
                                    host=cloud_provider_instance.api_endpoint,
                                    password=cloud_provider_instance.password,
                                    vmid=vmid),
                                vmid=vmid
                            )
                            return {
                                "name": data["name"],
                                "vmid": vmid,
                                "ip": ip,
                                "cloud_provider_id": cloud_provider_instance.id,
                                "cores": data["cores"],
                                "sockets": data["sockets"],
                                'memory': data['memory'],
                                'boot_disk': data['boot_disk']
                            }


