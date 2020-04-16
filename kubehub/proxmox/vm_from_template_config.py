from ..proxmox.proxmox_auth import proxmox_auth
from ..proxmox.get_task_status import get_task_status


def vm_from_template_config(host, password, node, cores, sockets, vmid, memory):
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    config = proxmox.nodes(node).qemu(vmid).config().create(
        cores=cores,
        sockets=sockets,
        memory=memory,
    )
    config_task_status = get_task_status(
        host=host,
        password=password,
        task=config,
        node=node
    )
    while config_task_status.get('status') == 'running':
        if config_task_status.get('exitstatus') is None:
            config_task_status = get_task_status(
                host=host,
                password=password,
                task=config,
                node=node
            )
        else:
            return config_task_status.get('exitstatus')
    return True
