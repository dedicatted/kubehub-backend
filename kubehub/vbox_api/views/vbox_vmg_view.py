from json import loads
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from kubehub.vbox_api.vbox_functions.vbox_vmg_create_data_formation import vmg_create_data_formation
from kubehub.vbox_api.vbox_functions.vbox_create_vm import vbox_create_vm
from multiprocessing.pool import ThreadPool
import multiprocessing


@csrf_exempt
def vbox_vmg_add(request):
    if request.method == 'POST':
        data = loads(request.body)
        number_of_cores = multiprocessing.cpu_count()
        pool = ThreadPool(number_of_cores)
        pool.map(vbox_create_vm, vmg_create_data_formation(data))
        return JsonResponse("crettt", safe=False)
