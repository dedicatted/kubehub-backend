from git import Repo
from subprocess import run, Popen, PIPE

from ..k8s_deploy.kubespray_deploy_directory_create import create_k8s_deploy_dir


def ansible_deploy_config(k8s_cluster_id, vm_ips):
    kubespray_deploy_dir = create_k8s_deploy_dir(k8s_cluster_id=k8s_cluster_id)
    kubespray = Repo.clone_from("https://github.com/kubernetes-sigs/kubespray.git", kubespray_deploy_dir)
    kubespray.git.checkout('tags/v2.11.0')
    cmd = f'cp -rfp {kubespray_deploy_dir}/inventory/sample/ {kubespray_deploy_dir}/inventory/mycluster/'
    Popen(cmd.split(), stdout=PIPE)
    cmd = (
        f"CONFIG_FILE={kubespray_deploy_dir}/inventory/mycluster/hosts.yml "
        f"python3 {kubespray_deploy_dir}/contrib/inventory_builder/inventory.py {vm_ips}"
    )
    run(cmd, shell=True)
    return kubespray_deploy_dir
