from json import loads
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from ..models.template import Template
from ..proxmox.get_template_list import get_template_list
from ..serializers.template_serializer import TemplateSerializer


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_template(request):
    if request.method == 'GET':
        try:
            return JsonResponse({'template_list': list(Template.objects.values())})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def populate_template_list(request):
    global tl
    if request.method == 'POST':
        data = loads(request.body)
        template_list = get_template_list(data)
        db_template_list = [vmid['vmid'] for vmid in list(Template.objects.values('vmid'))]
        for template in template_list:
            if template.get('vmid') in db_template_list:
                template_list.remove(template)
            else:
                tls = TemplateSerializer(data=template)
                if tls.is_valid():
                    tl = tls.create(tls.validated_data)
                else:
                    return JsonResponse({'errors': tls.errors})
    return JsonResponse(model_to_dict(tl))
