# encoding:utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
import embedding.static_values as sc

class UserProfileManager(UserManager):
    def search_user_by_username(self, user_name):
        return self.filter(username__contains=user_name)

    def get_by_external_id(self, external_id):
        users = self.filter(external_id=external_id)
        if users:
            return users[0]
        return None

    def wrap(self, _user):
        ret = {'username': _user.username,
               'email': _user.email,
               }
        return ret


class UserProfile(AbstractUser):
    objects = UserProfileManager()

    external_id = models.CharField(max_length=20, default='')
    max_token = models.IntegerField(default=100000)
    used_token = models.IntegerField(default=0)
    left_token = models.IntegerField(default=100000)

    def __unicode__(self):
        return u'%s %s' % (self.username, self.external_id)


class TokenConsumption(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,)
    token_amount = models.IntegerField(default=0)
    model_type = models.IntegerField(default=0, choices=sc.MODEL_TYPES)
    secret = models.CharField(max_length=20, default='')

    def __unicode__(self):
        return u'%s %s %s %s' % (self.user.username, self.token_amount, self.model_type, self.secret)