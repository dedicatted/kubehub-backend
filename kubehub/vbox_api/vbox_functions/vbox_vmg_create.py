from kubehub.vbox_api.vbox_functions.vbox_vm_create import vbox_create_vm
from kubehub.vbox_api.vbox_functions.vbox_vmg_create_data_formation import vmg_create_data_formation


def create_vm_group(data):
    vm_group_data = vmg_create_data_formation(data)
    create = []
    for vm in vm_group_data:
        create.append(vbox_create_vm(vm))
    return create
