from json import loads
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models.k8s_cluster import KubernetesCluster


@csrf_exempt
def get_kube_config(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            kubernetes_cluster_name = KubernetesCluster.objects.get(pk=data['kubernetes_cluster_id']).name
            fd_open = open('/tmp/test/test.txt', 'rb')
            response = HttpResponse(content=fd_open)
            response['Content-Disposition'] = f'attachment; filename={kubernetes_cluster_name}_kube_config'
            fd_open.close()
            return response
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
