from django.conf.urls import url
from .views import (
    vbox_coud_provider_view,
    vbox_img_view,
    vbox_vmg_view
)


urlpatterns = [
    url(
        r"^cloud-provider/list$",
        vbox_coud_provider_view.virtualbox_provider_list,
        name="virtualbox_provider_list"
    ),
    url(
        r"^cloud-provider/add$",
        vbox_coud_provider_view.virtualbox_provider_add,
        name="virtualbox_provider_add"
    ),
    url(
        r"^cloud-provider/edit$",
        vbox_coud_provider_view.virtualbox_provider_edit,
        name="virtualbox_provider_edit"
    ),
    url(
        r"^cloud-provider/remove$",
        vbox_coud_provider_view.virtualbox_provider_remove,
        name="virtualbox_provider_remove"
    ),
    url(
        r"^vbox_img/list$",
        vbox_img_view.vbox_img_list,
        name="vbox_img_list"
    ),
    url(
        r"^vbox_img/add$",
        vbox_img_view.vbox_img_add,
        name="vbox_img_add"
    ),
    url(
        r"^vmg/list$",
        vbox_vmg_view.vbox_vmg_list,
        name="vbox_vmg_list"
    ),
    url(
        r"^vmg/add$",
        vbox_vmg_view.vbox_vmg_add,
        name="vbox_vmg_add"
    ),
]
