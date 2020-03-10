from os import mkdir
from os.path import exists
from kubehub_backend.settings import K8S_DEPLOY_LOG_DIR


def create_deploy_logs_dir():
    path = K8S_DEPLOY_LOG_DIR
    if not exists(path=path):
        try:
            mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            return path
    else:
        return path
