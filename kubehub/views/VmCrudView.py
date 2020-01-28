from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

import json

from ..models.VmGroup import VmGroups
from ..serializers.VmGroupSerializer import VmGroupsSerializer


@csrf_exempt
def vm_groups_list(request):
    if request.method == 'GET':
        return JsonResponse({'vm_groups_list': list(VmGroups.objects.values())})
    if request.method == 'POST':
        return JsonResponse({'vm_groups_list': list(VmGroups.objects.values())})


@csrf_exempt
def vm_group_add(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        vmgs = VmGroupsSerializer(data=data)
        if vmgs.is_valid():
            vmg = vmgs.create(vmgs.validated_data)
            return JsonResponse(model_to_dict(vmg))
        else:
            return JsonResponse({'errors': vmgs.errors})
    return JsonResponse({'operation': 'add_VmGroup'})


@csrf_exempt
def vm_group_remove(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pk = data.pop('id')
            instance = VmGroups.objects.get(pk=pk)
            instance.delete()
            return JsonResponse({'VmGroup_deleted': model_to_dict(instance)})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
    return JsonResponse({'operation': 'remove_VmGroup'})


@csrf_exempt
def vm_group_edit(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pk = data.pop('id')
            instance = VmGroups.objects.get(pk=pk)
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})

        vmgs = VmGroupsSerializer(data=data, partial=True)
        if vmgs.is_valid():
            vmg = vmgs.update(instance, vmgs.validated_data)
            return JsonResponse(model_to_dict(vmg))
        else:
            return JsonResponse({'errors': vmgs.errors})
    return JsonResponse({'operation': 'edit_VmGroup'})
