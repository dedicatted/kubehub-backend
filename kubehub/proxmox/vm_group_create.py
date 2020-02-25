from multiprocessing.pool import ThreadPool

import multiprocessing

from ..proxmox.vm_create import create_vm
from ..proxmox.vmg_create_data_formation import vmg_data_formation


def create_vm_group(data):
    number_of_cores = multiprocessing.cpu_count()
    pool = ThreadPool(number_of_cores)
    return pool.map(create_vm, vmg_data_formation(data))
