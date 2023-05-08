from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import related
from django.db.models import Q
# Create your models here.



class Customer(AbstractUser):
    friends = models.ManyToManyField("Customer",blank=True,related_name='customer_friends')
    subscribed_on = models.ManyToManyField("Customer",blank=True,related_name= "customer_subscribed_on",through = 'FriendshipRequest')
    @property
    def followed_by(self):
        followed_by = Customer.objects.filter(Q(subscribed_on =self.id ) & ~Q(friends =self.id ))
        return followed_by
    def __str__(self):
        return f"{self.id}"

class FriendshipRequest(models.Model):
    from_person = models.ForeignKey(Customer, related_name='from_person',on_delete=models.CASCADE)
    to_person = models.ForeignKey(Customer, related_name='to_person',on_delete=models.CASCADE)


