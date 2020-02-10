from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

import json

from ..models.template import Template
from ..serializers.template_serializer import TemplateSerializer
from ..proxmox.get_template_list import get_template_list


@csrf_exempt
def list_template(request):
    return JsonResponse({'template_list': list(Template.objects.values())})


@csrf_exempt
def populate_template_list(request):
    global tl
    if request.method == 'POST':
        data = json.loads(request.body)
        template_list = get_template_list(data)
        for template in template_list:
            tls = TemplateSerializer(data=template)
            if tls.is_valid():
                tl = tls.create(tls.validated_data)
            else:
                return JsonResponse({'errors': tls.errors})
    return JsonResponse(model_to_dict(tl))

