from django.db import models
from subprocess import check_output


class OsImage(models.Model):
    name_max = int(check_output('getconf NAME_MAX /', shell=True))
    name = models.CharField(max_length=name_max)
    vmid = models.IntegerField(unique=True)
    AGENT_CHOICES = (
        ('enabled=0', 'enabled=0'),
        ('enabled=1', 'enabled=1')
    )
    agent = models.CharField(
        max_length=name_max,
        choices=AGENT_CHOICES,
        default='enabled=1'
    )
    OS_TYPE_CHOICES = (
        ('wxp', 'wxp'),
        ('w2k', 'w2k'),
        ('w2k3', 'w2k3'),
        ('w2k8', 'w2k8'),
        ('wvista', 'wvista'),
        ('win7', 'win7'),
        ('win8', 'win8'),
        ('win10', 'win10'),
        ('l24', 'l24'),
        ('l26', 'l26'),
        ('solaris', 'solaris')
    )
    os_type = models.CharField(
        max_length=name_max,
        choices=OS_TYPE_CHOICES,
        default='l26'
    )
    BIOS_CHOICES = (
        ('seabios', 'seabios'),
        ('ovmf', 'ovmf')
    )
    bios = models.CharField(
        max_length=name_max,
        choices=BIOS_CHOICES,
        default='seabios'
    )
    SCSI_CONTROLLER_MODEL_CHOICES = (
        ('lsi', 'lsi'),
        ('lsi53c810', 'lsi53c810'),
        ('virtio-scsi-pci', 'virtio-scsi-pci'),
        ('virtio-scsi-single', 'virtio-scsi-single'),
        ('megasas', 'megasas'),
        ('pvscsi', 'pvscsi')
    )
    scsi_controller_model = models.CharField(
        max_length=name_max,
        choices=SCSI_CONTROLLER_MODEL_CHOICES,
        default='virtio-scsi-pci'
    )

    storage = models.CharField(max_length=name_max, default='local')
    readonly_fields = ('name', 'vmid', 'os_type', 'bios', 'scsi_controller_model', 'storage')

    def __str__(self):
        return f'id: {self.id}, name: {self.name}, vmid: {self.vmid}, os_type: {self.os_type},' \
               f'bios: {self.bios}, scsi_controller_model: {self.scsi_controller_model},' \
               f'storage: {self.storage}'

