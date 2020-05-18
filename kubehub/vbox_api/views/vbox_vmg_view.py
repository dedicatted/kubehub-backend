from json import loads
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt

from kubehub.vbox_api.models.vbox_vm import VirtualBoxVm
from kubehub.vbox_api.models.vbox_vmg import VboxVmGroup
from kubehub.vbox_api.vbox_functions.vbox_vmg_create import create_vm_group
from kubehub.vbox_api.serializers.vbox_vm_serializer import VboxVmSerializer
from kubehub.vbox_api.serializers.vbox_vm_group_serializer import VboxVmGroupSerializer


@csrf_exempt
def vbox_vmg_add(request):
    if request.method == 'POST':
        data = loads(request.body)
        virtual_machine_group = {
            'name': data['name'],
            'user_id': '1',
            'status': 'creating',
            'cloud_provider': data['cloud_provider_id'],
            'vbox_vms': [{
                'name': data['name'],
                'ip': 'creating',
                'cores': data['cores'],
                'memory': data['memory'],
                'vbox_os_image': data['image_id']
            } for _ in range(int(data['number_of_nodes']))]
        }
        vmgs = VboxVmGroupSerializer(data=virtual_machine_group)
        if vmgs.is_valid():
            created_group = vmgs.create(vmgs.validated_data)
            pk = created_group.id
            try:
                vmg_list = create_vm_group(data)
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
