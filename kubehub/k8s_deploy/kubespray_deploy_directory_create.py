from shutil import rmtree
from os import mkdir, listdir, unlink
from os.path import exists, join, isfile, islink, isdir


def create_k8s_deploy_dir(k8s_cluster_id):
    deploy_dir = f'/tmp/kubespray_deploy_{k8s_cluster_id}'
    if exists(path=deploy_dir):
        for filename in listdir(deploy_dir):
            file_path = join(deploy_dir, filename)
            if isfile(file_path) or islink(file_path):
                unlink(file_path)
            elif isdir(file_path):
                rmtree(file_path)
        return deploy_dir
    mkdir(path=deploy_dir)
    return deploy_dir
