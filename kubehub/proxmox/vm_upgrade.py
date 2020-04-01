from ..proxmox.proxmox_auth import proxmox_auth
from ..proxmox.get_root_privileges import get_root_privileges


def vm_upgrade(host, password, node, vmid):
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    get_root_privileges(
        host=host,
        password=password,
        node=node,
        vmid=vmid
    )
    agent = proxmox.nodes(node).qemu(vmid).agent('exec')
    upgrade = agent.post(command='apt-get upgrade')
    return upgrade
