from django.conf.urls import url
from .views import crud_views
from .views import kubespray_deploy
from .proxmox import nodes_list
from .proxmox import vm_list
from .proxmox import vm_delete
from .proxmox import vm_clone


urlpatterns = [
    url(r'^list$', crud_views.cloud_provider_list, name='cloud_provider_list'),
    url(r'^add$', crud_views.cloud_provider_add, name='cloud_provider_add'),
    url(r'^remove$', crud_views.cloud_provider_remove, name='cloud_provider_remove'),
    url(r'^edit$', crud_views.cloud_provider_edit, name='cloud_provider_edit'),
    url(r'^cluster/create/$', kubespray_deploy.kubespray_deploy, name='cluster_create'),
    url(r'^nodes/list$', nodes_list.nodes_list, name='proxmox_nodes_list'),
    url(r'^vm/list$', vm_list.vm_list, name='proxmox_vm_list'),
    url(r'^vm/delete$', vm_delete.vm_delete, name='proxmox_vm_delete'),
    url(r'^vm/clone$', vm_clone.vm_clone, name='proxmox_vm_clone')
]


