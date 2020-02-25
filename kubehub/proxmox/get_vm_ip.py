from ..proxmox.proxmox_auth import proxmox_auth


def get_vm_ip(proxmox_ip, password, node, vmid):
    proxmox = proxmox_auth(
        host=proxmox_ip,
        password=password
    )
    status = False
    while not status:
        try:
            agent = proxmox.nodes(node).qemu(vmid).agent('network-get-interfaces').get()
            ip = agent.get("result")[1].get("ip-addresses")[0].get("ip-address")
            status = True
            return ip
        except Exception:
            pass
