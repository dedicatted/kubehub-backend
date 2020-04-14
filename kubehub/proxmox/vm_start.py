from ..proxmox.proxmox_auth import proxmox_auth
from ..proxmox.get_task_status import get_task_status


def vm_start(host, password, node, vmid):
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    start = proxmox.nodes(node).qemu(vmid).status().start().post()
    start_task_status = get_task_status(
        host=host,
        password=password,
        task=start,
        node=node
        )
    while start_task_status.get('status') == 'running':
        if start_task_status.get('exitstatus') is None:
            start_task_status = get_task_status(
                host=host,
                password=password,
                task=start,
                node=node
            )
        else:
            return start_task_status.get('exitstatus')
    return True
