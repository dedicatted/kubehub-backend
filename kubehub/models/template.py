from django.db import models
import subprocess


class Template(models.Model):
    name_max = int(subprocess.check_output("getconf NAME_MAX /", shell=True))
    name = models.CharField(max_length=name_max)
    vmid = models.IntegerField()
    diskread = models.IntegerField()
    template = models.BooleanField()
    status = models.CharField(max_length=name_max)
    disk = models.IntegerField()
    node = models.CharField(max_length=name_max)
    cpu = models.IntegerField()
    diskwrite = models.IntegerField()
    maxcpu = models.IntegerField()
    type = models.CharField(max_length=name_max)
    netin = models.IntegerField()
    maxdisk = models.IntegerField()
    mem = models.IntegerField()
    maxmem = models.IntegerField()
    netout = models.IntegerField()
    uptime = models.IntegerField()

    readonly_fields = ('name', 'vmid', 'diskread', 'template', 'status', 'disk', 'node', 'cpu', 'diskwrite', 'maxcpu',
                       'type', 'netin', 'maxdisk', 'mem', 'maxmem', 'netout', 'uptime')

    def __str__(self):
        return f'template_id: {self.id}, name: {self.name}, vmid: {self.vmid}, diskread: {self.diskread}, ' \
               f'template: {self.template}, status: {self.status}, disk: {self.disk}, node: {self.node}, ' \
               f'cpu: {self.cpu}, diskwrite: {self.diskwrite}, maxcpu: {self.maxcpu}, type: {self.type}, ' \
               f'netin: {self.netin}, maxdisk: {self.maxdisk}, mem: {self.mem}, maxmem: {self.maxmem}, ' \
               f'netout: {self.netout}, uptime: {self.uptime}'
