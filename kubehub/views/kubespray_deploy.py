from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
import subprocess

from ..models.vm_group import VM


@csrf_exempt
def kubespray_deploy(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            vm_group__instance = VM.objects.filter(vm_group=data['vm_group_id']).values_list('ip', flat=True)
            vms_ip = list(vm_group__instance)
            virtual_machine_ip = (" ".join(vms_ip))
            cmd = ["./scripts/cluster_create.sh", virtual_machine_ip]
            output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
        except Exception as e:
            return JsonResponse(e.args, safe=False)
        else:
            return JsonResponse(str(output), safe=False)

