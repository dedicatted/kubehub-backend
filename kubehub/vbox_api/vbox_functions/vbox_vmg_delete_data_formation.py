from kubehub.vbox_api.models.vbox_vm import VirtualBoxVm


def vmg_delete_data_formation(data):
    vm_group_vms_list = VirtualBoxVm.objects.filter(vm_group=data['vm_group_id'])
    vms_list = vm_group_vms_list.values_list('name', flat=True)
    return list(vms_list)
