from ..proxmox.proxmox_auth import proxmox_auth


def vm_config(host, password, node, vmid):
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    config = proxmox.nodes(node).qemu(vmid).config().create(
        scsi0='local:9999/vm-9999-disk-0.qcow2',
        boot='c',
        bootdisk='scsi0',
        serial0="socket",
        vga='serial0',
        cipassword='ubuntu',
        ipconfig0='ip=dhcp'
    )
    return config
