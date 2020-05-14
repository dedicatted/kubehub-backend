from os import mkdir
from os.path import exists

from kubehub.vbox_api.models.vbox_cloud_provider import VirtualBoxCloudProvider


def get_machine_folder(cloud_provider_id):
    cloud_provider_instance = VirtualBoxCloudProvider.objects.get(pk=cloud_provider_id)
    machine_folder_path = cloud_provider_instance.machine_folder
    if not exists(path=machine_folder_path):
        try:
            mkdir(machine_folder_path)
            return machine_folder_path
        except Exception as e:
            return {'errors': {f'{type(e).__name__}': [str(e)]}}
    else:
        return machine_folder_path
