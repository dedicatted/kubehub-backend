from ..proxmox.proxmox_auth import proxmox_auth


def get_file_data(host, password, node, vmid, filename):
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    agent = proxmox.nodes(node).qemu(vmid).agent('file-read')
    read_config = agent.get(file=filename)
    return read_config
