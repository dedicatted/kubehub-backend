from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

import json

from kubehub.models import CloudProvider
from kubehub.serializers import CloudProviderSerializer


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
    return JsonResponse({'operation': 'remove'})


@csrf_exempt
def cloud_provider_edit(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cps = CloudProviderSerializer(data=data)
        # if cps.is_valid():
        #     cp = cps.update(cps.validated_data)
        #     return JsonResponse(model_to_dict(cp))
        # else:
        #     return JsonResponse({'errors': cps.errors})
    return JsonResponse({'operation': 'edit'})
