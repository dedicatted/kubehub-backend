import time

from ..models.cloud_provider import CloudProvider
from ..models.template import Template
from ..proxmox.vm_clone import vm_clone
from ..proxmox.vm_start import vm_start
from ..proxmox.vm_status import vm_status
from ..proxmox.get_vm_ip import get_vm_ip
from ..proxmox.get_less_busy_node import get_less_busy_node
from ..proxmox.get_vm_node import get_vm_node
from ..proxmox.get_newid import get_newid


def create_vm(data):
    cloud_provider_instance = CloudProvider.objects.get(pk=data['cloud_provider_id'])
    template_instance = Template.objects.get(pk=data['template_id'])
    newid = get_newid(host=cloud_provider_instance.api_endpoint, password=cloud_provider_instance.password)
    vm_clone(proxmox_ip=cloud_provider_instance.api_endpoint, password=cloud_provider_instance.password, node=template_instance.node, vmid=template_instance.vmid, newid=newid, name=data["name"], target=get_less_busy_node(host=cloud_provider_instance.api_endpoint, password=cloud_provider_instance.password))
    vm_start(proxmox_ip=cloud_provider_instance.api_endpoint, password=cloud_provider_instance.password, node=get_vm_node(host=cloud_provider_instance.api_endpoint, password=cloud_provider_instance.password, vmid=newid), vmid=newid)
    status = vm_status(proxmox_ip=cloud_provider_instance.api_endpoint, password=cloud_provider_instance.password, node=get_vm_node(host=cloud_provider_instance.api_endpoint, password=cloud_provider_instance.password, vmid=newid), vmid=newid)
    while status != "running":
        time.sleep(35)
        vm_start(proxmox_ip=cloud_provider_instance.api_endpoint, password=cloud_provider_instance.password, node=get_vm_node(host=cloud_provider_instance.api_endpoint, password=cloud_provider_instance.password, vmid=newid), vmid=newid)
        status = vm_status(proxmox_ip=cloud_provider_instance.api_endpoint, password=cloud_provider_instance.password, node=get_vm_node(host=cloud_provider_instance.api_endpoint, password=cloud_provider_instance.password, vmid=newid), vmid=newid)
        if status == "running":
            time.sleep(15*int(data["number_of_nodes"]))
            ip = get_vm_ip(proxmox_ip=cloud_provider_instance.api_endpoint, password=cloud_provider_instance.password, node=get_vm_node(host=cloud_provider_instance.api_endpoint, password=cloud_provider_instance.password, vmid=newid), vmid=newid)
            return {"name": data["name"], "vmid": newid, "ip": ip, "cloud_provider_id": cloud_provider_instance.id, "template_id": template_instance.id}


