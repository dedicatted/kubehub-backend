from kubehub.vbox_api.vbox_functions.vbox_get_new_vm_name import get_new_vm_name


def vmg_create_data_formation(data):
    vms = data.get('vbox_vms')
    vm_names = get_new_vm_name(
        name=data.get('name'),
        number_of_nodes=int(len(vms))
    )
    for vm, name in zip(vms, vm_names):
        vm['name'] = name
        vm['cloud_provider'] = data['cloud_provider']
    return vms
