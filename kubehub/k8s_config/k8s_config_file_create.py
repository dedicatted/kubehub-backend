from os import unlink
from os.path import exists


def create_config_file(config_dir_path, k8s_cluster_id, config_data):
    filename = f'config_{k8s_cluster_id}.log'
    fullpath = config_dir_path + filename
    if exists(fullpath):
        unlink(fullpath)
        with open(fullpath, 'a') as file:
            file.write(config_data.get('content'))
    else:
        with open(fullpath, 'a') as file:
            file.write(config_data.get('content'))
    return fullpath

