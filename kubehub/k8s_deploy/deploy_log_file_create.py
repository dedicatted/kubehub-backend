from os import mknod
from time import gmtime, strftime
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import sys

from ..k8s_deploy.deploy_log_directory_create import create_deploy_logs_dir


@csrf_exempt
def create_log_file(request):
    log_dir_path = create_deploy_logs_dir()
    filename = "k8s_deploy_log_#.log"
    filename = filename.replace("#", strftime("%Y-%m-%d_%H:%M:%S", gmtime()))
    fullpath = log_dir_path + filename
    mknod(fullpath)


    # cmd = ["./scripts/script.sh"]
    # output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]

    f = open(fullpath, 'w')
    sys.stdout = f
    print("text")
    f.close()
    return JsonResponse(str(fullpath), safe=False)

