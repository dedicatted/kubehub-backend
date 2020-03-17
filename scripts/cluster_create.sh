#!/bin/bash

rm -rf kubespray

#download kubespray
{
if [ ! -d /kubespray ]; then
    git clone https://github.com/kubernetes-sigs/kubespray.git
fi
}

#check out v2.11.0 release
cd kubespray || exit
git checkout tags/v2.11.0

# Copy ``inventory/sample`` as ``inventory/mycluster``
cp -rfp inventory/sample inventory/mycluster

# Update Ansible inventory file with inventory builder
declare -a IPS=("$@")
echo ${IPS[@]}
CONFIG_FILE=inventory/mycluster/hosts.yml python3 contrib/inventory_builder/inventory.py ${IPS[@]}

# Review and change parameters under ``inventory/mycluster/group_vars``
cat inventory/mycluster/group_vars/all/all.yml
cat inventory/mycluster/group_vars/k8s-cluster/k8s-cluster.yml

# Deploy Kubespray with Ansible Playbook - run the playbook as root
# The option --become is required, as for example writing SSL keys in /etc/,
# installing packages and interacting with various systemd daemons.
# Without --become the playbook will fail to run!
ansible-playbook -i inventory/mycluster/hosts.yml --flush-cache --user=ubuntu --extra-vars "ansible_user=ubuntu ansible_password=ubuntu" --become --become-user=root cluster.yml