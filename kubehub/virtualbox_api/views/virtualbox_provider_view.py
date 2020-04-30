from json import loads
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt

from ..models.virtualbox_provider import VirtualBoxCloudProvider
from ..serializers.virtualbox_provider_serializer import VirtualBoxCloudProviderSerializer


@csrf_exempt
def virtualbox_provider_list(request):
    if request.method == 'GET':
        try:
            return JsonResponse({'virtualbox_provider_list': list(VirtualBoxCloudProvider.objects.values())})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@csrf_exempt
def virtualbox_provider_add(request):
    if request.method == 'POST':
        data = loads(request.body)
        cps = VirtualBoxCloudProviderSerializer(data=data)
        if cps.is_valid():
            cp = cps.create(cps.validated_data)
            return JsonResponse(model_to_dict(cp))
        else:
            return JsonResponse({'errors': cps.errors})
    return JsonResponse({'operation': 'add'})


@csrf_exempt
def virtualbox_provider_remove(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            pk = data.pop('id')
            instance = VirtualBoxCloudProvider.objects.get(pk=pk)
            instance.delete()
            return JsonResponse({'deleted': model_to_dict(instance)})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
    return JsonResponse({'operation': 'remove'})


@csrf_exempt
def virtualbox_provider_edit(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            pk = data.pop('id')
            instance = VirtualBoxCloudProvider.objects.get(pk=pk)
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
        cps = VirtualBoxCloudProviderSerializer(data=data, partial=True)
        if cps.is_valid():
            cp = cps.update(instance, cps.validated_data)
            return JsonResponse(model_to_dict(cp))
        else:
            return JsonResponse({'errors': cps.errors})
    return JsonResponse({'operation': 'edit'})
