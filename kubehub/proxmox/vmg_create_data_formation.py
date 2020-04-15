from ..models.cloud_provider import CloudProvider
from ..proxmox.get_vmid import get_vmid


def vmg_data_formation(data):
    cloud_provider_instance = CloudProvider.objects.get(pk=data['cloud_provider_id'])
    data_list = []
    for vmid in get_vmid(
            host=cloud_provider_instance.api_endpoint,
            password=cloud_provider_instance.password,
            number_of_nodes=int(data["number_of_nodes"])
    ):
        vm_data = data.copy()
        vm_data["vmid"] = vmid
        data_list.append(vm_data)
    return data_list
