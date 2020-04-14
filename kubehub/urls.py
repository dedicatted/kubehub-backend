from django.conf.urls import url

from .proxmox import proxmox_hard_drive_cleaning
from .views import (
    cloud_provider_view,
    k8s_cluster_view,
    get_deploy_logs,
    restart_kubespray_deploy_view,
    tamplate_view,
    vm_group_view,
    get_kube_config,
    kubernetes_version_view
)


urlpatterns = [
    url(
        r"^list$",
        cloud_provider_view.cloud_provider_list,
        name="cloud_provider_list"
    ),
    url(
        r"^add$",
        cloud_provider_view.cloud_provider_add,
        name="cloud_provider_add"
    ),
    url(
        r"^remove$",
        cloud_provider_view.cloud_provider_remove,
        name="cloud_provider_remove"
    ),
    url(
        r"^edit$",
        cloud_provider_view.cloud_provider_edit,
        name="cloud_provider_edit"
    ),
    url(
        r"^cluster/add$",
        k8s_cluster_view.kubernetes_cluster_add,
        name="cluster_add"
    ),
    url(
        r"^cluster/remove$",
        k8s_cluster_view.kubernetes_cluster_remove,
        name="cluster_remove",
    ),
    url(
        r"^cluster/list$",
        k8s_cluster_view.kubernetes_cluster_list,
        name="cluster_list"
    ),
    url(
        r"^kubespray/deploy/get/log$",
        get_deploy_logs.get_deploy_logs,
        name="kubespray_deploy_get_log",
    ),
    url(
        r"^kubespray/deploy/restart$",
        restart_kubespray_deploy_view.restart_kubespray_deploy,
        name="kubespray_deploy_restart",
    ),
    url(
        r"^vm/group/list$",
        vm_group_view.vm_group_list,
        name="virtual_machines_group_list",
    ),
    url(
        r"^vm/group/status$",
        vm_group_view.get_vm_group_status,
        name="vm_group_status"
    ),
    url(
        r"^vm/group/add$",
        vm_group_view.vm_group_add,
        name="virtual_machines_group_add"
    ),
    url(
        r"^vm/group/remove$",
        vm_group_view.vm_group_remove,
        name="virtual_machines_group_remove",
    ),
    url(
        r"^template/list$",
        tamplate_view.list_template,
        name="proxmox_template_list"),
    url(
        r"^template/populate$",
        tamplate_view.populate_template_list,
        name="proxmox_template_populate",
    ),
    url(
        r"^proxmox/clean$",
        proxmox_hard_drive_cleaning.proxmox_hard_drive_cleaning,
        name="proxmox_hard_drive_cleaning",
    ),
    url(
        r"^cluster/get/config$",
        get_kube_config.get_kube_config,
        name="cluster_get_config",
    ),
    url(
        r"^kubernetes/version/list$",
        kubernetes_version_view.kubernetes_version_list,
        name="kubernetes_version_list"
    ),
    url(
        r"^kubernetes/version/add$",
        kubernetes_version_view.kubernetes_version_add,
        name="kubernetes_version_add"
    ),
    url(
        r"^kubernetes/version/remove$",
        kubernetes_version_view.kubernetes_version_remove,
        name="kubernetes_version_remove"
    ),
]
