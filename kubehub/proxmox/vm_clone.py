from proxmoxer import ProxmoxAPI


def vm_clone(proxmox_ip, password, node, vmid, newid, name, target):
    proxmox = ProxmoxAPI(host=proxmox_ip, user='root@pam', password=password, verify_ssl=False)
    template = proxmox.nodes(node).qemu(vmid)
    clone = template.clone.create(newid=newid, full='1', name=name,  storage='kube', target=target)
    return clone
