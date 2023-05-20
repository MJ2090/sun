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

    def __str__(self):
        return u'%s %s %s %s' % (self.user.username, self.token_amount, self.model_type, self.secret)

    def __unicode__(self):
        return u'%s %s %s %s' % (self.user.username, self.token_amount, self.model_type, self.secret)


class PromptModel(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE,)
    name = models.CharField(max_length=20, default='')
    history = models.CharField(max_length=1500, default='')

    def __str__(self):
        return u'%s %s %s' % (self.owner.username, self.name, self.history)


class EmbeddingModel(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE,)
    name = models.CharField(max_length=20, default='')
    uuid = models.CharField(max_length=10, default='')
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return u'%s %s %s' % (self.owner.username, self.name, self.uuid)


class Contact(models.Model):
    username = models.CharField(max_length=100, default='')
    email = models.EmailField(max_length=100, default='')
    message = models.CharField(max_length=1500, default='')

    def __str__(self):
        return self.username


class Dialogue(models.Model):
    role = models.CharField(max_length=20, default='')
    message = models.EmailField(max_length=5000, default='')
    dialogue_id = models.CharField(max_length=10, default='')
    source = models.CharField(max_length=20, default='chat')
    response_time = models.IntegerField(default=0)
    request_time = models.IntegerField(default=0)
    prompt_tokens = models.IntegerField(default=0)
    completion_tokens = models.IntegerField(default=0)
    total_tokens = models.IntegerField(default=0)

    def __str__(self):
        return self.dialogue_id + " " + str(self.response_time-self.request_time) + "\n" + self.message;
