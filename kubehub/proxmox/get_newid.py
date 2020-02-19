from proxmoxer import ProxmoxAPI


def get_newid(host, password, number_of_nodes):
    proxmox = ProxmoxAPI(host=host, user='root@pam', password=password, verify_ssl=False)
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





