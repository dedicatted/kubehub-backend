from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
import json


@csrf_exempt
def kubespray_deploy(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cmd = ["./scripts/cluster_create.sh", data["virtual_machine_ip"]]
            output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
        except Exception as e:
            return JsonResponse(e.args, safe=False)
        else:
            return JsonResponse(str(output), safe=False)
