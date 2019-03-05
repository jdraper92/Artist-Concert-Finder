# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.
class User(models.Model):
	email = models.CharField(max_length=100)
	create_date = models.DateTimeField('date created')
	city = models.CharField(max_length=100,default='Chicago')

	def __str__(self):
		return self.email

class Artist(models.Model):
	name = models.CharField(max_length=100)
	users = models.ManyToManyField(User)

	def __str__(self):
		return self.name

class Concert(models.Model):
	band = models.CharField(max_length=300)
	venue = models.CharField(max_length=300)
	concert_date = models.DateTimeField('date of concert')
	city = models.CharField(max_length=300,default='Chicago')

	def __str__(self):
		return self.band + '@ ' + self.venue 

class Links(models.Model):
	url = models.CharField(max_length=100)
	users = models.ManyToManyField(User)

	def __str__(self):
		return self.url

class Update(models.Model):
	last = models.DateTimeField('last updated')
	city = models.CharField(max_length=30,default='chicago')
	def __str__(self):
		return self.last.strftime('%m-%d-%Y')