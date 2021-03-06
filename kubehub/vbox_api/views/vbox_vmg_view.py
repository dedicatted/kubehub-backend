from json import loads
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from kubehub.vbox_api.models.vbox_vm import VirtualBoxVm
from kubehub.vbox_api.models.vbox_vmg import VboxVmGroup
from kubehub.vbox_api.vbox_functions.vbox_vmg_delete import vmg_delete
from kubehub.vbox_api.vbox_functions.vbox_get_pkill import vbox_pkill
from kubehub.vbox_api.vbox_functions.vbox_vmg_create import create_vm_group
from kubehub.vbox_api.serializers.vbox_vm_serializer import VboxVmSerializer
from kubehub.vbox_api.serializers.vbox_vm_group_serializer import VboxVmGroupSerializer


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vbox_vmg_list(request):
    if request.method == 'GET':
        try:
            vbox_pkill()
            vm_groups = []
            for vm_group in VboxVmGroup.objects.all():
                vm_list = VirtualBoxVm.objects.filter(vm_group=vm_group)
                vmg_dict = model_to_dict(vm_group)
                vmg_dict['vms'] = [model_to_dict(vm) for vm in vm_list]
                vm_groups.append(vmg_dict)
            return JsonResponse({'vm_group_list': vm_groups})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vbox_vmg_add(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            master_data = data.get("master")
            master_data.update({
                'name': data.get('name'),
                'vmid': '0',
                'ip': 'creating',
                'node_type': 'master'
            })
            worker_data = data.get("worker")
            worker_data.update({
                'name': data.get('name'),
                'vmid': '0',
                'ip': 'creating',
                'node_type': 'worker'
            })
            masters = [master_data.copy() for _ in range(int(master_data.get("number_of_nodes")))]
            workers = [worker_data.copy() for _ in range(int(worker_data.get("number_of_nodes")))]
            virtual_machine_group = {
                'name': data['name'],
                'user_id': '1',
                'status': 'creating',
                'cloud_provider': data['cloud_provider_id'],
                'vbox_vms': masters + workers
            }
            vmgs = VboxVmGroupSerializer(data=virtual_machine_group)
            if vmgs.is_valid():
                created_group = vmgs.create(vmgs.validated_data)
                pk = created_group.id
                try:
                    vmg_list = create_vm_group(virtual_machine_group)
                    vbox_vms_update(
                        pk=pk,
                        vms=vmg_list
                    )
                    vmg = vbox_vms_status_update(
                        pk=pk,
                        status='running'
                    )
                    return JsonResponse({'data': vmg})
                except Exception as e:
                    vbox_vms_status_update(
                        pk=pk,
                        status='error'
                    )
                    return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
            else:
                return JsonResponse({'errors': vmgs.errors})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
        

def vbox_vms_update(pk, vms):
    vms_instance = VirtualBoxVm.objects.filter(vm_group__id=pk)
    updated_vms = []
    for instance, vm in zip(list(vms_instance), vms):
        vm_serializer = VboxVmSerializer(data=vm, partial=True)
        if vm_serializer.is_valid():
            vm = vm_serializer.update(instance, vm_serializer.validated_data)
            updated_vms.append(model_to_dict(vm))
        else:
            print(vm_serializer.errors)
    return updated_vms


def vbox_vms_status_update(pk, status):
    instance = VboxVmGroup.objects.get(pk=pk)
    data = {'status': status}
    vmgs = VboxVmGroupSerializer(data=data, partial=True)
    if vmgs.is_valid():
        vmg = vmgs.update(instance, vmgs.validated_data)
        return model_to_dict(vmg)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vbox_vmg_remove(request):
    if request.method == 'POST':
        try:
            vbox_pkill()
            data = loads(request.body)
            pk = data.get('vm_group_id')
            try:
                vbox_vms_status_update(pk, 'removing')
                delete = vmg_delete(data)
                if delete:
                    vbox_vms_status_update(
                        pk=pk,
                        status='removed'
                    )
                    instance = VboxVmGroup.objects.get(pk=pk)
                    instance.delete()
                    return JsonResponse({'deleted': model_to_dict(instance)})
            except Exception as e:
                vbox_vms_status_update(
                    pk=pk,
                    status='error'
                )
                return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
