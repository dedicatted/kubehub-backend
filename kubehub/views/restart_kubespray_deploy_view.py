from json import loads
from re import findall
from subprocess import Popen
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from ..models.vm_from_img import VmFromImage
from ..models.k8s_cluster import KubernetesCluster
from ..models.kubespray_deploy import KubesprayDeploy
from ..k8s_deploy.ansible_deploy_config import ansible_deploy_config
from ..k8s_deploy.deploy_log_file_create import create_log_file
from ..k8s_deploy.deploy_log_directory_create import create_deploy_logs_dir
from ..serializers.k8s_cluster_serializer import KubernetesClusterSerializer
from ..serializers.kubespray_deploy_serializer import KubesprayDeploySerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def restart_kubespray_deploy(request):
    if request.method == 'POST':
        data = loads(request.body)
        log_dir = create_deploy_logs_dir()
        k8s_cluster_id = KubernetesCluster.objects.get(id=data['k8s_cluster_id']).id
        kubernetes_version = KubernetesCluster.objects.get(id=k8s_cluster_id).kubernetes_version_id.version
        vm_group_id = KubernetesCluster.objects.get(id=data['k8s_cluster_id']).vm_group.id
        vm_group__instance = VmFromImage.objects.filter(vm_group=vm_group_id).values_list('ip', flat=True)
        vms_ip = list(vm_group__instance)
        nomber_of_node = len(vms_ip) + 1
        virtual_machine_ip = (' '.join(vms_ip))
        kubespray_deploy_dir = ansible_deploy_config(
            k8s_cluster_id=k8s_cluster_id,
            vm_ips=virtual_machine_ip,
            kubernetes_version=kubernetes_version
        )
        cmd = (
            f'ANSIBLE_HOST_KEY_CHECKING=False '
            f'ansible-playbook -i '
            f'{kubespray_deploy_dir}/inventory/mycluster/hosts.yml '
            f'--flush-cache '
            f'--user=ubuntu '
            f'--extra-vars "ansible_user=ubuntu ansible_password=ubuntu" '
            f'--become --become-user=root '
            f'{kubespray_deploy_dir}/cluster.yml'
        )
        kubespray_deploy_data = {
            'status': 'deploying',
            'vm_group': vm_group_id,
            'k8s_cluster': k8s_cluster_id
        }
        k8s_cluster_status_update(
            id=k8s_cluster_id,
            status='deploying'
        )
        kds = KubesprayDeploySerializer(data=kubespray_deploy_data)
        if kds.is_valid():
            kd = kds.create(kds.validated_data)
            id = kd.id
            log_fd_create = create_log_file(
                log_dir_path=log_dir,
                kubespray_deploy_id=id
            )
            log_fd_open = open(log_fd_create, 'w')
            deploy = Popen(cmd, shell=True, stdout=log_fd_open).communicate()[0]
            log_fd_open.close()
            log_fd_open_read = open(log_fd_create, 'r')
            contents = log_fd_open_read.read()
            if len(findall("failed=0", contents)) == nomber_of_node and \
                    len(findall("unreachable=0", contents)) == nomber_of_node:
                log_fd_open_read.close()
                kd = status_update(
                    id=id,
                    status='successful'
                )
                k8s_cluster_status_update(
                    id=k8s_cluster_id,
                    status='running'
                )
                return JsonResponse(kd)
            else:
                log_fd_open_read.close()
                kd = status_update(
                    id=id,
                    status='failed'
                )
                k8s_cluster_status_update(
                    id=k8s_cluster_id,
                    status='error'
                )
                return JsonResponse(kd)
        else:
            return JsonResponse({'errors': kds.errors})


def status_update(id, status):
    instance = KubesprayDeploy.objects.get(id=id)
    data = {'status': status}
    kds = KubesprayDeploySerializer(data=data, partial=True)
    if kds.is_valid():
        kd = kds.update(instance, kds.validated_data)
        return model_to_dict(kd)


def k8s_cluster_status_update(id, status):
    instance = KubernetesCluster.objects.get(id=id)
    data = {'status': status}
    k8scs = KubernetesClusterSerializer(data=data, partial=True)
    if k8scs.is_valid():
        k8sc = k8scs.update(instance, k8scs.validated_data)
        return model_to_dict(k8sc)

