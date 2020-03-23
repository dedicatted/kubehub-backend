from ..proxmox.proxmox_auth import proxmox_auth
from ..proxmox.get_root_privileges import get_root_privileges


def get_file_data(host, password, node, vmid, filename):
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
    agent = proxmox.nodes(node).qemu(vmid).agent('file-read')
    read_config = agent.get(file=filename)
    return read_config
