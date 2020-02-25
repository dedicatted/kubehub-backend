from ..proxmox.proxmox_auth import proxmox_auth


def vm_clone(host, password, node, vmid, newid, name, target):
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    template = proxmox.nodes(node).qemu(vmid)
    clone = template.clone.create(
        newid=newid,
        full='1',
        name=name,
        storage='kube',
        target=target
    )
    return clone
