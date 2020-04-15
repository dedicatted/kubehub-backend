from json import loads
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models.vm_from_img import VmFromImage
from ..proxmox.get_vm_node import get_vm_node
from ..proxmox.get_file_data import get_file_data
from ..models.cloud_provider import CloudProvider
from ..models.k8s_cluster import KubernetesCluster
from kubehub_backend.settings import K8S_CONFIG_FILE_DIR
from ..k8s_config.k8s_config_file_create import create_config_file
from ..k8s_config.k8s_config_directory_create import create_k8s_config_file_dir


@csrf_exempt
def get_kube_config(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            kubernetes_cluster_instance = KubernetesCluster.objects.get(pk=data['kubernetes_cluster_id'])
            vm_group_instance = VmFromImage.objects.get(
                pk=KubernetesCluster.objects.get(pk=data['kubernetes_cluster_id']).vm_group_id
            )
            create_k8s_config_file_dir()
            cloud_provider_instance = CloudProvider.objects.get(pk=vm_group_instance.cloud_provider.id)
            kube_conf = create_config_file(
                config_dir_path=K8S_CONFIG_FILE_DIR,
                k8s_cluster_id=kubernetes_cluster_instance.id,
                config_data=get_file_data(
                    host=cloud_provider_instance.api_endpoint,
                    password=cloud_provider_instance.password,
                    node=get_vm_node(
                        host=cloud_provider_instance.api_endpoint,
                        password=cloud_provider_instance.password,
                        vmid=vm_group_instance.vmid
                    ),
                    vmid=vm_group_instance.vmid,
                    filename='/root/.kube/config'
                )
            )
            fd_open = open(kube_conf, 'rb')
            response = HttpResponse(content=fd_open)
            response['Content-Disposition'] = f'attachment; filename={kubernetes_cluster_instance.name}_kube_config'
            fd_open.close()
            return response
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})