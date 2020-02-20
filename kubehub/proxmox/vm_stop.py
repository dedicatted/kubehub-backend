from proxmoxer import ProxmoxAPI


def vm_stop(proxmox_ip, password, node, vmid):
    proxmox = ProxmoxAPI(host=proxmox_ip, user='root@pam', password=password, verify_ssl=False)
    stop = proxmox.nodes(node).qemu(vmid).status().stop().post()
    return stop