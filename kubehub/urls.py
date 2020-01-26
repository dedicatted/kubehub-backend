from django.conf.urls import url
from . views import kubespray_deploy


urlpatterns = [
    url(r'^run/ansible$', kubespray_deploy.kubespray_deploy, name='run_ansible_script'),
]