from ..proxmox.proxmox_auth import proxmox_auth


def vm_create_set_up(host, password, node, vmid):
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    create_vm = proxmox.nodes(node).qemu.create(
        agent="enabled=1",
        bios="seabios",
        cores=1,
        sockets=1,
        autostart=1,
        vmid=vmid,
        memory=2048,
        ostype="l26",
        scsihw="virtio-scsi-pci",
        net0="model=virtio,bridge=vmbr0,firewall=1",
        ide2=f"kube:vm-{vmid}-cloudinit"
    )
    return create_vm
