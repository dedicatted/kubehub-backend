from django.conf.urls import url
from .views import crud_views
from .views import kubespray_deploy
from .views import VmCrudView


urlpatterns = [
    url(r'^list$', crud_views.cloud_provider_list, name='cloud_provider_list'),
    url(r'^add$', crud_views.cloud_provider_add, name='cloud_provider_add'),
    url(r'^remove$', crud_views.cloud_provider_remove, name='cloud_provider_remove'),
    url(r'^edit$', crud_views.cloud_provider_edit, name='cloud_provider_edit'),
    url(r'^cluster/create/$', kubespray_deploy.kubespray_deploy, name='cluster_create'),
    url(r'^VM/group/list$', VmCrudView.vm_groups_list, name='virtual_machines_group_list'),
    url(r'^VM/group/add$', VmCrudView.vm_group_add, name='virtual_machines_group_add'),
    url(r'^VM/group/remove$', VmCrudView.vm_group_remove, name='virtual_machines_group_remove'),
    url(r'^VM/group/edit$', VmCrudView.vm_group_edit, name='virtual_machines_group_edit'),
]


