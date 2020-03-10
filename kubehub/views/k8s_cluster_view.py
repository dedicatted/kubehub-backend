from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt

from json import loads
from ..models.k8s_cluster import KubernetesCluster
from ..models.kubespray_deploy import KubesprayDeploy
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
            pk = data.get('k8s_cluster_id')
            instance = KubernetesCluster.objects.get(pk=pk)
            instance.delete()
            return JsonResponse({'deleted': model_to_dict(instance)})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
