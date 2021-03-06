from ..proxmox.proxmox_auth import proxmox_auth
from ..proxmox.get_task_status import get_task_status


def vm_create_set_up(host, password, agent, bios, cores, sockets, memory, name, ostype, scsihw, node, vmid, storage):
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    create_vm = proxmox.nodes(node).qemu.create(
        agent=agent,
        bios=bios,
        cores=cores,
        sockets=sockets,
        autostart=1,
        vmid=vmid,
        memory=int(memory)*1024,
        name=name,
        ostype=ostype,
        scsihw=scsihw,
        net0="model=virtio,bridge=vmbr0,firewall=1",
        ide2=f"{storage}:vm-{vmid}-cloudinit"
    )
    create_vm_task_status = get_task_status(
        host=host,
        password=password,
        task=create_vm,
        node=node
    )
    while create_vm_task_status.get('status') == 'running':
        if create_vm_task_status.get('exitstatus') is None:
            create_vm_task_status = get_task_status(
                host=host,
                password=password,
                task=create_vm,
                node=node
            )
        else:
            return create_vm_task_status.get('exitstatus')
    return True
