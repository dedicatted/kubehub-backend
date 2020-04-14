from ..proxmox.proxmox_auth import proxmox_auth


def get_storage_content(host, password, node, storage):
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    get_content = proxmox.nodes(node).storage(storage).content().get()
    return get_content
