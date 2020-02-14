from proxmoxer import ProxmoxAPI
import random


def get_newid(host, password):
    proxmox = ProxmoxAPI(host=host, user='root@pam', password=password, verify_ssl=False)
    vm_list = proxmox.cluster.resources.get(type='vm')
    vmid_list = [vm["vmid"] for vm in vm_list]
    newid = random.randint(100, 500)
    while newid in vmid_list:
        newid = random.randint(100, 500)
    return newid
