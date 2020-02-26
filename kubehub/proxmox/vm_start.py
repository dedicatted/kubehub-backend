from ..proxmox.proxmox_auth import proxmox_auth


def vm_start(host, password, node, vmid):
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    start = proxmox.nodes(node).qemu(vmid).status().start().post()
    return start
