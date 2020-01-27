from django.conf.urls import url
from . views import kubespray_deploy


urlpatterns = [
    url(r'^cluster/create/$', kubespray_deploy.kubespray_deploy, name='cluster_create'),
]
