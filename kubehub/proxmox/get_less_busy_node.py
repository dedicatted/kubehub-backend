from ..proxmox.proxmox_auth import proxmox_auth


def get_less_busy_node(host, password):
    proxmox = proxmox_auth(
        host=host,
        password=password
    )
    nodes = proxmox.nodes.get()
    less_busy_node = nodes[0]
    for node in nodes:
        if node["maxmem"]-node["mem"] > less_busy_node["maxmem"]-less_busy_node["mem"]:
            less_busy_node = node
    less_busy_node_name = less_busy_node["node"]
    return less_busy_node_name
