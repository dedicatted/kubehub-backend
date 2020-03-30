from re import sub


def choose_kubernetes_version(file_path, kubernetes_version):
    old_kubernetes_version = r"kube_version: v\d\.\d{1,3}\.\d{1,3}"
    with open(file_path, 'r+') as file:
        replace_version = file.read()
        replace_version = sub(pattern=old_kubernetes_version, repl=f'kube_version: {kubernetes_version}', string=replace_version)
        file.seek(0)
        file.write(replace_version)
        file.truncate()
    return file_path
