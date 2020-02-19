from proxmoxer import ProxmoxAPI
from ..models.cloud_provider import CloudProvider


def get_template_list(data):
    instance = CloudProvider.objects.get(pk=data['cloud_provider_id'])
    proxmox = ProxmoxAPI(host=instance.api_endpoint, user='root@pam', password=instance.password, verify_ssl=False)
    vm = proxmox.cluster.resources.get(type='vm')
    template_list = [template for template in vm if template["template"] == 1]
    return template_list
