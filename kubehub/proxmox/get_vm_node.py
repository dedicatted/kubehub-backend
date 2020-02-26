from ..proxmox.proxmox_auth import proxmox_auth


def get_vm_node(host, password, vmid):
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    vm = proxmox.cluster.resources.get(type='vm')
    vm_node = list(filter(lambda x: "qemu/" + str(vmid) in x["id"], vm))
    current_node = vm_node[0]["node"]
    return current_node
