from multiprocessing import Pool

import multiprocessing

from ..proxmox.create_vm import create_vm


def create_vm_group(data):
    number_of_cores = multiprocessing.cpu_count()
    pool = Pool(number_of_cores)
    data = [data] * int(data["number_of_nodes"])
    return pool.map(create_vm, data)

