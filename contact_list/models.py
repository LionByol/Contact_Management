from __future__ import unicode_literals

from django.db import models

import datetime
from django.utils import timezone

class Question(models.Model):
   question_text = models.CharField(max_length=200)
   pub_date = models.DateTimeField('date published')

   def __str__(self):
       return self.question_text

   def was_puplished_recently(self):
       now = timezone.now()
       return now - datetime.timedelta(days=1) <= self.pub_date <= now

   was_puplished_recently.admin_order_field = 'pub_date'
   was_puplished_recently.boolean = True
   was_puplished_recently.short_description = 'Published recently?'


class Choice(models.Model):
   question = models.ForeignKey(Question)
   choice_test = models.CharField(max_length=200)
   votes = models.IntegerField(default=0)

   def __str__(self):
       return self.choice_test


class Contactlist(models.Model):
   email = models.CharField(max_length=50)
   name = models.CharField(max_length=50)
   company = models.CharField(max_length=50)
   source = models.CharField(max_length=50)
   lasttouch = models.CharField(max_length=50)
   nexttouch = models.CharField(max_length=50)   
   online = models.ForeignKey('Online', default=1)
   class Meta:
 	  db_table = "contactlist"
class Online(models.Model):
   domain = models.CharField(max_length=30)
   class Meta:
 	  db_table = "online"

class UploadFileModel(models.Model):
	title = models.CharField(max_length=50)
	file = models.FileField(upload_to='tmp')