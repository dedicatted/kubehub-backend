from ..proxmox.proxmox_auth import proxmox_auth


def resize_disk(host, password, node, vmid, size):
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    disk_resize = proxmox.nodes(node).qemu(vmid).resize.set(
        disk='scsi0',
        size=f'{size}G'
    )
    return disk_resize
