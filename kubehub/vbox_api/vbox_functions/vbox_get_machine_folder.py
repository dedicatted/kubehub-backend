from os import mkdir
from pathlib import Path
from os.path import exists


def get_machine_folder():
    machine_folder_name = 'VirtualBox\ VMs/'
    machine_folder_path = Path.home() / machine_folder_name
    if not exists(path=str(machine_folder_path)):
        try:
            mkdir(str(machine_folder_path))
            return machine_folder_path
        except Exception as e:
            return {'errors': {f'{type(e).__name__}': [str(e)]}}
    else:
        return machine_folder_path
