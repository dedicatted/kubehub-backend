from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

import json

from ..models.template import Template
from ..serializers.template_serializer import TemplateSerializer
from ..proxmox.template_list import template_list


@csrf_exempt
def list_template(request):
    return JsonResponse({'template_list': list(Template.objects.values())})


@csrf_exempt
def populate_template_list(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        template_list_data = template_list(data)
        tls = TemplateSerializer(data=template_list_data)
        print(tls)
        if tls.is_valid():
            tl = tls.create(tls.validated_data)
            return JsonResponse(model_to_dict(tl))
        else:
            return JsonResponse({'errors': tls.errors})
    return JsonResponse({'operation': 'populate_template_list'})