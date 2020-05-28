from json import loads
from os.path import split
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from kubehub.vbox_api.models.vbox_img import VirtualBoxImage
from kubehub.vbox_api.vbox_functions.vbox_get_images import get_images
from kubehub.vbox_api.models.vbox_cloud_provider import VirtualBoxCloudProvider
from kubehub.vbox_api.serializers.vbox_img_serializer import VirtualBoxImageSerializer


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vbox_img_list(request):
    if request.method == 'GET':
        try:
            return JsonResponse({'vbox_images_list': list(VirtualBoxImage.objects.values())})
        except Exception as e:
            return JsonResponse({'errors': {f'{type(e).__name__}': [str(e)]}})


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vbox_img_add(request):
    if request.method == 'POST':
        data = loads(request.body)
        cloud_provider_instance = VirtualBoxCloudProvider.objects.get(pk=data['cloud_provider_id'])
        vbox_images = get_images(path=cloud_provider_instance.image_folder)
        for img_path in vbox_images:
            path, filename = split(img_path)
            vbox_img_data = {
                'name': filename,
                'img_full_path': f'{path}/\'{filename}\'',
            }
            vbox_imgs = VirtualBoxImageSerializer(data=vbox_img_data)
            if vbox_imgs.is_valid():
                vbox_imgs.create(vbox_imgs.validated_data)
        return JsonResponse(vbox_images, safe=False)
