from django.conf.urls import url
from .views import tamplate_view
from .views import crud_views
from .views import kubespray_deploy
from .views import vm_group_crud_view
from .proxmox import node_list
from .proxmox import vm_delete
from .proxmox import create_vm_group


urlpatterns = [
    url(r'^list$', crud_views.cloud_provider_list, name='cloud_provider_list'),
    url(r'^add$', crud_views.cloud_provider_add, name='cloud_provider_add'),
    url(r'^remove$', crud_views.cloud_provider_remove, name='cloud_provider_remove'),
    url(r'^edit$', crud_views.cloud_provider_edit, name='cloud_provider_edit'),
    url(r'^cluster/create/$', kubespray_deploy.kubespray_deploy, name='cluster_create'),

    url(r'^nodes/list$', node_list.node_list, name='proxmox_nodes_list'),
    url(r'^vm/delete$', vm_delete.vm_delete, name='proxmox_vm_delete'),

    url(r'^vm/group/list$', vm_group_crud_view.vm_group_list, name='virtual_machines_group_list'),
    url(r'^vm/group/add$', vm_group_crud_view.vm_group_add, name='virtual_machines_group_add'),
    url(r'^vm/group/remove$', vm_group_crud_view.vm_group_remove, name='virtual_machines_group_remove'),
    url(r'^vm/group/edit$', vm_group_crud_view.vm_group_edit, name='virtual_machines_group_edit'),

    url(r'^vm/group/create$', create_vm_group.create_vm_group, name='vm_group_create'),

    url(r'^template/list$', tamplate_view.list_template, name='proxmox_template_list'),
    url(r'^template/populate$', tamplate_view.populate_template_list, name='proxmox_template_populate'),
]


