from ..proxmox.proxmox_auth import proxmox_auth


def allocate_disk_image(host, password, node, storage, vmid, size):
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    vm = proxmox.nodes(node)
    disk_image_allocation = vm.storage(storage).content().create(
        filename=f'vm-{vmid}-disk-0',
        vmid=vmid,
        size=f'{size}G'
    )
    return disk_image_allocation
