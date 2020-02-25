from ..proxmox.vm_delete import vm_delete
from ..proxmox.vmg_delete_data_formation import vmg_delete_data_formation


def vm_group_delete(data):
    vm_group_data = vmg_delete_data_formation(data)
    delete = []
    for vm in vm_group_data:
        delete.append(vm_delete(vm))
    return delete
