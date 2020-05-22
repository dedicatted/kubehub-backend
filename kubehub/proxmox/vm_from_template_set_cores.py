from kubehub.proxmox.proxmox_auth import proxmox_auth
from kubehub.proxmox.get_task_status import get_task_status


def vm_from_template_set_cores(host, password, node, cores, vmid):
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    config = proxmox.nodes(node).qemu(vmid).config().create(
        cores=cores
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
