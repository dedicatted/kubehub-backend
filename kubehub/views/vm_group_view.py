from json import loads
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from kubehub.models.vm_from_img import VmFromImage
from kubehub.models.vm_from_template import VmFromTemplate
from kubehub.models.proxmox_vm_group import ProxmoxVmGroup
from kubehub.proxmox.vm_group_delete import vm_group_delete
from kubehub.proxmox.vmg_create_from_img import create_vm_group_from_img
from kubehub.proxmox.vmg_create_from_template import create_vm_group_from_template
from kubehub.serializers.vm_from_img_serializer import VmFromImageSerializer
from kubehub.serializers.vm_group_from_img_serializer import VmGroupFromImageSerializer
from kubehub.serializers.vm_from_template_serializer import VmFromTemplateSerializer
from kubehub.serializers.vm_group_from_template_serializer import VmGroupFromTemplateSerializer


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vm_group_list(request):
    if request.method == 'GET':
        try:
            vm_groups = []
            for vm_group in ProxmoxVmGroup.objects.all():
                template_based_vm_list = VmFromTemplate.objects.filter(vm_group=vm_group)
                image_based_vm_list = VmFromImage.objects.filter(vm_group=vm_group)
                vm_list = list(template_based_vm_list) + list(image_based_vm_list)
                vmg_dict = model_to_dict(vm_group)
                vmg_dict['vms'] = [model_to_dict(vm) for vm in vm_list]
                vm_groups.append(vmg_dict)
            return JsonResponse({'vm_group_list': vm_groups})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vm_group_from_template_list(request):
    if request.method == 'GET':
        try:
            vm_groups = []
            for vm_group in ProxmoxVmGroup.objects.all():
                template_based_vm_list = VmFromTemplate.objects.filter(vm_group=vm_group)
                if template_based_vm_list:
                    vmg_dict = model_to_dict(vm_group)
                    vmg_dict['vms'] = [model_to_dict(vm) for vm in template_based_vm_list]
                    vm_groups.append(vmg_dict)
            return JsonResponse({'vm_group_from_template_list': vm_groups})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vm_group_from_image_list(request):
    if request.method == 'GET':
        try:
            vm_groups = []
            for vm_group in ProxmoxVmGroup.objects.all():
                image_based_vm_list = VmFromImage.objects.filter(vm_group=vm_group)
                if image_based_vm_list:
                    vmg_dict = model_to_dict(vm_group)
                    vmg_dict['vms'] = [model_to_dict(vm) for vm in image_based_vm_list]
                    vm_groups.append(vmg_dict)
            return JsonResponse({'vm_group_from_image_list': vm_groups})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_vm_group_status(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            pk = data.get('vm_group_id')
            instance = ProxmoxVmGroup.objects.get(pk=pk)
            return JsonResponse(str(instance.status), safe=False)
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def vm_group_add(request):
    if request.method == 'POST':
        data = loads(request.body)
        if 'template' not in data.get("master"):
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
                'image_vms': masters + workers
            }
            vmgs = VmGroupFromImageSerializer(data=virtual_machine_group)
            if vmgs.is_valid():
                created_group = vmgs.create(vmgs.validated_data)
                pk = created_group.id
                try:
                    vmg_list = create_vm_group_from_img(virtual_machine_group)
                    image_based_vms_update(
                        pk=pk,
                        vms=vmg_list
                    )
                    vmg = image_based_vm_status_update(
                        pk=pk,
                        status='running'
                    )
                    return JsonResponse({'data': vmg})
                except Exception as e:
                    image_based_vm_status_update(
                        pk=pk,
                        status='error'
                    )
                    return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
            else:
                return JsonResponse({'errors': vmgs.errors})
        else:
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
                'template_vms': masters + workers
            }
            vmgs = VmGroupFromTemplateSerializer(data=virtual_machine_group)
            if vmgs.is_valid():
                print('\n\nis_valid')
                created_group = vmgs.create(vmgs.validated_data)
                print('\n\ncreated_group', created_group)
                pk = created_group.id
                try:
                    vmg_list = create_vm_group_from_template(virtual_machine_group)
                    template_based_vms_update(
                        pk=pk,
                        vms=vmg_list
                    )
                    vmg = template_based_vm_status_update(
                        pk=pk,
                        status='running'
                    )
                    return JsonResponse({'data': vmg})
                except Exception as e:
                    template_based_vm_status_update(
                        pk=pk,
                        status='error'
                    )
                    return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
            else:
                return JsonResponse({'errors': vmgs.errors})


def image_based_vms_update(pk, vms):
    vms_instance = VmFromImage.objects.filter(vm_group__id=pk)
    updated_vms = []
    for instance, vm in zip(list(vms_instance), vms):
        vm_serializer = VmFromImageSerializer(data=vm, partial=True)
        if vm_serializer.is_valid():
            vm = vm_serializer.update(instance, vm_serializer.validated_data)
            updated_vms.append(model_to_dict(vm))
        else:
            print(vm_serializer.errors)
    return updated_vms


def template_based_vms_update(pk, vms):
    vms_instance = VmFromTemplate.objects.filter(vm_group__id=pk)
    updated_vms = []
    for instance, vm in zip(list(vms_instance), vms):
        vm_serializer = VmFromTemplateSerializer(data=vm, partial=True)
        if vm_serializer.is_valid():
            vm = vm_serializer.update(instance, vm_serializer.validated_data)
            updated_vms.append(model_to_dict(vm))
        else:
            print(vm_serializer.errors)
    return updated_vms


def image_based_vm_status_update(pk, status):
    instance = ProxmoxVmGroup.objects.get(pk=pk)
    data = {'status': status}
    vmgs = VmGroupFromImageSerializer(data=data, partial=True)
    if vmgs.is_valid():
        vmg = vmgs.update(instance, vmgs.validated_data)
        return model_to_dict(vmg)


def template_based_vm_status_update(pk, status):
    instance = ProxmoxVmGroup.objects.get(pk=pk)
    data = {'status': status}
    vmgs = VmGroupFromTemplateSerializer(data=data, partial=True)
    if vmgs.is_valid():
        vmg = vmgs.update(instance, vmgs.validated_data)
        return model_to_dict(vmg)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def vm_group_remove(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            pk = data.get('vm_group_id')
            try:
                image_based_vm_status_update(pk, 'removing')
                template_based_vm_status_update(pk, 'removing')
                delete = vm_group_delete(data)
                if delete:
                    image_based_vm_status_update(
                        pk=pk,
                        status='removed'
                    )
                    instance = ProxmoxVmGroup.objects.get(pk=pk)
                    instance.delete()
                    return JsonResponse({'deleted': model_to_dict(instance)})
            except Exception as e:
                image_based_vm_status_update(
                    pk=pk,
                    status='error'
                )
                return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
