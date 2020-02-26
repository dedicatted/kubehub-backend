from proxmoxer import ProxmoxAPI


def get_vm_ip(proxmox_ip, password, node, vmid):
    proxmox = ProxmoxAPI(host=proxmox_ip, user='root@pam', password=password, verify_ssl=False)
    status = False
    while not status:
        try:
            agent = proxmox.nodes(node).qemu(vmid).agent('network-get-interfaces').get()
            ip = agent.get("result")[1].get("ip-addresses")[0].get("ip-address")
            status = True
            return ip
        except Exception:
            pass
