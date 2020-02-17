from proxmoxer import ProxmoxAPI


def get_vm_node(host, password, vmid):
    proxmox = ProxmoxAPI(host=host, user='root@pam', password=password, verify_ssl=False)
    vm = proxmox.cluster.resources.get(type='vm')
    vm_node = list(filter(lambda x: "qemu/" + str(vmid) in x["id"], vm))
    current_node = vm_node[0]["node"]
    return current_node
