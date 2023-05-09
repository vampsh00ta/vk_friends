from django.db import models

from auth_service.models import Customer


# Create your models here.
class OldRequest(models.Model):
    # id = models.IntegerField(primary_key=True)
    from_person = models.ForeignKey(Customer, related_name='OldRequest.from_person+', on_delete=models.CASCADE)
    to_person = models.ForeignKey(Customer, related_name='OldRequest.to_person+', on_delete=models.CASCADE)