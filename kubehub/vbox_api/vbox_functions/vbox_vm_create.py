from kubehub.vbox_api.models.vbox_img import VirtualBoxImage
from kubehub.vbox_api.vbox_functions.vbox_vm_start import start_vm
from kubehub.vbox_api.vbox_functions.vbox_set_vrde import set_vrde
from kubehub.vbox_api.vbox_functions.vbox_attach_hdd import attach_hdd
from kubehub.vbox_api.vbox_functions.vbox_clone_disk import clone_disk
from kubehub.vbox_api.vbox_functions.vbox_config_file import config_file
from kubehub.vbox_api.vbox_functions.vbox_set_bootdisk import set_bootdisk
from kubehub.vbox_api.vbox_functions.vbox_set_ram_size import set_ram_size
from kubehub.vbox_api.vbox_functions.vbox_vm_create_set_up import create_vm
from kubehub.vbox_api.vbox_functions.vbox_set_vrde_port import set_vrde_port
from kubehub.vbox_api.vbox_functions.vbox_add_network_card import add_network_card
from kubehub.vbox_api.vbox_functions.vbox_set_network_card import set_network_card
from kubehub.vbox_api.vbox_functions.vbox_get_machine_folder import get_machine_folder
from kubehub.vbox_api.vbox_functions.vbox_set_number_of_cpus import set_number_of_cpus
from kubehub.vbox_api.vbox_functions.vbox_select_hdd_controller import select_hdd_controller


def vbox_create_vm(data):
    vm_name = data.get('name')
    vbox_img_instance = VirtualBoxImage.objects.get(pk=data['image_id'])
    vms_dir = get_machine_folder()
    image = vbox_img_instance.img_full_path
    config_file(image=image)
    disk_path = f'{vms_dir}/{vm_name}/{vm_name}_disk.vmdk'
    create_vm(
        name=vm_name,
        basefolder=vms_dir,
        os_type='Ubuntu_64'
    )
    add_network_card(name=vm_name, status="on")
    set_ram_size(name=vm_name, ram_size=data.get('memory'))
    set_number_of_cpus(name=vm_name, cpus=data.get('cores'))
    set_network_card(name=vm_name, protocol="bridged")
    select_hdd_controller(
        name=vm_name,
        controller_name='SATA Controller',
        controller='IntelAhci'
    )
    clone_disk(image_path=image, new_disk_path=disk_path)
    attach_hdd(
        name=vm_name,
        storagectl='SATA Controller',
        disk_type='hdd',
        medium=disk_path
    )
    set_bootdisk(name=vm_name, boot1='disk', boot2='none', boot3='none', boot4='none')
    set_vrde(name=vm_name, status='on')
    set_vrde_port(name=vm_name, vrdemulticon_status='on', vrdeport=10001)
    start_vm(vm_name=vm_name, start_mode='headless')
    return {
        'name': data['name'],
        'cores': data['cores'],
        'memory': data['memory']
    }
