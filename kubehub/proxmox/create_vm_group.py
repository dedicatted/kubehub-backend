from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from multiprocessing import Pool

import multiprocessing
import json

from ..proxmox.create_vm import create_vm


@csrf_exempt
def create_vm_group(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            number_of_cores = multiprocessing.cpu_count()
            pool = Pool(number_of_cores)
            data = [data]*int(data["number_of_nodes"])
            return JsonResponse(str(pool.map(create_vm, data)), safe=False)
        except Exception as e:
            return JsonResponse(e.args, safe=False)

