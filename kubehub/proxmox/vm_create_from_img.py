from ..models.os_image import OsImage
from ..proxmox.vm_start import vm_start
from ..proxmox.get_vm_ip import get_vm_ip
from ..proxmox.vm_status import vm_status
from ..proxmox.vm_update import vm_update
from ..proxmox.vm_upgrade import vm_upgrade
from ..proxmox.vm_migrate import vm_migrate
from ..proxmox.get_vm_node import get_vm_node
from ..proxmox.vm_move_disk import vm_move_disk
from ..proxmox.vm_disk_resize import resize_disk
from ..proxmox.vm_create_set_up import vm_create_set_up
from ..proxmox.vm_from_img_config import vm_from_img_config
from ..models.proxmox_cloud_provider import ProxmoxCloudProvider


def create_vm_from_img(data):
    cloud_provider_instance = ProxmoxCloudProvider.objects.get(pk=data['cloud_provider'])
    os_image_instance = OsImage.objects.get(pk=data['os_image'])
    vmid = data["vmid"]
    node = get_vm_node(
        host=cloud_provider_instance.api_endpoint,
        password=cloud_provider_instance.password,
        vmid=os_image_instance.vmid
    )
    set_up_vm = vm_create_set_up(
        host=cloud_provider_instance.api_endpoint,
        password=cloud_provider_instance.password,
        cores=data['cores'],
        sockets=1,
        memory=data['memory'],
        name=data['name'],
        node=node,
        vmid=vmid,
        storage=cloud_provider_instance.shared_storage_name,
        agent=os_image_instance.agent,
        bios=os_image_instance.bios,
        ostype=os_image_instance.os_type,
        scsihw=os_image_instance.scsi_controller_model

    )
    if set_up_vm:
        config = vm_from_img_config(
            host=cloud_provider_instance.api_endpoint,
            password=cloud_provider_instance.password,
            node=node,
            vmid=vmid,
            img_vmid=os_image_instance.vmid,
            img_storage=os_image_instance.storage
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
                storage=cloud_provider_instance.shared_storage_name
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
                        disk='scsi0',
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
                                "cloud_provider": cloud_provider_instance.id,
                                "cores": data["cores"],
                                'memory': data['memory'],
                                'boot_disk': data['boot_disk']
                            }


