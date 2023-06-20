# encoding:utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
import embedding.static_values as sc
from django.utils.translation import gettext as _


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
    reject_message = models.CharField(max_length=500, default='')
    enabled = models.BooleanField(default = True)

    def __str__(self):
        return u'%s %s %s' % (self.owner.username, self.name, self.uuid)


class EmbeddingDocument(models.Model):
    model = models.ForeignKey(EmbeddingModel, on_delete=models.CASCADE,)
    filename = models.CharField(max_length=500, default='')
    pages = models.IntegerField(default=0)
    summarization = models.CharField(max_length=5000, default=_('Processing'))

    def __str__(self):
        return u'%s' % (self.filename)
    

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
        return self.dialogue_id + " " + str(self.response_time-self.request_time) + "\n" + self.message


class QuizRecord(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,blank=True, null=True)
    question = models.EmailField(max_length=1500, default='')
    answer = models.CharField(max_length=2500, default='')
    response_time = models.IntegerField(default=0)
    request_time = models.IntegerField(default=0)
    llm_model = models.CharField(max_length=25, default='')
    token_request = models.IntegerField(default=0)
    token_response = models.IntegerField(default=0)

    def __str__(self):
        username = self.user.username if self.user is not None else 'None'
        return f"{username} Q:{self.question} latency: {self.response_time - self.request_time}s {self.llm_model} token request: {self.token_request} token response: {self.token_response}"
   

class OcrRecord(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,blank=True, null=True)
    image_path = models.EmailField(max_length=200, default='')
    question = models.CharField(max_length=1500, default='')
    response_time = models.IntegerField(default=0)
    request_time = models.IntegerField(default=0)

    def __str__(self):
        username = self.user.username if self.user is not None else 'None'
        return username + " " + self.question + " " + str(self.response_time - self.request_time)
        

class TherapyProfile(models.Model):
    username = models.CharField(max_length=100, default='')
    age = models.IntegerField(default=30)
    gender = models.CharField(max_length=50, default='')
    marriage = models.CharField(max_length=50, default='')
    therapy_id = models.CharField(max_length=20, default='')
    diagnosis = models.CharField(max_length=50, default='')
    evidence = models.CharField(max_length=1500, default='')

    def __str__(self):
        return self.username + self.therapy_id


class VisitorProfile(models.Model):
    username = models.CharField(max_length=100, default='')
    pin = models.CharField(max_length=6, default='')
    age = models.IntegerField(default=30)
    age_range = models.CharField(max_length=20, default='')
    gender = models.CharField(max_length=50, default='')
    marriage = models.CharField(max_length=50, default='', blank=True)
    uuid = models.CharField(max_length=20, default='')
    diagnosis = models.CharField(max_length=50, default='', blank=True)
    evidence = models.CharField(max_length=1500, default='', blank=True)

    def __str__(self):
        return f"{self.username}"


class VisitorDialogue(models.Model):
    visitor = models.ForeignKey(VisitorProfile, on_delete=models.CASCADE,)
    timestamp = models.IntegerField(default=0)
    dialogue_uuid = models.CharField(max_length=20, default='')
    msg_uuid = models.CharField(max_length=20, default='')
    message = models.CharField(max_length=1500, default='')
    role = models.CharField(max_length=10, default='')
    ack = models.BooleanField(default=False)

    def __str__(self):
        return self.visitor.username + ' ' + self.dialogue_uuid + ' ' + self.role + " " + self.message + " " + str(self.ack)


class TherapyAssessment(models.Model):
    visitor = models.ForeignKey(VisitorProfile, on_delete=models.CASCADE,)
    timestamp = models.IntegerField(default=0)
    result = models.CharField(max_length=30, default='')
    evidence = models.CharField(max_length=1500, default='', blank=True)

    def __str__(self):
        return self.visitor.username + ' ' + str(self.timestamp) + ' ' + self.result
    

class SuicideAssessment(models.Model):
    visitor = models.ForeignKey(VisitorProfile, on_delete=models.CASCADE,)
    timestamp = models.IntegerField(default=0)
    result = models.CharField(max_length=30, default='')
    evidence = models.CharField(max_length=1500, default='', blank=True)

    def __str__(self):
        return self.visitor.username + ' ' + str(self.timestamp) + ' ' + self.result
    

class DepressionAssessment(models.Model):
    visitor = models.ForeignKey(VisitorProfile, on_delete=models.CASCADE,)
    timestamp = models.IntegerField(default=0)
    result = models.CharField(max_length=20, default='')
    evidence = models.CharField(max_length=1500, default='', blank=True)

    def __str__(self):
        return self.visitor.username + ' ' + str(self.timestamp) + ' ' + self.result
    

class FruitOrder(models.Model):
    username = models.CharField(max_length=300, default='')
    area = models.CharField(max_length=30, default='')
    mobile = models.CharField(max_length=30, default='')
    address = models.CharField(max_length=1000, default='')
    notes = models.CharField(max_length=1000, default='')
    size = models.CharField(max_length=30, default='')
    quantity = models.IntegerField(default=0)
    order_state = models.CharField(max_length=100, default='')
    created_time = models.IntegerField(default=0)
    paid_time = models.IntegerField(default=0)
    delivery_time = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    pi_id = models.CharField(max_length=100, default='')
    delivery_id = models.CharField(max_length=100, default='')
    order_id = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.username + ' ' + self.mobile + ' ' + self.result