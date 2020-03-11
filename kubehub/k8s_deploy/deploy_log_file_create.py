from os import mknod, unlink
from os.path import exists


def create_log_file(log_dir_path, kubespray_deploy_id):
    filename = "kubespray_deploy_#.log"
    filename = filename.replace("#", f"{kubespray_deploy_id}")
    fullpath = log_dir_path + filename
    if exists(fullpath):
        unlink(fullpath)
    mknod(fullpath)
    return fullpath

