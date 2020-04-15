from multiprocessing.pool import ThreadPool

import multiprocessing

from ..proxmox.vm_create_from_img import create_vm_from_img
from ..proxmox.vmg_create_data_formation import vmg_data_formation


def create_vm_group_from_img(data):
    number_of_cores = multiprocessing.cpu_count()
    pool = ThreadPool(number_of_cores)
    return pool.map(create_vm_from_img, vmg_data_formation(data))
