from json import loads
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..proxmox.proxmox_auth import proxmox_auth
from ..models.cloud_provider import CloudProvider
from ..proxmox.allocate_disk_image import allocate_disk_image


@csrf_exempt
def create_vm(request):
    if request.method == 'POST':
        data = loads(request.body)
        cloud_provider_instance = CloudProvider.objects.get(pk=data['cloud_provider_id'])
        proxmox = proxmox_auth(
            host=cloud_provider_instance.api_endpoint,
            password=cloud_provider_instance.password
        )
        vmid = 761
        node = 'pve-01'
        create = proxmox.nodes(node).qemu.create(
            agent="enabled=1",
            bios="seabios",
            cores=1,
            sockets=1,
            autostart=1,
            vmid=vmid,
            memory=2048,
            ostype="l26",
            cdrom="local:iso/ubuntu-16.04.6-server-amd64.iso",
            scsihw="virtio-scsi-pci",
            scsi0=f"kube:vm-{vmid}-disk-0,size=10G",
            net0="model=virtio,bridge=vmbr0,firewall=1"
        )
        allocate_disk_image(
            host=cloud_provider_instance.api_endpoint,
            password=cloud_provider_instance.password,
            node=node,
            storage='kube',
            vmid=vmid,
            size=10
        )
        return JsonResponse(str(create), safe=False)
