from ..proxmox.proxmox_auth import proxmox_auth


def move_disk(host, password, node, vmid, storage):
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    move_volume = proxmox.nodes(node).qemu(vmid).move_disk.create(
        disk='scsi0',
        storage=storage,
        format='qcow2'
    )
    return move_volume
