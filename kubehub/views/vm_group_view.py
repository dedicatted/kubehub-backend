from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

from ..models.vm_group import VM, VMGroup
from ..proxmox.vm_group_create import create_vm_group
from ..proxmox.vm_group_delete import vm_group_delete
from ..serializers.vm_group_serializer import VMGroupSerializer, VMSerializer


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
def get_vm_group_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pk = data.get('vm_group_id')
            instance = VMGroup.objects.get(pk=pk)
            return JsonResponse(str(instance.status), safe=False)
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@csrf_exempt
def vm_group_add(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        virtual_machine_group = {
            "name": data['name'],
            "user_id": "1",
            "status": "creating",
            "vms": [{
                "name": "creating",
                "vmid": "0",
                "ip": "creating",
                "template_id": "0",
                "cloud_provider": data['cloud_provider_id']
            } for _ in range(int(data["number_of_nodes"]))]
        }
        print(virtual_machine_group)
        vmgs = VMGroupSerializer(data=virtual_machine_group)
        if vmgs.is_valid():
            created_group = vmgs.create(vmgs.validated_data)
            pk = created_group.id
            try:
                vmg_list = create_vm_group(data)
                vms_update(
                    pk=pk,
                    vms=vmg_list
                )
                vmg = status_update(
                    pk=pk,
                    status="running"
                )
                return JsonResponse({"data": vmg})
            except Exception as e:
                status_update(
                    pk=pk,
                    status="error"
                )
                return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
        else:
            return JsonResponse({'errors': vmgs.errors})


def vms_update(pk, vms):
    vms_instance = VM.objects.filter(vm_group__id=pk)
    updated_vms = []
    for instance, vm in zip(list(vms_instance), vms):
        vm_serializer = VMSerializer(data=vm, partial=True)
        if vm_serializer.is_valid():
            vm = vm_serializer.update(instance, vm_serializer.validated_data)
            updated_vms.append(model_to_dict(vm))
        else:
            print(vm_serializer.errors)
    return updated_vms


def status_update(pk, status):
    instance = VMGroup.objects.get(pk=pk)
    data = {"status": status}
    vmgs = VMGroupSerializer(data=data, partial=True)
    if vmgs.is_valid():
        vmg = vmgs.update(instance, vmgs.validated_data)
        return model_to_dict(vmg)


@csrf_exempt
def vm_group_remove(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        pk = data.get('vm_group_id')
        try:
            status_update(pk, "removing")
            delete = vm_group_delete(data)
            if delete:
                status_update(
                    pk=pk,
                    status="removed"
                )
                instance = VMGroup.objects.get(pk=pk)
                instance.delete()
                return JsonResponse({'deleted': model_to_dict(instance)})
        except Exception as e:
            status_update(
                pk=pk,
                status="error"
            )
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
    return JsonResponse({'operation': 'remove'})
