from os import mknod, unlink
from os.path import exists


def create_config_file(config_dir_path, k8s_cluster_id, config_data):
    filename = f"config_{k8s_cluster_id}.log"
    fullpath = config_dir_path + filename
    if exists(fullpath):
        unlink(fullpath)
    else:
        file = open(fullpath, "w")
        file.write(config_data.get('content'))
        file.close()
    return fullpath

