from proxmoxer import ProxmoxAPI


def vm_status(proxmox_ip, password, node, vmid):
    proxmox = ProxmoxAPI(host=proxmox_ip, user='root@pam', password=password, verify_ssl=False)
    status = proxmox.nodes(node).qemu(vmid).status('current').get()
    return status.get("status")
