from proxmoxer import ProxmoxAPI
from ..models.cloud_provider import CloudProvider


def get_template_list(data):
    instance = CloudProvider.objects.get(pk=data['cloud_provider_id'])
    proxmox = ProxmoxAPI(host=instance.api_endpoint, user='root@pam', password=instance.password, verify_ssl=False)
    vm = proxmox.cluster.resources.get(type='vm')
    template = list(filter(lambda x: "template" in x["name"], vm))
    return template
