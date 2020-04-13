from ..proxmox.proxmox_auth import proxmox_auth


def get_task_status(host, password, task, node):
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    task_status = proxmox.nodes(node).tasks(task).status.get()
    return task_status
