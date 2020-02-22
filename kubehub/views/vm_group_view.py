from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

import json

from ..models.vm_group import VMGroup, VM
from ..serializers.vm_group_serializer import VMGroupSerializer
from ..proxmox.create_vm_group import create_vm_group
from ..proxmox.vm_group_delete import vm_group_delete


@csrf_exempt
def vm_group_list(request):
    vm_groups = []
    for vm_group in VMGroup.objects.all():
        vm_list = VM.objects.filter(vm_group=vm_group)
        vmg_dict = model_to_dict(vm_group)
        vmg_dict["vms"] = [model_to_dict(vm) for vm in vm_list]
        vm_groups.append(vmg_dict)
    return JsonResponse({"vm_group_list": vm_groups})


@csrf_exempt
def vm_group_add(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        vmg_list = create_vm_group(data)
        virtual_machine_group = {
            "name": data['name'],
            "user_id": "1",
            "vms": vmg_list
        }
        vmgs = VMGroupSerializer(data=virtual_machine_group)
        if vmgs.is_valid():
            vmgs.save()
            return JsonResponse({"data": vmgs.validated_data})
        else:
            return JsonResponse({'errors': vmgs.errors})


@csrf_exempt
def vm_group_remove(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pk = data.pop('vm_group_id')
            delete = vm_group_delete(data)
            if delete:
                instance = VMGroup.objects.get(pk=pk)
                instance.delete()
                return JsonResponse({'deleted': model_to_dict(instance)})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
    return JsonResponse({'operation': 'remove'})
