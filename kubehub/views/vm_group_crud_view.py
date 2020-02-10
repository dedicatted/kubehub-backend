from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

import json

from ..models.vm_group import VMGroup
from ..serializers.vm_group_serializer import VMGroupSerializer
from ..proxmox.create_vm_group import create_vm_group


@csrf_exempt
def vm_group_list(request):
    return JsonResponse({'vm_group_list': list(VMGroup.objects.values())})


@csrf_exempt
def vm_group_add(request):
    global vmg
    if request.method == 'POST':
        data = json.loads(request.body)
        vmg_list = create_vm_group(data)
        for vm_group in vmg_list:
            vmgs = VMGroupSerializer(data=vm_group)
            if vmgs.is_valid():
                vmg = vmgs.create(vmgs.validated_data)
            else:
                return JsonResponse({'errors': vmgs.errors})
    return JsonResponse(model_to_dict(vmg))

