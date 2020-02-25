from ..proxmox.proxmox_auth import proxmox_auth


def vm_stop(host, password, node, vmid):
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    stop = proxmox.nodes(node).qemu(vmid).status().stop().post()
    return stop
