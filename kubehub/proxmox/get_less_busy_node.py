from proxmoxer import ProxmoxAPI


def get_less_busy_node(host, password):
    proxmox = ProxmoxAPI(host=host, user='root@pam', password=password, verify_ssl=False)
    nodes = proxmox.nodes.get()
    less_busy_node = nodes[0]
    for node in nodes:
        if node["maxmem"]-node["mem"] > less_busy_node["maxmem"]-less_busy_node["mem"]:
            less_busy_node = node
    less_busy_node_name = less_busy_node["node"]
    return less_busy_node_name






