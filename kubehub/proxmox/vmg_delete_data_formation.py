from ..models.vm_group import VM
from ..models.cloud_provider import CloudProvider
from ..proxmox.get_vm_node import get_vm_node


def vmg_delete_data_formation(data):
    vm_group__instance = VM.objects.filter(vm_group=data['vm_group_id'])
    cloud_provider = vm_group__instance.values_list('cloud_provider_id', flat=True)
    cloud_provider_instance = CloudProvider.objects.get(pk=cloud_provider[0])
    vms_list = vm_group__instance.values_list('vmid', flat=True)
    vms_vmid = list(vms_list)
    data_list = []
    for vmid in vms_vmid:
        vm_data = data.copy()
        vm_data["vmid"] = vmid
        vm_data["node"] = get_vm_node(host=cloud_provider_instance.api_endpoint,
                                      password=cloud_provider_instance.password, vmid=vmid)
        vm_data["cloud_provider_id"] = cloud_provider[0]
        data_list.append(vm_data)
    return data_list
