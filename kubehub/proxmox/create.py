from ..models.cloud_provider import CloudProvider
from ..proxmox.get_less_busy_node import get_less_busy_node
from ..proxmox.get_vm_ip import get_vm_ip
from ..proxmox.get_vm_node import get_vm_node
from ..proxmox.proxmox_auth import proxmox_auth
from django.views.decorators.csrf import csrf_exempt
from json import loads
from django.http import JsonResponse


@csrf_exempt
def create_vm(request):
    if request.method == 'POST':
        data = loads(request.body)
        cloud_provider_instance = CloudProvider.objects.get(pk=data['cloud_provider_id'])
        proxmox = proxmox_auth(
            host=cloud_provider_instance.api_endpoint,
            password=cloud_provider_instance.password
        )
        vm = proxmox.nodes('pve-01')
        vmid = 682
        creat = vm.qemu.create(
            agent="enabled=1",
            vcpus=1,
            autostart=1,
            vmid=vmid,
            memory=2048,
            scsi0=f"kube:vm-{vmid}-disk-0,size=32G"
        )
        created_vm = proxmox.nodes(get_vm_node(
            host=cloud_provider_instance.api_endpoint,
            password=cloud_provider_instance.password,
            vmid=vmid
        )).qemu().vmid676()
        import_disk = created_vm.importdisk().source("/xenial-server-cloudimg-amd64-disk1.img").storage(f"kube:vm-{vmid}-disk-0").format("qcow2")
        return JsonResponse(str(import_disk), safe=False)
