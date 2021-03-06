from json import loads
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from kubehub_backend.settings import K8S_DEPLOY_LOG_DIR
from ..models.kubespray_deploy import KubesprayDeploy


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_deploy_logs(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            kubespray_deploy_id = KubesprayDeploy.objects.get(pk=data['kubespray_deploy_id']).id
            filename = f'kubespray_deploy_{kubespray_deploy_id}.log'
            fullpath = f'{K8S_DEPLOY_LOG_DIR}{filename}'
            log_data = open(fullpath).readlines()
            num_lines = len(log_data)
            line_diff = num_lines - int(data['last_line'])
            if line_diff != 0:
                readed_lines = log_data[-line_diff:]
            else:
                return JsonResponse({'readed_lines': "", 'last_line': num_lines}, safe=False)
            return JsonResponse({'readed_lines': readed_lines, 'last_line': num_lines}, safe=False)
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})
