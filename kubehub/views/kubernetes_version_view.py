from json import loads
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt

from kubehub.models.kubernetes_version import KubernetesVersion
from kubehub.serializers.kubernetes_version_serializer import KubernetesVersionSerializer


@csrf_exempt
def kubernetes_version_list(request):
    if request.method == 'GET':
        try:
            return JsonResponse({'kubernetes_version_list': list(KubernetesVersion.objects.values())})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@csrf_exempt
def kubernetes_version_add(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            kvs = KubernetesVersionSerializer(data=data)
            if kvs.is_valid():
                kv = kvs.create(kvs.validated_data)
                return JsonResponse(model_to_dict(kv))
            else:
                return JsonResponse({'errors': kvs.errors})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@csrf_exempt
def kubernetes_version_remove(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            pk = data.pop('id')
            instance = KubernetesVersion.objects.get(pk=pk)
            instance.delete()
            return JsonResponse({'deleted': model_to_dict(instance)})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
    return JsonResponse({'operation': 'remove'})

