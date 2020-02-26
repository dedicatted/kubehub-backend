from ..models.cloud_provider import CloudProvider
from ..proxmox.get_newid import get_newid


def vmg_data_formation(data):
    cloud_provider_instance = CloudProvider.objects.get(pk=data['cloud_provider_id'])
    data_list = []
    for newid in get_newid(
            host=cloud_provider_instance.api_endpoint,
            password=cloud_provider_instance.password,
            number_of_nodes=int(data["number_of_nodes"])
    ):
        vm_data = data.copy()
        vm_data["newid"] = newid
        data_list.append(vm_data)
    return data_list
