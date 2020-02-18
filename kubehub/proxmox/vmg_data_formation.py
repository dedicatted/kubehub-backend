from ..proxmox.get_newid import get_newid
from ..models.cloud_provider import CloudProvider


def vmg_data_formation(data):
    cloud_provider_instance = CloudProvider.objects.get(pk=data['cloud_provider_id'])
    data_list = []
    for newid in get_newid(cloud_provider_instance.api_endpoint, cloud_provider_instance.password,
                           int(data["number_of_nodes"])):
        vm_data = data.copy()
        vm_data["newid"] = newid
        data_list.append(vm_data)
    return data_list
