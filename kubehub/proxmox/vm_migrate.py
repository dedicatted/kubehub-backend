from ..proxmox.proxmox_auth import proxmox_auth
from ..proxmox.get_vm_node import get_vm_node
from ..proxmox.get_less_busy_node import get_less_busy_node
from ..proxmox.get_task_status import get_task_status


def vm_migrate(host, password, vmid):
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    source_node = get_vm_node(
        host=host,
        password=password,
        vmid=vmid
    )
    target_node = get_less_busy_node(
        host=host,
        password=password
    )
    if source_node != target_node:
        migrate = proxmox.nodes(source_node).qemu(vmid).migrate.create(
            target=target_node,
            migration_type='secure',
            online=1
        )
        migrate_task_status = get_task_status(
            host=host,
            password=password,
            task=migrate,
            node=source_node
        )
        migrate_successful = True
        while migrate_task_status.get('status') == 'running':
            if migrate_task_status.get('exitstatus') is None:
                migrate_task_status = get_task_status(
                    host=host,
                    password=password,
                    task=migrate,
                    node=source_node
                )
            else:
                migrate_successful = False
                break
        if migrate_successful:
            return True
        else:
            return False
    return True
