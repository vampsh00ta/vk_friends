from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import related
from django.db.models import Q
# Create your models here.



class Customer(AbstractUser):
    friends = models.ManyToManyField("Customer",blank=True,related_name='customer_friends')
    subscriptions = models.ManyToManyField("Customer",blank=True,related_name= "customer_subscribed_on",through = 'FriendshipRequest')
    @property
    def followers(self):
        followers = Customer.objects\
            .prefetch_related('subscriptions') \
            .filter(subscriptions =self.id )
        return followers
    def __str__(self):
        return f"{self.id}"

class FriendshipRequest(models.Model):
    from_person = models.ForeignKey(Customer, related_name='from_person',on_delete=models.CASCADE)
    to_person = models.ForeignKey(Customer, related_name='to_person',on_delete=models.CASCADE)


