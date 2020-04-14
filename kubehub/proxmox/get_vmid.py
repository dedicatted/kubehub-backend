from ..proxmox.proxmox_auth import proxmox_auth


def get_vmid(host, password, number_of_nodes):
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    vm_list = proxmox.cluster.resources.get(type='vm')
    vmid_list = [vm["vmid"] for vm in vm_list]
    newid_list = []
    for newid in range(100, 999999999):
        if len(newid_list) == number_of_nodes:
            break
        else:
            if newid not in vmid_list and newid not in newid_list and len(newid_list) < number_of_nodes:
                newid_list.append(newid)
    return newid_list
