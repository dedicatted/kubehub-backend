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


@csrf_exempt
def vbox_vmg_add(request):
    if request.method == 'POST':
        data = loads(request.body)
        path = "/home/klevchenko/.config/VirtualBox/VirtualBox.xml"
        if exists(path=path):
            unlink(path=path)
        vm_name = data.get('name')
        img = "/home/klevchenko/vbox_imgs/'Ubuntu 16.04.6 (64bit).vmdk'"
        vms_dir = "/home/klevchenko/'VirtualBox VMs'"
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
        cmd = f"VBoxManage clonehd {img} {disk_path}"
        system(cmd)
        attach_hdd(
            name=vm_name,
            storagectl='SATA Controller',
            disk_type='hdd',
            medium=disk_path
        )
        set_bootdisk(name=vm_name, boot1='disk', boot2='none', boot3='none', boot4='none')
        set_vrde(name=vm_name, status='on')
        set_vrde_port(name=vm_name, vrdemulticon_status='on', vrdeport=10001)
        # cmd = f'VBoxManage startvm {vm_name} --type headless'
        # system(cmd)
        return JsonResponse("", safe=False)


