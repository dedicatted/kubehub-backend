from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt

from json import loads
from ..models.vm_group import VMGroup
from ..models.k8s_cluster import KubernetesCluster
from ..models.kubespray_deploy import KubesprayDeploy
from ..proxmox.vm_group_delete import vm_group_delete
from ..serializers.vm_group_serializer import VMGroupSerializer
from ..serializers.k8s_cluster_serializer import KubernetesClusterSerializer


@csrf_exempt
def kubernetes_cluster_list(request):
    if request.method == 'GET':
        try:
            k8s_clusters = []
            for k8s_cluster in KubernetesCluster.objects.all():
                kubespray_deploy_list = KubesprayDeploy.objects.filter(k8s_cluster=k8s_cluster)
                k8s_cluster_dict = model_to_dict(k8s_cluster)
                k8s_cluster_dict["kubespray_deployments"] = [
                    model_to_dict(kubespray_deploy)
                    for kubespray_deploy in kubespray_deploy_list
                ]
                k8s_clusters.append(k8s_cluster_dict)
            return JsonResponse({'kubernetes_cluster_list': k8s_clusters})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@csrf_exempt
def kubernetes_cluster_add(request):
    if request.method == 'POST':
        try:
            kubernetes_cluster = loads(request.body)
            kcs = KubernetesClusterSerializer(data=kubernetes_cluster)
            kubernetes_cluster["status"] = "ready_to_deploy"
            if kcs.is_valid():
                kcs.create(kcs.validated_data)
                response = dict(kcs.validated_data)
                response['vm_group'] = model_to_dict(response['vm_group'])
                return JsonResponse(response)
            else:
                return JsonResponse({'errors': kcs.errors})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


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
                    status="removing"
                )
                vm_group_status_update(
                    pk=vm_group_pk,
                    status="removing"
                )
                delete = vm_group_delete(data)
                if delete:
                    vm_group_status_update(
                        pk=vm_group_pk,
                        status="removed"
                    )
                    k8s_cluster_status_update(
                        pk=k8s_cluster_pk,
                        status="removed"
                    )
                    k8s_cluster_instance = KubernetesCluster.objects.get(pk=k8s_cluster_pk)
                    k8s_cluster_instance.delete()
                    return JsonResponse({'deleted': model_to_dict(k8s_cluster_instance)})
            except Exception as e:
                k8s_cluster_status_update(
                    pk=k8s_cluster_pk,
                    status="error"
                )
                vm_group_status_update(
                    pk=vm_group_pk,
                    status="error"
                )
                return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


def k8s_cluster_status_update(pk, status):
    instance = KubernetesCluster.objects.get(pk=pk)
    data = {"status": status}
    k8scs = KubernetesClusterSerializer(data=data, partial=True)
    if k8scs.is_valid():
        k8sc = k8scs.update(instance, k8scs.validated_data)
        return model_to_dict(k8sc)


def vm_group_status_update(pk, status):
    instance = VMGroup.objects.get(pk=pk)
    data = {"status": status}
    vmgs = VMGroupSerializer(data=data, partial=True)
    if vmgs.is_valid():
        vmg = vmgs.update(instance, vmgs.validated_data)
        return model_to_dict(vmg)
