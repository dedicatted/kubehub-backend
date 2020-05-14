from json import loads
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from os import system, unlink
from os.path import exists

from kubehub.vbox_api.vbox_functions.vbox_set_vrde import set_vrde
from kubehub.vbox_api.vbox_functions.vbox_attach_hdd import attach_hdd
from kubehub.vbox_api.vbox_functions.vbox_set_bootdisk import set_bootdisk
from kubehub.vbox_api.vbox_functions.vbox_set_ram_size import set_ram_size
from kubehub.vbox_api.vbox_functions.vbox_vm_create_set_up import create_vm
from kubehub.vbox_api.vbox_functions.vbox_set_vrde_port import set_vrde_port
from kubehub.vbox_api.vbox_functions.vbox_add_network_card import add_network_card
from kubehub.vbox_api.vbox_functions.vbox_set_network_card import set_network_card
from kubehub.vbox_api.vbox_functions.vbox_select_hdd_controller import select_hdd_controller

from kubehub.vbox_api.vbox_functions.vbox_get_machine_folder import get_machine_folder
from kubehub.vbox_api.models.vbox_img import VirtualBoxImage
from kubehub.vbox_api.vbox_functions.vbox_clone_disk import clone_disk
from kubehub.vbox_api.vbox_functions.vbox_start_vm import start_vm


@csrf_exempt
def vbox_vmg_add(request):
    if request.method == 'POST':
        data = loads(request.body)
        path = "~/.config/VirtualBox/VirtualBox.xml"
        if exists(path=path):
            unlink(path=path)
        vm_name = data.get('name')
        vbox_img_instance = VirtualBoxImage.objects.get(pk=data['image_id'])

        img = vbox_img_instance.img_full_path
        vms_dir = get_machine_folder(cloud_provider_id=data['cloud_provider_id'])
        disk_path = f'{vms_dir}/{vm_name}/{vm_name}_disk.vmdk'
        create_vm(
            name=vm_name,
            basefolder=vms_dir,
            os_type='Ubuntu_64'
        )
        add_network_card(name=vm_name, status="on")
        set_ram_size(name=vm_name, ram_size=data.get('memory'))
        set_network_card(name=vm_name, protocol="nat")
        select_hdd_controller(
            name=vm_name,
            controller_name='SATA Controller',
            controller='IntelAhci'
        )
        clone_disk(image_path=img, new_disk_path=disk_path)
        attach_hdd(
            name=vm_name,
            storagectl='SATA Controller',
            disk_type='hdd',
            medium=disk_path
        )
        set_bootdisk(name=vm_name, boot1='disk', boot2='none', boot3='none', boot4='none')
        set_vrde(name=vm_name, status='on')
        set_vrde_port(name=vm_name, vrdemulticon_status='on', vrdeport=10001)
        # start_vm(vm_name=vm_name, start_mode='headless')
        return JsonResponse("", safe=False)


