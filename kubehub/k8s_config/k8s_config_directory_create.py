from os import mkdir
from os.path import exists
from kubehub_backend.settings import K8S_CONFIG_FILE_DIR


def create_k8s_config_file_dir():
    path = K8S_CONFIG_FILE_DIR
    if not exists(path=path):
        try:
            mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            return path
    else:
        return path