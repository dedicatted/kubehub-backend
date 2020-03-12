from django.conf.urls import url

from .views import crud_views, k8s_cluster_view, tamplate_view, vm_group_view, restart_kubespray_deploy_view
from .k8s_deploy import read_deploy_log_file
from .proxmox import proxmox_hard_drive_cleaning

urlpatterns = [
    url(r'^list$', crud_views.cloud_provider_list, name='cloud_provider_list'),
    url(r'^add$', crud_views.cloud_provider_add, name='cloud_provider_add'),
    url(r'^remove$', crud_views.cloud_provider_remove, name='cloud_provider_remove'),
    url(r'^edit$', crud_views.cloud_provider_edit, name='cloud_provider_edit'),
    url(r'^cluster/add$', k8s_cluster_view.kubernetes_cluster_add, name='cluster_add'),
    url(r'^cluster/remove$', k8s_cluster_view.kubernetes_cluster_remove, name='cluster_remove'),
    url(r'^cluster/list$', k8s_cluster_view.kubernetes_cluster_list, name='cluster_list'),

    url(r'^kubespray/deploy/read/log$', read_deploy_log_file.read_deploy_log_file, name='kubespray_deploy_read_log'),

    url(r'^kubespray/deploy/restart$', restart_kubespray_deploy_view.restart_kubespray_deploy,name='kubespray_deploy_restart'),
    url(r'^vm/group/list$', vm_group_view.vm_group_list, name='virtual_machines_group_list'),
    url(r'^vm/group/status$', vm_group_view.get_vm_group_status, name='vm_group_status'),
    url(r'^vm/group/add$', vm_group_view.vm_group_add, name='virtual_machines_group_add'),
    url(r'^vm/group/remove$', vm_group_view.vm_group_remove, name='virtual_machines_group_remove'),
    url(r'^template/list$', tamplate_view.list_template, name='proxmox_template_list'),
    url(r'^template/populate$', tamplate_view.populate_template_list, name='proxmox_template_populate'),
    url(r'^proxmox/clean$', proxmox_hard_drive_cleaning.proxmox_hard_drive_cleaning, name='proxmox_hard_drive_cleaning')
]
