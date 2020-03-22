from ..proxmox.proxmox_auth import proxmox_auth


def get_root_privileges(host, password, node, vmid):
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    agent = proxmox.nodes(node).qemu(vmid).agent('exec')
    su = agent.post(command='sudo su')
    return su
