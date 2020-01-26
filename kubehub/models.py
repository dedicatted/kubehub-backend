from django.db import models

class CloudProvider(models.Model):
    cp_type = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    api_endpoint = models.CharField(max_length=50)
    password = models.CharField(max_length=20)

    # def save(self, *args, **kwargs):
    #     self.save()

    def __str__(self):
        return f'id: {self.id} name: {self.name} api_endpoint: {self.api_endpoint} password: {self.password}'
