from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

from kubehub.vbox_api.vbox_functions.vbox_vm_delete import vm_delete
from kubehub.vbox_api.vbox_functions.vbox_vmg_delete_data_formation import vmg_delete_data_formation


def vmg_delete(data):
    number_of_cores = cpu_count()
    pool = ThreadPool(number_of_cores)
    return pool.map(vm_delete, vmg_delete_data_formation(data))
