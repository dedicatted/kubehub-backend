from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

from kubehub.vbox_api.vbox_functions.vbox_vm_create import vbox_create_vm
from kubehub.vbox_api.vbox_functions.vbox_vmg_create_data_formation import vmg_create_data_formation


def create_vm_group(data):
    number_of_cores = cpu_count()
    pool = ThreadPool(number_of_cores)
    return pool.map(vbox_create_vm, vmg_create_data_formation(data))
