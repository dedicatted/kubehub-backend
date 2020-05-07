from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import virtualbox


@csrf_exempt
def vbox_vmg_add(request):
    if request.method == 'POST':
        vbox = virtualbox.VirtualBox()
        vm = vbox.create_machine(name="test", flags='', groups=[], settings_file="", os_type_id='Linux')
        return JsonResponse(str(vm), safe=False)


