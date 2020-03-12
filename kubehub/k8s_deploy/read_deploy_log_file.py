from json import loads
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from kubehub_backend.settings import K8S_DEPLOY_LOG_DIR
from ..models.kubespray_deploy import KubesprayDeploy


@csrf_exempt
def read_deploy_log_file(request):
    data = loads(request.body)
    kubespray_deploy_id = KubesprayDeploy.objects.get(pk=data['kubespray_deploy_id']).id
    filename = f'kubespray_deploy_{kubespray_deploy_id}.log'
    fullpath = f'{K8S_DEPLOY_LOG_DIR}{filename}'
    num_lines = sum(1 for line in open(fullpath))
    log_data = open(fullpath).readlines()
    line_diff = num_lines-int(data['last_line'])
    if line_diff != 0:
        readed_lines = log_data[-line_diff:]
    else:
        return JsonResponse({'readed_lines': "", 'last_line': num_lines}, safe=False)
    return JsonResponse({'readed_lines': readed_lines, 'last_line': num_lines}, safe=False)
