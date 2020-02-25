from proxmoxer import ProxmoxAPI


def proxmox_auth(host, password):
    proxmox = ProxmoxAPI(
        host=host,
        user='root@pam',
        password=password,
        verify_ssl=False
    )
    return proxmox