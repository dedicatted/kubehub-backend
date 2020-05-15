from kubehub.vbox_api.vbox_functions.vbox_get_new_vm_name import get_new_vm_name


def vmg_create_data_formation(data):
    data_list = []
    for new_name in get_new_vm_name(
            name=data.get('name'),
            number_of_nodes=data.get('number_of_nodes')
    ):
        vm_data = data.copy()
        vm_data["name"] = new_name
        data_list.append(vm_data)
    return data_list
