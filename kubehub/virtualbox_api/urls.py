from django.conf.urls import url
from .views import (
    virtualbox_provider_view,
)


urlpatterns = [
    url(
        r"^cloud-provider/list$",
        virtualbox_provider_view.virtualbox_provider_list,
        name="virtualbox_provider_list"
    ),
    url(
        r"^cloud-provider/add$",
        virtualbox_provider_view.virtualbox_provider_add,
        name="virtualbox_provider_add"
    ),
    url(
        r"^cloud-provider/edit$",
        virtualbox_provider_view.virtualbox_provider_edit,
        name="virtualbox_provider_edit"
    ),
    url(
        r"^cloud-provider/remove$",
        virtualbox_provider_view.virtualbox_provider_remove,
        name="virtualbox_provider_remove"
    ),
]
