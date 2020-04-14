from ..proxmox.proxmox_auth import proxmox_auth
from ..proxmox.get_task_status import get_task_status


def vm_move_disk(host, password, node, vmid, storage):
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    move_disk = proxmox.nodes(node).qemu(vmid).move_disk.create(
        disk='scsi0',
        storage=storage,
        format='qcow2'
    )
    move_disk_task_status = get_task_status(
        host=host,
        password=password,
        task=move_disk,
        node=node
    )
    while move_disk_task_status.get('status') == 'running':
        if move_disk_task_status.get('exitstatus') is None:
            move_disk_task_status = get_task_status(
                host=host,
                password=password,
                task=move_disk,
                node=node
            )
        else:
            return move_disk_task_status.get('exitstatus')
    return True
