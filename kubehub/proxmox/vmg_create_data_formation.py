from ..models.proxmox_cloud_provider import ProxmoxCloudProvider
from ..proxmox.get_vmid import get_vmid


def vmg_data_formation(data):
    cloud_provider_instance = ProxmoxCloudProvider.objects.get(pk=data['cloud_provider'])
    vms = data.get('template_vms') if 'template_vms' in data else data.get('image_vms')
    vm_ids = get_vmid(
        host=cloud_provider_instance.api_endpoint,
        password=cloud_provider_instance.password,
        number_of_nodes=int(len(vms))
    )
    for vm, vmid in zip(vms, vm_ids):
        vm['vmid'] = vmid
        vm['cloud_provider'] = data['cloud_provider']

    return vms
