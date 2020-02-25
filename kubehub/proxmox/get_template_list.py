from ..proxmox.proxmox_auth import proxmox_auth
from ..models.cloud_provider import CloudProvider


def get_template_list(data):
    cloud_provider_instance = CloudProvider.objects.get(pk=data['cloud_provider_id'])
    proxmox = proxmox_auth(
        host=cloud_provider_instance.api_endpoint,
        password=cloud_provider_instance.password
    )
    vm = proxmox.cluster.resources.get(type='vm')
    template_list = [template for template in vm if template["template"] == 1]
    return template_list
