from ..proxmox.proxmox_auth import proxmox_auth


def vm_status(host, password, node, vmid):
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    status = proxmox.nodes(node).qemu(vmid).status('current').get()
    return status.get("status")
