from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt

import json
import subprocess

from ..models.vm_group import VM
from ..models.k8s_cluster import KubernetesCluster
from ..serializers.k8s_cluster_serializer import KubernetesClusterSerializer


@csrf_exempt
def kubernetes_cluster_list(request):
    return JsonResponse({'kubernetes_cluster_list': list(KubernetesCluster.objects.values())})


def kubespray_deploy(vm_group):
    vm_group__instance = VM.objects.filter(vm_group=vm_group).values_list('ip', flat=True)
    vms_ip = list(vm_group__instance)
    virtual_machine_ip = (" ".join(vms_ip))
    cmd = ["./scripts/cluster_create.sh", virtual_machine_ip]
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
    return output


@csrf_exempt
def kubernetes_cluster_add(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        kubernetes_cluster = {
            'name': data['name'],
            'k8s_version': data['k8s_version'],
            'vm_group': data['vm_group_id']
        }
        kubespray = kubespray_deploy(vm_group=data['vm_group_id'])
        kcs = KubernetesClusterSerializer(data=kubernetes_cluster)
        if kcs.is_valid():
            kcs.create(kcs.validated_data)
            response = dict(kcs.validated_data)
            response['vm_group'] = model_to_dict(response['vm_group'])
            return JsonResponse(response)
        else:
            return JsonResponse({'errors': kcs.errors})