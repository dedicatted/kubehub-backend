from os import mknod, unlink
from os.path import exists


def create_log_file(log_dir_path, k8s_cluster_id, vm_group_id):
    filename = "kubespray_deploy_#.log"
    filename = filename.replace("#", f"k8s_cluster_id_{k8s_cluster_id}_vm_group_id_{vm_group_id}")
    fullpath = log_dir_path + filename
    if exists(fullpath):
        unlink(fullpath)
    mknod(fullpath)
    return fullpath

