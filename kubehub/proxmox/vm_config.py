from ..proxmox.proxmox_auth import proxmox_auth
from ..proxmox.get_task_status import get_task_status


def vm_config(host, password, img_vmid, img_storage, node, vmid):
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    config = proxmox.nodes(node).qemu(vmid).config().create(
        scsi0=f'{img_storage}:{img_vmid}/vm-{img_vmid}-disk-0.qcow2',
        boot='c',
        bootdisk='scsi0',
        serial0="socket",
        vga='serial0',
        cipassword='ubuntu',
        ipconfig0='ip=dhcp'
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
