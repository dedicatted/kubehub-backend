from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from json import loads
from ..models.proxmox_vm_group import ProxmoxVmGroup
from ..models.k8s_cluster import KubernetesCluster
from ..models.kubespray_deploy import KubesprayDeploy
from ..proxmox.vm_group_delete import vm_group_delete
from ..k8s_deploy.kubespray_deploy import kubespray_deploy
from ..serializers.vm_group_from_img_serializer import VmGroupFromImageSerializer
from ..serializers.k8s_cluster_serializer import KubernetesClusterSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def kubernetes_cluster_list(request):
    if request.method == 'GET':
        try:
            k8s_clusters = []
            for k8s_cluster in KubernetesCluster.objects.all():
                kubespray_deploy_list = KubesprayDeploy.objects.filter(k8s_cluster=k8s_cluster)
                k8s_cluster_dict = model_to_dict(k8s_cluster)
                k8s_cluster_dict['kubespray_deployments'] = [
                    model_to_dict(kubespray_deploy_attempt)
                    for kubespray_deploy_attempt in kubespray_deploy_list
                ]
                k8s_clusters.append(k8s_cluster_dict)
            return JsonResponse({'kubernetes_cluster_list': k8s_clusters})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def kubernetes_cluster_add(request):
    if request.method == 'POST':
        try:
            kubernetes_cluster = loads(request.body)
            kcs = KubernetesClusterSerializer(data=kubernetes_cluster)
            kubernetes_cluster['status'] = 'deploying'
            if kcs.is_valid():
                kc = kcs.create(kcs.validated_data)
                deploy = kubespray_deploy(
                    k8s_cluster_id=kc.id
                )
                if deploy.get('status') == 'successful':
                    k8s_cluster_status_update(
                        pk=kc.id,
                        status='running'
                    )
                else:
                    k8s_cluster_status_update(
                        pk=kc.id,
                        status='error'
                    )
                return JsonResponse(model_to_dict(kc))
            else:
                return JsonResponse({'errors': kcs.errors})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def kubernetes_cluster_remove(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            data['vm_group_id'] = KubernetesCluster.objects.get(pk=data['k8s_cluster_id']).vm_group.id
            vm_group_pk = data.get('vm_group_id')
            k8s_cluster_pk = data.get('k8s_cluster_id')
            try:
                k8s_cluster_status_update(
                    pk=k8s_cluster_pk,
                    status='removing'
                )
                vm_group_status_update(
                    pk=vm_group_pk,
                    status='removing'
                )
                delete = vm_group_delete(data)
                if delete:
                    vm_group_status_update(
                        pk=vm_group_pk,
                        status='removed'
                    )
                    k8s_cluster_status_update(
                        pk=k8s_cluster_pk,
                        status='removed'
                    )
                    k8s_cluster_instance = KubernetesCluster.objects.get(pk=k8s_cluster_pk)
                    k8s_cluster_instance.delete()
                    vm_group_instance = ProxmoxVmGroup.objects.get(pk=vm_group_pk)
                    vm_group_instance.delete()
                    return JsonResponse({'deleted': model_to_dict(k8s_cluster_instance)})
            except Exception as e:
                k8s_cluster_status_update(
                    pk=k8s_cluster_pk,
                    status='error'
                )
                vm_group_status_update(
                    pk=vm_group_pk,
                    status='error'
                )
                return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


def k8s_cluster_status_update(pk, status):
    instance = KubernetesCluster.objects.get(pk=pk)
    data = {'status': status}
    k8scs = KubernetesClusterSerializer(data=data, partial=True)
    if k8scs.is_valid():
        k8sc = k8scs.update(instance, k8scs.validated_data)
        return model_to_dict(k8sc)


def vm_group_status_update(pk, status):
    instance = ProxmoxVmGroup.objects.get(pk=pk)
    data = {'status': status}
    vmgs = VmGroupFromImageSerializer(data=data, partial=True)
    if vmgs.is_valid():
        vmg = vmgs.update(instance, vmgs.validated_data)
        return model_to_dict(vmg)
