from django.conf.urls import url
from .views import crud_views
from .views import kubespray_deploy
from .views import vm_group_crud_view
from .proxmox import node_list
from .proxmox import vm_list
from .proxmox import vm_delete
from .proxmox import get_vm_ip
from .proxmox import create_cluster_node
from .proxmox import vm_manager_status
from .proxmox import create_vm_cluster


urlpatterns = [
    url(r'^list$', crud_views.cloud_provider_list, name='cloud_provider_list'),
    url(r'^add$', crud_views.cloud_provider_add, name='cloud_provider_add'),
    url(r'^remove$', crud_views.cloud_provider_remove, name='cloud_provider_remove'),
    url(r'^edit$', crud_views.cloud_provider_edit, name='cloud_provider_edit'),
    url(r'^cluster/create/$', kubespray_deploy.kubespray_deploy, name='cluster_create'),

    url(r'^nodes/list$', node_list.node_list, name='proxmox_nodes_list'),
    url(r'^vm/list$', vm_list.vm_list, name='proxmox_vm_list'),
    url(r'^vm/delete$', vm_delete.vm_delete, name='proxmox_vm_delete'),
    url(r'^vm/get_ip$', get_vm_ip.vm_ip, name='proxmox_get_vm_ip'),

    url(r'^vm/group/list$', vm_group_crud_view.vm_group_list, name='virtual_machines_group_list'),
    url(r'^vm/group/add$', vm_group_crud_view.vm_group_add, name='virtual_machines_group_add'),
    url(r'^vm/group/remove$', vm_group_crud_view.vm_group_remove, name='virtual_machines_group_remove'),
    url(r'^vm/group/edit$', vm_group_crud_view.vm_group_edit, name='virtual_machines_group_edit'),
    url(r'^vm/get/net/manager/status$', vm_manager_status.vm_manager_status , name='proxmox_get_vm_net_manager_status'),

    url(r'^cluster/create/node$', create_cluster_node.create_cluster_node, name='cluster_create_node'),
    url(r'^vm/cluster/create$', create_vm_cluster.create_vm_cluster, name='vm_cluster_create')
]


