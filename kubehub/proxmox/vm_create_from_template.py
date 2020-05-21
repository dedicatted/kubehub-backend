from ..models.template import Template
from ..proxmox.vm_clone import vm_clone
from ..proxmox.vm_start import vm_start
from ..proxmox.vm_update import vm_update
from ..proxmox.vm_status import vm_status
from ..proxmox.get_vm_ip import get_vm_ip
from ..proxmox.vm_upgrade import vm_upgrade
from ..proxmox.get_vm_node import get_vm_node
from ..proxmox.vm_disk_resize import resize_disk
from ..proxmox.get_less_busy_node import get_less_busy_node
from ..models.proxmox_cloud_provider import ProxmoxCloudProvider
from ..proxmox.vm_from_template_set_cores import vm_from_template_set_cores
from kubehub.proxmox.vm_from_template_set_memory import vm_from_template_set_memory


def create_vm_from_template(data):
    cloud_provider_instance = ProxmoxCloudProvider.objects.get(pk=data['cloud_provider_id'])
    template_instance = Template.objects.get(pk=data['template_id'])
    newid = data["vmid"]
    clone = vm_clone(
        host=cloud_provider_instance.api_endpoint,
        password=cloud_provider_instance.password,
        node=template_instance.node,
        vmid=template_instance.vmid,
        newid=newid,
        name=data["name"],
        target=get_less_busy_node(
            host=cloud_provider_instance.api_endpoint,
            password=cloud_provider_instance.password
        ),
        shared_storage_name=cloud_provider_instance.shared_storage_name

    )
    if clone:
        set_cores = vm_from_template_set_cores(
            host=cloud_provider_instance.api_endpoint,
            password=cloud_provider_instance.password,
            node=get_vm_node(
                host=cloud_provider_instance.api_endpoint,
                password=cloud_provider_instance.password,
                vmid=newid
            ),
            cores=data['cores'],
            vmid=newid
        )
        if set_cores:
            set_memory = vm_from_template_set_memory(
                host=cloud_provider_instance.api_endpoint,
                password=cloud_provider_instance.password,
                node=get_vm_node(
                    host=cloud_provider_instance.api_endpoint,
                    password=cloud_provider_instance.password,
                    vmid=newid
                ),
                memory=data['memory'],
                vmid=newid
            )
            if set_memory:
                set_boot_disk = resize_disk(
                    host=cloud_provider_instance.api_endpoint,
                    password=cloud_provider_instance.password,
                    node=get_vm_node(
                        host=cloud_provider_instance.api_endpoint,
                        password=cloud_provider_instance.password,
                        vmid=newid
                    ),
                    vmid=newid,
                    disk='virtio0',
                    size=data['boot_disk']
                )
                if set_boot_disk:
                    vm_start(
                        host=cloud_provider_instance.api_endpoint,
                        password=cloud_provider_instance.password,
                        node=get_vm_node(
                            host=cloud_provider_instance.api_endpoint,
                            password=cloud_provider_instance.password,
                            vmid=newid),
                        vmid=newid
                    )
                    status = vm_status(
                        host=cloud_provider_instance.api_endpoint,
                        password=cloud_provider_instance.password,
                        node=get_vm_node(
                            host=cloud_provider_instance.api_endpoint,
                            password=cloud_provider_instance.password,
                            vmid=newid),
                        vmid=newid
                    )
                    if status == "running":
                        ip = get_vm_ip(
                            proxmox_ip=cloud_provider_instance.api_endpoint,
                            password=cloud_provider_instance.password,
                            node=get_vm_node(
                                host=cloud_provider_instance.api_endpoint,
                                password=cloud_provider_instance.password,
                                vmid=newid),
                            vmid=newid
                        )
                        vm_update(
                            host=cloud_provider_instance.api_endpoint,
                            password=cloud_provider_instance.password,
                            node=get_vm_node(
                                host=cloud_provider_instance.api_endpoint,
                                password=cloud_provider_instance.password,
                                vmid=newid),
                            vmid=newid
                        )
                        vm_upgrade(
                            host=cloud_provider_instance.api_endpoint,
                            password=cloud_provider_instance.password,
                            node=get_vm_node(
                                host=cloud_provider_instance.api_endpoint,
                                password=cloud_provider_instance.password,
                                vmid=newid),
                            vmid=newid
                        )
                        return {
                            "name": data["name"],
                            "vmid": newid,
                            "ip": ip,
                            "cloud_provider_id": cloud_provider_instance.id,
                            "template_id": template_instance.id
                        }

