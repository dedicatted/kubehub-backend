from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

import json

from kubehub.models.CloudProvider import CloudProvider
from kubehub.serializers.CloudProviderSerializer import CloudProviderSerializer


@csrf_exempt
def cloud_provider_list(request):
    return JsonResponse({'cloud_provider_list': list(CloudProvider.objects.values())})


@csrf_exempt
def cloud_provider_add(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cps = CloudProviderSerializer(data=data)
        if cps.is_valid():
            cp = cps.create(cps.validated_data)
            return JsonResponse(model_to_dict(cp))
        else:
            return JsonResponse({'errors': cps.errors})
    return JsonResponse({'operation': 'add'})


@csrf_exempt
def cloud_provider_remove(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pk = data.pop('id')
            instance = CloudProvider.objects.get(pk=pk)
            instance.delete()
            return JsonResponse({'deleted': model_to_dict(instance)})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
    return JsonResponse({'operation': 'remove'})


@csrf_exempt
def cloud_provider_edit(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pk = data.pop('id')
            instance = CloudProvider.objects.get(pk=pk)
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})

        cps = CloudProviderSerializer(data=data, partial=True)
        if cps.is_valid():
            cp = cps.update(instance, cps.validated_data)
            return JsonResponse(model_to_dict(cp))
        else:
            return JsonResponse({'errors': cps.errors})
    return JsonResponse({'operation': 'edit'})
