from proxmoxer import ProxmoxAPI


def get_newid(host, password):
    proxmox = ProxmoxAPI(host=host, user='root@pam', password=password, verify_ssl=False)
    vm_list = proxmox.cluster.resources.get(type='vm')
    vmid_list = [vm["vmid"] for vm in vm_list]
    for newid in range(100, 999999999):
        if newid not in vmid_list:
            return newid
