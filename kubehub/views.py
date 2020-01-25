from django.http import JsonResponse
import subprocess
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def run_ansible_script(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data['host'])
            cmd = ["./kubespray_deploy/kubespray_deploy_script.sh", data["host"]]
            output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
        except Exception as e:
            return JsonResponse(e.args, safe=False)
        else:
            return JsonResponse(str(output), safe=False)
            # return JsonResponse('bla bla bla', safe=False)
