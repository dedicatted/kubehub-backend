from os import mkdir
from os.path import exists


def create_deploy_logs_dir():
    path = "/tmp/k8s-deploy-logs/"
    if not exists(path=path):
        try:
            mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            return path
    else:
        return path
