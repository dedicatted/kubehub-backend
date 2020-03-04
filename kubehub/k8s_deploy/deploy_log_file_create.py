from os import mknod
from time import gmtime, strftime


def create_log_file(log_dir_path):
    filename = "k8s_deploy_log_#.log"
    filename = filename.replace("#", strftime("%Y-%m-%d_%H:%M:%S", gmtime()))
    fullpath = log_dir_path + filename
    mknod(fullpath)
    return fullpath

