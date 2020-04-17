from ..models.proxmox_cloud_provider import ProxmoxCloudProvider
from ..models.vm_from_img import VmFromImage
from ..models.vm_from_template import VmFromTemplate
from ..proxmox.get_vm_node import get_vm_node


def vmg_delete_data_formation(data):
    vm_group_vms_list = VmFromImage.objects.filter(vm_group=data['vm_group_id'])
    if not vm_group_vms_list:
        vm_group_vms_list = VmFromTemplate.objects.filter(vm_group=data['vm_group_id'])
    cloud_provider = vm_group_vms_list.values_list('cloud_provider_id', flat=True)
    print(cloud_provider)
    cloud_provider_instance = ProxmoxCloudProvider.objects.get(pk=cloud_provider[0])
    vms_list = vm_group_vms_list.values_list('vmid', flat=True)
    vms_vmid = list(vms_list)
    data_list = []
    for vmid in vms_vmid:
        vm_data = data.copy()
        vm_data["vmid"] = vmid
        vm_data["node"] = get_vm_node(
            host=cloud_provider_instance.api_endpoint,
            password=cloud_provider_instance.password,
            vmid=vmid
        )
        vm_data["cloud_provider_id"] = cloud_provider[0]
        data_list.append(vm_data)
    return data_list
