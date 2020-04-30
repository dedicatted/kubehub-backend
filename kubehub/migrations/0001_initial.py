# Generated by Django 3.0.3 on 2020-04-30 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, null=True, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=30, null=True, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='data joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('first_name', models.CharField(blank=True, max_length=20)),
                ('last_name', models.CharField(blank=True, max_length=20, null=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KubernetesCluster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('status', models.CharField(choices=[('deploying', 'deploying'), ('running', 'running'), ('removing', 'removing'), ('removed', 'removed'), ('error', 'error')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='KubernetesVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(choices=[('v1.14.9', 'v1.14.9'), ('v1.15.3', 'v1.15.3'), ('v1.15.8', 'v1.15.8'), ('v1.15.11', 'v1.15.11'), ('v1.16.8', 'v1.16.8')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OsImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('vmid', models.IntegerField(unique=True)),
                ('agent', models.CharField(choices=[('enabled=0', 'enabled=0'), ('enabled=1', 'enabled=1')], default='enabled=1', max_length=255)),
                ('os_type', models.CharField(choices=[('wxp', 'wxp'), ('w2k', 'w2k'), ('w2k3', 'w2k3'), ('w2k8', 'w2k8'), ('wvista', 'wvista'), ('win7', 'win7'), ('win8', 'win8'), ('win10', 'win10'), ('l24', 'l24'), ('l26', 'l26'), ('solaris', 'solaris')], default='l26', max_length=255)),
                ('bios', models.CharField(choices=[('seabios', 'seabios'), ('ovmf', 'ovmf')], default='seabios', max_length=255)),
                ('scsi_controller_model', models.CharField(choices=[('lsi', 'lsi'), ('lsi53c810', 'lsi53c810'), ('virtio-scsi-pci', 'virtio-scsi-pci'), ('virtio-scsi-single', 'virtio-scsi-single'), ('megasas', 'megasas'), ('pvscsi', 'pvscsi')], default='virtio-scsi-pci', max_length=255)),
                ('storage', models.CharField(default='local', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ProxmoxCloudProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cp_type', models.CharField(choices=[('Proxmox', 'Proxmox'), ('AWS', 'AWS'), ('GCP', 'GCP')], max_length=255, null=True)),
                ('name', models.CharField(max_length=255, null=True, unique=True)),
                ('api_endpoint', models.CharField(max_length=255, null=True, unique=True)),
                ('password', models.CharField(max_length=255, null=True, unique=True)),
                ('shared_storage_name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('vmid', models.IntegerField(unique=True)),
                ('diskread', models.IntegerField()),
                ('template', models.BooleanField()),
                ('status', models.CharField(max_length=255)),
                ('disk', models.IntegerField()),
                ('node', models.CharField(max_length=255)),
                ('cpu', models.IntegerField()),
                ('diskwrite', models.IntegerField()),
                ('maxcpu', models.IntegerField()),
                ('type', models.CharField(max_length=255)),
                ('netin', models.IntegerField()),
                ('maxdisk', models.IntegerField()),
                ('mem', models.IntegerField()),
                ('maxmem', models.IntegerField()),
                ('netout', models.IntegerField()),
                ('uptime', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='VMGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('user_id', models.IntegerField()),
                ('status', models.CharField(choices=[('creating', 'creating'), ('running', 'running'), ('removing', 'removing'), ('removed', 'removed'), ('error', 'error')], max_length=255)),
                ('cloud_provider', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vms', to='kubehub.ProxmoxCloudProvider')),
            ],
        ),
        migrations.CreateModel(
            name='VmFromTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('vmid', models.IntegerField()),
                ('ip', models.CharField(max_length=255)),
                ('cores', models.IntegerField(choices=[(1, 1), (2, 2), (4, 4)], default=1)),
                ('sockets', models.IntegerField(choices=[(1, 1), (2, 2), (4, 4)], default=1)),
                ('memory', models.IntegerField(choices=[(1024, 1024), (2048, 2048), (4096, 4096), (8192, 8192), (16384, 16384)], default=1024)),
                ('boot_disk', models.IntegerField(choices=[(32, 32), (64, 64), (128, 128), (256, 256), (512, 512)], default=32)),
                ('disk_type', models.CharField(choices=[('scsi0', 'scsi0'), ('virtio0', 'virtio0'), ('ide0', 'ide0'), ('sata0', 'sata0')], default='scsi0', max_length=255)),
                ('template', models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, related_name='vms', to='kubehub.Template')),
                ('vm_group', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='template_vms', to='kubehub.VMGroup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VmFromImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('vmid', models.IntegerField()),
                ('ip', models.CharField(max_length=255)),
                ('cores', models.IntegerField(choices=[(1, 1), (2, 2), (4, 4)], default=1)),
                ('sockets', models.IntegerField(choices=[(1, 1), (2, 2), (4, 4)], default=1)),
                ('memory', models.IntegerField(choices=[(1024, 1024), (2048, 2048), (4096, 4096), (8192, 8192), (16384, 16384)], default=1024)),
                ('boot_disk', models.IntegerField(choices=[(32, 32), (64, 64), (128, 128), (256, 256), (512, 512)], default=32)),
                ('disk_type', models.CharField(choices=[('scsi0', 'scsi0'), ('virtio0', 'virtio0'), ('ide0', 'ide0'), ('sata0', 'sata0')], default='scsi0', max_length=255)),
                ('os_image', models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, related_name='vms', to='kubehub.OsImage')),
                ('vm_group', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='image_vms', to='kubehub.VMGroup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KubesprayDeploy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('deploying', 'deploying'), ('successful', 'successful'), ('failed', 'failed')], max_length=255)),
                ('k8s_cluster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kubespray_deployments', to='kubehub.KubernetesCluster')),
                ('vm_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kubespray_deployments', to='kubehub.VMGroup')),
            ],
        ),
        migrations.AddField(
            model_name='kubernetescluster',
            name='kubernetes_version_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kubehub.KubernetesVersion'),
        ),
        migrations.AddField(
            model_name='kubernetescluster',
            name='vm_group',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='kubehub.VMGroup'),
        ),
    ]
