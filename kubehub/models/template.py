from django.db import models
import subprocess


class Template(models.Model):
    name_max = int(subprocess.check_output("getconf NAME_MAX /", shell=True))
    name = models.CharField(max_length=name_max)
    vmid = models.IntegerField(max_length=name_max)
    diskread = models.IntegerField(max_length=name_max)
    template = models.BooleanField(max_length=name_max)
    status = models.CharField(max_length=name_max)
    disk = models.IntegerField(max_length=name_max)
    node = models.CharField(max_length=name_max)
    cpu = models.IntegerField(max_length=name_max)
    diskwrite = models.IntegerField(max_length=name_max)
    maxcpu = models.IntegerField(max_length=name_max)
    type = models.CharField(max_length=name_max)
    netin = models.IntegerField(max_length=name_max)
    maxdisk = models.IntegerField(max_length=name_max)
    mem = models.IntegerField(max_length=name_max)
    maxmem = models.IntegerField(max_length=name_max)
    netout = models.IntegerField(max_length=name_max)
    uptime = models.IntegerField(max_length=name_max)

    readonly_fields = ('name', 'vmid', 'diskread', 'template', 'status', 'disk', 'node', 'cpu', 'diskwrite', 'maxcpu',
                       'type', 'netin', 'maxdisk', 'mem', 'maxmem', 'netout', 'uptime')

    def __str__(self):
        return f'id: {self.id}, name: {self.name}, vmid: {self.vmid}, diskread: {self.diskread}, ' \
               f'template: {self.template}, status: {self.status}, disk: {self.disk}, node: {self.node}, ' \
               f'cpu: {self.cpu}, diskwrite: {self.diskwrite}, maxcpu: {self.maxcpu}, type: {self.type}, ' \
               f'netin: {self.netin}, maxdisk: {self.maxdisk}, mem: {self.mem}, maxmem: {self.maxmem}, ' \
               f'netout: {self.netout}, uptime: {self.uptime}'
