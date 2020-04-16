from ..proxmox.proxmox_auth import proxmox_auth
from ..proxmox.get_task_status import get_task_status
from ..models.proxmox_cloud_provider import ProxmoxCloudProvider


def vm_clone(host, password, node, vmid, newid, name, target):
    cloud_provider_instance = ProxmoxCloudProvider.objects.get(pk=data['cloud_provider_id'])
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    template = proxmox.nodes(node).qemu(vmid)
    clone = template.clone.create(
        newid=newid,
        full='1',
        name=name,
        storage=cloud_provider_instance.shared_storage_name,
        target=target
    )
    clone_task_status = get_task_status(
        host=host,
        password=password,
        task=clone,
        node=node
    )
    while clone_task_status.get('status') == 'running':
        if clone_task_status.get('exitstatus') is None:
            clone_task_status = get_task_status(
                host=host,
                password=password,
                task=clone,
                node=node
            )
        else:
            return clone_task_status.get('exitstatus')
    return True
