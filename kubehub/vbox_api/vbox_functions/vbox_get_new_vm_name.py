

def get_new_vm_name(name, number_of_nodes):
    new_name_list = []
    for number in range(1, 100):
        if len(new_name_list) == number_of_nodes:
            break
        else:
            if f'{name}_{number}' not in new_name_list:
                new_name = f'{name}_{number}'
                new_name_list.append(new_name)
    return new_name_list
