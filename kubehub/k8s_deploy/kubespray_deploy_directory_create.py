from os import mkdir
from shutil import rmtree
from os.path import exists


def create_k8s_deploy_dir(k8s_cluster_id):
    deploy_dir = f'/tmp/kubespray_deploy_{k8s_cluster_id}'
    if exists(path=deploy_dir):
        rmtree(f'/tmp/kubespray_deploy_{k8s_cluster_id}/')
    mkdir(path=deploy_dir)
    return deploy_dir
