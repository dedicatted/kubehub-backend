from json import loads
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from kubehub.models.vm_type import VmType
from kubehub.serializers.vm_type_serializer import VmTypeSerializer


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vm_type_list(request):
    if request.method == 'GET':
        try:
            return JsonResponse({'vm_type_list': list(VmType.objects.values())})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vm_type_add(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            vmts = VmTypeSerializer(data=data)
            if vmts.is_valid():
                vm_type = vmts.create(vmts.validated_data)
                return JsonResponse(model_to_dict(vm_type))
            else:
                return JsonResponse({'errors': vmts.errors})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vm_type_edit(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            pk = data.get('vm_type_id')
            instance = VmType.objects.get(pk=pk)
            cps = VmTypeSerializer(data=data, partial=True)
            if cps.is_valid():
                cp = cps.update(instance, cps.validated_data)
                return JsonResponse(model_to_dict(cp))
            else:
                return JsonResponse({'errors': cps.errors})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


