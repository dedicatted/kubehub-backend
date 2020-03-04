from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
import subprocess

from ..models.vm_group import VM
from ..k8s_deploy.deploy_log_directory_create import create_deploy_logs_dir
from ..k8s_deploy.deploy_log_file_create import create_log_file


@csrf_exempt
def kubespray_deploy(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            log_dir = create_deploy_logs_dir
            vm_group__instance = VM.objects.filter(vm_group=data['vm_group_id']).values_list('ip', flat=True)
            vms_ip = list(vm_group__instance)
            virtual_machine_ip = (" ".join(vms_ip))
            cmd = ["./scripts/cluster_create.sh", virtual_machine_ip]
            log_fd = open(create_log_file(log_dir_path=log_dir), 'w')
            output = subprocess.Popen(cmd, stdout=log_fd).communicate()[0]
            log_fd.close()
        except Exception as e:
            return JsonResponse(e.args, safe=False)
        else:
            return JsonResponse(str(output), safe=False)

