# encoding:utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


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

    def __unicode__(self):
        return u'%s %s' % (self.username, self.external_id)
